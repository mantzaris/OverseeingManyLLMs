"""Serial vLLM HTTP client. Never loads a model or provides CPU inference."""

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request

from .domain import ACTIONS, canonical, digest
from .io import append_jsonl, utc_now
from .simulator import ProposalFailure

MODEL = "Qwen/Qwen2.5-7B-Instruct"
REVISION = "a09a35458c702b33eeacc393d103063234e8bc28"
MANUAL = (
    "You coordinate synthetic campus ventilation maintenance. Each job's hidden fault is filter or sensor. "
    "A filter fault requires replace_filter; a sensor fault requires reset_sensor. "
    "The first clue identifies the fault with probability 0.8, the second with probability 0.6; "
    "their noise is independent. Prior faults are equally likely and jobs are independent. "
    "Choose a repair from the current clues. Work continues while a shared supervisor reviews requests. "
    "An incorrect workflow costs cost_per_tick until deadline, then terminal_cost. "
    "All proposals request review automatically. Supervisor feedback is binding for the job it names. "
    "Return only a JSON object with exactly one field action, either replace_filter or reset_sensor."
)
ACTION_SCHEMA = {"type": "object", "properties": {"action": {"type": "string", "enum": list(ACTIONS)}},
                 "required": ["action"], "additionalProperties": False}


def parse_action(body):
    data = json.loads(body)
    if len(data["choices"]) != 1 or data["choices"][0]["finish_reason"] != "stop":
        raise ValueError("Missing choice or truncated generation")

    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Duplicate JSON field")
            result[key] = value
        return result

    action = json.loads(data["choices"][0]["message"]["content"], object_pairs_hook=unique_object)
    if not isinstance(action, dict) or set(action) != {"action"} or action["action"] not in ACTIONS:
        raise ValueError("Invalid structured action")
    return action["action"]


class GPUClient:
    # Actual hardware is established by the same-pod placement evidence, not this label.
    evidence = "live_gpu"

    def __init__(self, config, raw_path, deadline, max_calls=12, budget=None):
        parsed = urllib.parse.urlparse(config["base_url"])
        if parsed.scheme != "http" or parsed.hostname != "127.0.0.1" or parsed.path != "/v1":
            raise ValueError("Run the client on the verified GPU pod against its loopback vLLM server")
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError("Endpoint must not contain credentials or query data")
        self.config, self.deadline, self.max_calls = config, deadline, max_calls
        self.budget = budget
        self.session_call_id = None
        self.attempt_deadline = deadline
        self.base_url = config["base_url"]
        self.raw_path = Path(raw_path)
        self.raw_path.parent.mkdir(parents=True, exist_ok=True)
        self.raw_path.touch(exist_ok=False)
        # Disable environment proxies and automatic redirecting to another host.
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
        self.counts = {"scheduled_calls": 0, "attempts": 0, "prompt_tokens": 0,
                       "completion_tokens": 0, "unknown_token_attempts": 0,
                       "request_wall_seconds": 0.0}

    def stats(self):
        return dict(self.counts)

    def _http(self, url, payload):
        remaining = (min(self.deadline, self.attempt_deadline) - datetime.now(timezone.utc)).total_seconds()
        if remaining <= 0:
            raise TimeoutError("Stage deadline reached")
        request = urllib.request.Request(url, data=canonical(payload).encode(),
                                         headers={"Content-Type": "application/json"})
        try:
            with self.opener.open(request, timeout=min(self.config["timeout_seconds"], remaining)) as response:
                return response.status, response.read().decode("utf-8"), response.headers.get("X-Request-Id")
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read().decode("utf-8", errors="replace"), exc.headers.get("X-Request-Id")

    def action(self, public_observation, metadata, sample):
        if self.counts["scheduled_calls"] >= self.max_calls:
            raise ProposalFailure("Scheduled model-call cap reached")
        if self.budget is not None:
            self.session_call_id = self.budget.reserve_call(metadata, sample)
        self.counts["scheduled_calls"] += 1
        last_error = "No attempt"
        for retry in range(self.config["max_attempts_per_call"]):
            self.attempt_deadline = min(self.deadline, datetime.now(timezone.utc)
                                        + timedelta(seconds=self.config["timeout_seconds"]))
            seed = int(digest(dict(metadata, sample=sample, retry=retry))[:8], 16)
            messages = [{"role": "system", "content": MANUAL + (
                " Strictly follow the one-field JSON schema; include no prose." if retry else "")},
                        {"role": "user", "content": canonical(public_observation)}]
            payload = {"model": self.config["model"], "messages": messages,
                       "temperature": self.config["temperature"], "top_p": self.config["top_p"],
                       "max_tokens": self.config["max_output_tokens"], "seed": seed, "n": 1,
                       "guided_json": ACTION_SCHEMA, "stream": False}
            record = dict(metadata, sample=sample, retry=retry, seed=seed, wall_utc=utc_now(),
                          observation_hash=digest(public_observation), request=payload,
                          inference_request_attempted=False, evidence=self.evidence,
                          attempt_deadline_utc=self.attempt_deadline.isoformat())
            if self.budget is not None:
                record["session_call_id"] = self.session_call_id
            append_jsonl(self.raw_path, dict(record, phase="attempt_started"))
            start = time.monotonic()
            inference_start = None
            try:
                token_status, token_body, _ = self._http(self.base_url[:-3] + "/tokenize",
                                                       {"model": self.config["model"], "messages": messages})
                record["tokenization_status"] = token_status
                record["tokenization_response"] = token_body
                if token_status != 200:
                    raise ValueError("Tokenization HTTP {}".format(token_status))
                count = json.loads(token_body)["count"]
                if type(count) is not int or not 0 < count <= self.config["max_input_tokens"]:
                    raise ValueError("Input token limit exceeded or invalid count")
                if datetime.now(timezone.utc) >= self.deadline:
                    raise TimeoutError("Stage deadline reached before inference")
                if self.budget is not None:
                    self.budget.reserve_attempt(self.session_call_id, retry)
                self.counts["attempts"] += 1
                record["inference_request_attempted"] = True
                append_jsonl(self.raw_path, dict(record, phase="inference_started"))
                inference_start = time.monotonic()
                status, body, request_id = self._http(self.base_url + "/chat/completions", payload)
                record.update(http_status=status, raw_response=body, request_id=request_id)
                if status != 200:
                    raise ValueError("Inference HTTP {}".format(status))
                action = parse_action(body)
                record["parsed_action"] = action
            except Exception as exc:
                last_error = "{}: {}".format(type(exc).__name__, exc)
                record["error"] = last_error
            finally:
                if inference_start is not None:
                    elapsed = time.monotonic() - inference_start
                    self.counts["request_wall_seconds"] += elapsed
                    record["inference_wall_seconds"] = elapsed
                    try:
                        response_data = json.loads(record.get("raw_response", "{}"))
                        record["response_id"] = response_data.get("id")
                        usage = response_data["usage"]
                        if not all(isinstance(usage.get(k), int) and usage[k] >= 0 for k in ("prompt_tokens", "completion_tokens")):
                            raise ValueError("Invalid usage")
                        self.counts["prompt_tokens"] += usage["prompt_tokens"]
                        self.counts["completion_tokens"] += usage["completion_tokens"]
                        record["usage"] = usage
                    except (KeyError, ValueError, TypeError):
                        self.counts["unknown_token_attempts"] += 1
                        record["usage"] = None
                record["attempt_wall_seconds"] = time.monotonic() - start
                append_jsonl(self.raw_path, dict(record, phase="attempt_finished"))
            if "parsed_action" in record:
                return record["parsed_action"]
            if datetime.now(timezone.utc) >= self.deadline:
                break
        raise ProposalFailure(last_error)

    def pair(self, public_observation, metadata):
        # Identical observations and independent sample seeds; no policy in either seed.
        primary = self.action(public_observation, metadata, sample=0)
        secondary = self.action(public_observation, metadata, sample=1)
        return primary, secondary
