"""Authored natural-language scope challenges, reported separately from dialogues."""
import argparse
import json
from .client import ART, canonical, generate, parsed, write_json
from .collect import messages
from .prompts import EXTRACT,PARSE,HISTORY,MEMORY,dialogue_text
from .records import DecisionController,extracted_records,parsed_queries,model_answers

# Public text and evaluator-only expectations are separated before any model call.
CASES=[
 ('ordinary','Keep the hotel cheap. I do not need any restaurant recommendations.', 'Which spending band applies to accommodation?', 'cheap','preference'),
 ('different_domains','Use a cheap hotel, but an expensive restaurant.', 'Which spending band applies to eating out?', 'expensive','preference'),
 ('revision','I wanted a cheap hotel earlier. Change that to an expensive hotel now.', 'What price range should the hotel match?', 'expensive','preference'),
 ('undecided_conflict','For the hotel, one organizer requires cheap and another requires expensive. I have not decided which requirement to follow.', 'What price range should the hotel match?',None,'preference'),
 ('preference_not_approval','The hotel should be cheap. I have not authorized any booking.', 'May I place a non-refundable hotel booking now?',None,'approval'),
 ('specific_approval','I approve booking the Ashley Hotel for this request only. Other bookings need a new approval.', 'May I now book a different hotel?',None,'approval'),
 ('explicit_exception','Use cheap hotels except for the conference night, when an expensive hotel is acceptable.', 'What price range should the hotel match for an ordinary night?', 'cheap','preference'),
 ('paraphrased_exception','The premium hotel budget is reserved for the workshop evening. Accommodation on the ordinary nights must stay cheap.', 'For the workshop evening, what hotel price range is authorized?', 'expensive','preference'),
 ('similar_project','This trip needs a cheap hotel. The expensive hotel instruction belongs to a different project.', 'What price range should the hotel match on this trip?', 'cheap','preference'),
 ('inference_not_instruction','The hotel agent guessed that I wanted an expensive hotel. I have not told it my preferred price range.', 'What price range should the hotel match?',None,'preference'),
 ('revocation','I previously wanted a cheap hotel. Withdraw that preference; I have not selected a new price range.', 'What price range should the hotel match?',None,'preference'),
 ('explicit_reference','Use a moderate hotel. The restaurant should be in the same price range as the hotel.', 'Which spending band applies to eating out?', 'moderate','preference'),
]

def declaration():
    public=[];private=[]
    for i,(family,text,query,expected,kind) in enumerate(CASES):
        public.append(dict(id='challenge_%02d'%i,family=family,project='trip',
                           messages=[dict(turn=0,role='user',text=text)],
                           query=dict(id='q',text=query),operation_kind=kind))
        private.append(dict(id='challenge_%02d'%i,expected=expected))
    write_json(ART/'frozen/challenge_public.json',public)
    write_json(ART/'frozen/challenge_evaluation_only.json',private)

def collect():
    from .freeze import verify_frozen
    verify_frozen()
    if not (ART/'frozen/commit.json').exists():raise RuntimeError('Commit the declared comparison first')
    cases=json.loads((ART/'frozen/challenge_public.json').read_text());results=[]
    for case in cases:
        for rep in range(2):
            prefix=case['id']+'_'+str(rep);seed=94000+int(case['id'].split('_')[1])*10+rep
            extract=generate(prefix+'_extract',messages(EXTRACT,dialogue_text(case['messages'])),seed,768,True)
            parse=generate(prefix+'_parse',messages(PARSE,canonical({'queries':[case['query']]})),seed+1000,384,True)
            history=generate(prefix+'_history',messages(HISTORY,dialogue_text(case['messages'])+'\nQUESTIONS\n'+canonical([case['query']])),seed+2000,384,True)
            current,_=extracted_records(parsed(extract),case['messages'],False)
            memory=generate(prefix+'_memory',messages(MEMORY,canonical(dict(memories=list(current.values()),queries=[case['query']]))),seed+3000,384,True)
            row=dict(id=case['id'],replicate=rep,outputs={k:parsed(v) for k,v in [('extract',extract),('parse',parse),('history',history),('memory',memory)]},
                     call_ids=[x['call_id'] for x in (extract,parse,history,memory)])
            results.append(row);write_json(ART/'challenges_prepared.json',results)
            print(case['id'],rep,flush=True)

def analyze():
    public={x['id']:x for x in json.loads((ART/'frozen/challenge_public.json').read_text())}
    labels={x['id']:x['expected'] for x in json.loads((ART/'frozen/challenge_evaluation_only.json').read_text())}
    rows=[]
    for prepared in json.loads((ART/'challenges_prepared.json').read_text()):
        case=public[prepared['id']];out=prepared['outputs'];key=parsed_queries(out['parse']).get('q')
        for method in ('full_history','semantic_memory','global_barrier','dependency_barrier','no_source_guard'):
            request=dict(id='q',text=case['query']['text'],project=case['project'],key=key,kind=case['operation_kind'])
            if case['operation_kind']=='approval':value=None;reason='Shared automatic action-specific approval guard'
            elif method in ('full_history','semantic_memory'):
                value=model_answers(out['history' if method=='full_history' else 'memory']).get('q');reason='Model answer'
            else:
                records,rejected=extracted_records(out['extract'],case['messages'],method!='no_source_guard')
                c=DecisionController(case['project']);c.publish(records);answer=c.lookup(request)
                value=answer.get('value');reason=answer.get('reason')
            expected=labels[case['id']]
            rows.append(dict(id=case['id'],family=case['family'],replicate=prepared['replicate'],method=method,
                             returned=value,expected=expected,needs_user=value is None,
                             correct_auto_answer=value is not None and value==expected,
                             incorrect_transfer=value is not None and value!=expected,
                             appropriate_abstention=value is None and expected is None,
                             extra_question=value is None and expected is not None,reason=reason))
    write_json(ART/'challenge_results.json',rows)
    return rows

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['declare','collect','analyze']);a=p.parse_args()
    {'declare':declaration,'collect':collect,'analyze':analyze}[a.action]()
