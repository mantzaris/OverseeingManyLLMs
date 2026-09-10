"""Hash the downloaded pinned model/tokenizer files; never copy weights into Git."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time

out = Path(__file__).resolve().parent
revision = "a09a35458c702b33eeacc393d103063234e8bc28"
snapshot = Path("model-cache/hub/models--Qwen--Qwen2.5-7B-Instruct/snapshots") / revision
assert snapshot.is_dir(), "Pinned model snapshot is missing"
started = time.monotonic()
record = {"model": "Qwen/Qwen2.5-7B-Instruct", "revision": revision,
          "captured_utc": datetime.now(timezone.utc).isoformat(), "files": {}}
for path in sorted(snapshot.rglob("*")):
    if path.is_file():
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
                digest.update(block)
        record["files"][str(path.relative_to(snapshot))] = {
            "bytes": path.stat().st_size, "sha256": digest.hexdigest()}
assert len([name for name in record["files"] if name.endswith(".safetensors")]) == 4
record["hashing_wall_seconds"] = time.monotonic() - started
(out / "model_files.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
print(json.dumps({"files_hashed": len(record["files"]),
                  "total_bytes": sum(item["bytes"] for item in record["files"].values()),
                  "hashing_wall_seconds": record["hashing_wall_seconds"]}, indent=2))
