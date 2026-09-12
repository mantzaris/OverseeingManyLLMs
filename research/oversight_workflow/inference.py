"""Small public answer interface. Full source retained even if parsing fails."""
import time
from .transport import generate
from .common import ART,read,write
from research.adaptive_correction_transfer.answers import source_text,prepare
SYSTEM='''Answer the financial question using only the supplied table and source paragraphs. Return JSON with answer (a list), scale, evidence (optional table cell IDs or paragraph IDs), and derivation (an optional explanation under 35 words). Scale is "", "thousand", "million", "billion", or "percent". Read source headings, entity and comparison periods carefully. If unsupported, return answer:[] and explain the limitation. For arithmetic you may use a simple expression beginning with "=" in the answer list. A calculator evaluates +,-,*,/ and rounds to two decimals. Do not give an executable program. No text outside JSON.'''

def messages(c,q,previous=None):
    text=source_text(c)+'\nORIGINAL QUESTION: '+q['question']
    if previous is not None:
        text+='\nYour earlier draft: '+str(previous)+'\nRe-read the source and this same question. Return a fresh checked answer. No reference answer or new verified correction is available. Keep it if justified.'
    return [dict(role='system',content=SYSTEM),dict(role='user',content=text)]

def answer(c,q,replica,stage='primary',previous=None):
    cid=f"{stage}_r{replica}_{q['id']}"
    seed=912000+replica*10000+c['source_index']*10+q['order']
    started=time.monotonic();payload,raw=generate(cid,messages(c,q,previous),seed,230)
    output=prepare(payload,c)
    row=dict(call_id=cid,context_id=c['id'],question_id=q['id'],replica=replica,output=output,
             request_sha256=raw['request_sha256'],status=raw['status'],elapsed_seconds=time.monotonic()-started,
             generation_seconds=sum(a['elapsed_seconds'] for a in raw['attempts']),
             prompt_tokens=sum(a.get('response',{}).get('usage',{}).get('prompt_tokens',0) for a in raw['attempts']),
             completion_tokens=sum(a.get('response',{}).get('usage',{}).get('completion_tokens',0) for a in raw['attempts']))
    write(ART/'prepared'/f'{cid}.json',row)
    return row

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--pilot',action='store_true');args=p.parse_args()
    if args.pilot:
        c=read('artifacts/adaptive_correction_transfer/development_manifest.json')['contexts'][0]
        rows=[answer(c,q,0,'pilot') for q in c['questions']]
        write(ART/'pilot.json',rows)
        print([(r['status'],round(r['generation_seconds'],2),bool(r['output']['answer'])) for r in rows])
