#!/usr/bin/env python3
"""Serial GPU-only HTTP calls. Public task files contain no evaluator fields."""
import argparse,json,time,urllib.request,hashlib
from pathlib import Path
from datetime import datetime,timezone
SYSTEM='This is a closed-set component diagnosis task for a single-zone air handler. Choose the MOST LIKELY condition among normal, outdoor_damper, heating_valve, cooling_valve. These are the only possible annotated conditions; faults include stuck or leaking components. Use abstain only if observations are missing or unusable, not merely because certainty is impossible. Temperatures are degrees Fahrenheit; controls are fractional commands, not verified physical positions. Supply air substantially above its cooling setpoint despite cooling can indicate heating leakage; excessive cooling relative to mixed air and setpoints can indicate cooling-valve trouble. Compare outdoor, return and mixed temperatures with damper commands. Assess all evidence. Do not infer repair outcomes. Reply only JSON: {"diagnosis":"category","reason":"brief evidence"}.'
REVIEW='Independently review the proposed diagnosis using only the sensor evidence. You may preserve it, correct its category, or abstain. A proposal may be wrong. Do not assume another reviewer has access to additional measurements. Return the same JSON schema.'
def main():
    p=argparse.ArgumentParser();p.add_argument('split');a=p.parse_args();root=Path('artifacts/stage7_empirical');auth=json.loads((root/'authorization.json').read_text())
    out=root/a.split;out.mkdir(exist_ok=False);source_split='development' if a.split.startswith('development') else a.split;tasks=json.loads((root/(source_split+'_public.json')).read_text());ledger=root/'ledger.jsonl'
    for task in tasks:
        result=dict(case_id=task['case_id']);public=dict(task['public']);names={'sat':'supply_air_temperature','heat_sp':'supply_heating_setpoint','cool_sp':'supply_cooling_setpoint','outdoor':'outdoor_temperature','mixed':'mixed_air_temperature','return':'return_air_temperature','fan':'fan_speed_command','damper':'outdoor_damper_command','cool_valve':'cooling_valve_command','heat_valve':'heating_valve_command'}
        public['readings']={names[k]:dict(zip(public['statistic_order'],v)) for k,v in public['readings'].items()};public.pop('statistic_order');evidence=json.dumps(public,separators=(',',':'))
        for role in ('proposal','review'):
            message=evidence if role=='proposal' else REVIEW+'\nEvidence: '+evidence+'\nProposal: '+result['proposal']
            result[role]='';attempts=[]
            for retry in range(2):
                now=datetime.now(timezone.utc)
                if now>=datetime.fromisoformat(auth['inference_cutoff_utc']):raise SystemExit('Stage 7 inference cutoff')
                count=sum(1 for _ in ledger.open()) if ledger.exists() else 0
                if count>=auth['attempt_limit']:raise SystemExit('Stage 7 attempt ceiling')
                seed=int(hashlib.sha256((task['case_id']+role+str(retry)).encode()).hexdigest()[:8],16)%2147483647
                payload=dict(model='Qwen/Qwen2.5-7B-Instruct',messages=[dict(role='system',content=SYSTEM),dict(role='user',content=message)],temperature=.3,top_p=1,max_tokens=128,seed=seed)
                record=dict(case_id=task['case_id'],role=role,retry=retry,started_utc=now.isoformat(),request=payload)
                with ledger.open('a') as f:f.write(json.dumps(dict(event='attempt_reserved',case_id=task['case_id'],role=role,retry=retry,utc=now.isoformat()))+'\n')
                start=time.monotonic()
                try:
                    request=urllib.request.Request('http://127.0.0.1:8000/v1/chat/completions',json.dumps(payload).encode(),{'Content-Type':'application/json'})
                    with urllib.request.urlopen(request,timeout=min(60,(datetime.fromisoformat(auth['inference_cutoff_utc'])-now).total_seconds())) as response:raw=response.read().decode()
                    record['response']=raw;body=json.loads(raw);text=body['choices'][0]['message']['content'];parsed=json.loads(text)
                    assert parsed['diagnosis'] in ('normal','outdoor_damper','heating_valve','cooling_valve','abstain')
                    record['success']=True;result[role]=text
                except Exception as e:record.update(success=False,error=type(e).__name__+': '+str(e))
                record['elapsed_seconds']=time.monotonic()-start;attempts.append(record)
                (out/(task['case_id']+'_'+role+'_attempts.json')).write_text(json.dumps(attempts,indent=2)+'\n')
                if record['success']:break
            result[role+'_attempts']=len(attempts)
        (out/(task['case_id']+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(task['case_id'],flush=True)
if __name__=='__main__':main()
