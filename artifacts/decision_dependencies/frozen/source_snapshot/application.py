"""Local read-only travel planning tools. No evaluator labels or network access."""
from .records import normalize

def artifact(role,values,databases):
    """Executable local planning artifacts, with no booking or external effects."""
    if role in ('lodging_shortlist','dining_shortlist'):
        domain='hotel' if role=='lodging_shortlist' else 'restaurant'
        constraints={k.split('.')[1]:v for k,v in values.items() if k.startswith(domain+'.')}
        matches=[row.get('name','unnamed') for row in databases[domain]
                 if all(normalize(row.get(k,''))==normalize(v) for k,v in constraints.items())]
        return dict(kind='database_shortlist',constraints=constraints,matches=sorted(matches))
    if role=='budget_brief':
        return dict(kind='categorical_budget_brief',bands=values,
                    ordinal_bands={k:{'cheap':1,'moderate':2,'expensive':3}.get(v) for k,v in values.items()},
                    units='Source categories, not currency or actual travel cost')
    if role=='location_brief':
        return dict(kind='location_brief',areas=values,same_area=len(set(values.values()))==1)
    if role=='stay_specification':return dict(kind='accommodation_requirements',requirements=values)
    return dict(kind='itinerary_requirements',requirements=values,
                authority='Planning preferences only; no booking permission')

