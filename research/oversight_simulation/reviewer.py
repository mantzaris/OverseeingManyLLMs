"""Simulated response environment. Evaluator labels never enter policy selection."""
import math,random,hashlib


def rng(seed,qid,attempt,key):
    value=int(hashlib.sha256(('%s|%s|%s|%s'%(seed,qid,attempt,key)).encode()).hexdigest()[:16],16)
    return random.Random(value)


def uniform(seed,qid,attempt,key):return rng(seed,qid,attempt,key).random()


def jitter(seed,qid,attempt,key,sigma):
    return math.exp(rng(seed,qid,attempt,key).gauss(-sigma*sigma/2,sigma))


def orientation_time(item,now,memory,completed,cfg):
    scale=min(1.25,max(.75,item['source_characters']/3200.))
    source=item['source_id'];s=cfg['orientation']*scale
    if source not in memory:return s
    last_time,last_index=memory[source]
    gap=max(0,now-last_time);intervening=max(0,completed-last_index)
    retained=math.exp(-gap/cfg['memory_seconds']-intervening/cfg['memory_intervening'])
    return s*(cfg['recent_fraction']+(1-cfg['recent_fraction'])*(1-retained))


class ReviewerEnvironment:
    """Annotations define simulated correctness, never certified human behavior."""
    def __init__(self, annotations, initial_correct):
        self.annotations=annotations;self.initial_correct=initial_correct

    def plan(self,item,policy,seed,attempt,now,memory,completed,previous_source,cfg,group_opened):
        qid=item['id'];u=lambda key:uniform(seed,qid,attempt,key)
        factor=1+min(40,len(item['question'].split()))/80.
        component=lambda seconds,key:seconds*factor*jitter(seed,qid,attempt,key,cfg['jitter_sigma'])
        phases=[]
        if group_opened and policy=='G':phases.append(('grouping',cfg['group_seconds']))
        phases.extend([('orientation',orientation_time(item,now+sum(x[1] for x in phases),memory,completed,cfg)),('question',component(cfg['question_seconds'],'question'))])
        manual=policy=='M' or not item['output']['answer']
        initial=self.initial_correct[qid]
        origin='initial_draft';action='approve';correct=initial;recognized=False
        if manual:
            phases.append(('construction',component(cfg['manual_seconds'],'manual')))
            correct=u('manual_success')<cfg['manual_accuracy'];action='correct';origin='simulated_manual_construction'
            recognized=not correct and u('recognized_failure')<cfg['recognized_failure']
        else:
            phases.append(('verification',component(cfg['verify_seconds'],'verification')))
            if initial:
                if u('damage')<cfg['damage']:action='correct';correct=False;origin='simulated_damage'
            elif u('detection')<cfg['detect']:
                phases.append(('construction',component(cfg['construction_seconds'],'correction')))
                correct=u('correction_success')<cfg['correct'];action='correct';origin='simulated_detected_error_repair'
                recognized=not correct and u('recognized_failure')<cfg['recognized_failure']
        carry=previous_source==item['source_id'] and correct and u('carryover')<cfg['carryover']
        if carry:correct=False;action='correct';origin='simulated_carryover_error'
        if recognized:action='defer' if attempt<cfg['max_attempts'] else 'reject';origin='simulated_recognized_failure'
        phases.append(('interaction',cfg['interaction_seconds']/2))
        releases=action in ('approve','correct')
        if releases:phases.append(('release',cfg['interaction_seconds']/2))
        gold=self.annotations[qid]
        output=item['output']
        if action=='correct':
            output=dict(answer=(gold['answer'] if isinstance(gold['answer'],list) else [gold['answer']]) if correct else ['SIMULATED_UNSUCCESSFUL_RESPONSE'],
                        scale=gold['scale'] if correct else '',evidence=[],derivation='SIMULATED response, not a generated or human answer',issues=[])
        return dict(phases=phases,action=action,correct=bool(correct),output=output,releases=releases,origin=origin,carryover_harm=bool(carry),manual=manual,
                    initial_correct=initial,recognized_failure=recognized)
