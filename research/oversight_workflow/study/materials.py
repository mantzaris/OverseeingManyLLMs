"""Deterministic source-disjoint packet allocation, without model outcomes or labels."""
from research.oversight_workflow.common import ART,ROOT,read,write,digest

def main():
    contexts=read(ART/'frozen/manifest.json')['contexts'];packets=[[] for _ in range(4)]
    # Greedy balance on public source-character count, six contexts per packet.
    for c in sorted(contexts,key=lambda c:(-len(str(c['table'])+str(c['paragraphs'])),c['source_index'])):
        eligible=[i for i,p in enumerate(packets) if len(p)<6]
        k=min(eligible,key=lambda i:(sum(len(str(x['table'])+str(x['paragraphs'])) for x in packets[i]),i));packets[k].append(c)
    manifest=[dict(packet=i,context_ids=[c['id'] for c in p],questions=sum(len(c['questions']) for c in p),source_characters=sum(len(str(c['table'])+str(c['paragraphs'])) for c in p)) for i,p in enumerate(packets)]
    assert len({i for p in manifest for i in p['context_ids']})==24
    orders=[[0,1,3,2],[1,2,0,3],[2,3,1,0],[3,0,2,1]]
    cells=[dict(cell=4*i+j,condition_order=order,packet_order=[(period+j)%4 for period in range(4)]) for i,order in enumerate(orders) for j in range(4)]
    target=ROOT/'research/oversight_workflow/study'
    write(target/'packets.json',dict(rule='Six contexts per packet, greedily balanced on public source-character count; no output, correctness or annotation used.',packets=manifest,assignment_cells=cells,conditions=['B/lower','C/lower','B/higher','C/higher'],status='Prospective. No participant data. Timing remains a formative-pilot decision.'))
    old=read(ROOT/'artifacts/adaptive_correction_transfer/development_manifest.json')['contexts'][0]
    write(target/'training.json',dict(context=old,questions=old['questions'][:2],instructions=['Compare the generated answer with the original source.','Approve then explicitly release a version.','Defer a question and write a note.','Resume it; verify that the note and source persist.','A new output version needs a new review.'],status='Previously inspected development material, reserved for practice.'))
    write(target/'questionnaires.json',dict(status='Prospective instrument, not responses',raw_tlx=[dict(item=x,range=[0,100],anchors=a) for x,a in [('Mental demand',['Very low','Very high']),('Physical demand',['Very low','Very high']),('Temporal demand',['Very low','Very high']),('Performance',['Perfect','Failure']),('Effort',['Very low','Very high']),('Frustration',['Very low','Very high'])]],control_items=[dict(text=s,range=[1,7],anchors=['Strongly disagree','Strongly agree']) for s in ['I knew which work still needed my attention.','I felt in control of which answers were released.','I could return to deferred work without losing my place.']],background=['Experience reading financial tables','Experience using LLM agents','Quantitative training','Accessibility needs'],exit=['What made you decide to defer a request?','When did source grouping help or hinder you?','Did you ever feel that unfinished work was hidden?']))
    print('Four disjoint packets:',[(p['questions'],p['source_characters']) for p in manifest])

if __name__=='__main__':main()
