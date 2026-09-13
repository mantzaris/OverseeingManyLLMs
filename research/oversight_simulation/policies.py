"""Selectors see released public IDs/arrivals only. No labels or random draws."""

def choose(pending,policy,previous_source,group):
    if not pending:return None,[],False
    ordered=sorted(pending,key=lambda x:(x['arrival'],x['id']))
    byid={x['id']:x for x in ordered}
    if policy in ('G','Q-source-aware'):
        live=[i for i in group if i in byid]
        if live:return live[0],live,False
        first=ordered[0]
        same=[x['id'] for x in ordered if x['source_id']==first['source_id']][:3]
        return first['id'],same,len(same)>1
    if policy=='Q-sticky':
        same=[x for x in ordered if x['source_id']==previous_source]
        if same:return same[0]['id'],[],False
    elif policy not in ('Q','M'):raise ValueError(policy)
    return ordered[0]['id'],[],False
