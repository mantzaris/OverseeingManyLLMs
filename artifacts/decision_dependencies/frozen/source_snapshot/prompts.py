"""Public-only prompts shared by all methods using extracted records."""
SLOTS = {'hotel': ['area', 'pricerange', 'stars', 'parking', 'internet', 'type'],
         'restaurant': ['area', 'pricerange', 'food']}

EXTRACT = '''You maintain a travel user's CURRENT preferences from a conversation.
Return JSON only: {"records":[{"domain":"hotel or restaurant","slot":"...","value":"...","turn":0,"quote":"exact short substring from a USER turn"}]}.
Allowed hotel slots: area, pricerange, stars, parking, internet, type.
Allowed restaurant slots: area, pricerange, food.
Extract only preferences actually stated or explicitly accepted by the user.
An assistant suggestion alone is not a user instruction. A booking approval is not general authority.
Use the most recent user instruction for each domain and slot. A restaurant preference must not automatically transfer to a hotel or vice versa. Follow explicit references such as "same area" using preceding context. If uncertain, omit the record; do not invent a value.
Normalize: centre/north/south/east/west, cheap/moderate/expensive, parking and internet yes/no, type hotel/guesthouse, stars digits. Cuisine is lower-case text. Omit no-preference or unknown fields.
Every record must cite its supporting USER turn and an exact short quote. Do not include old superseded records. Keep at most 9 records.'''

PARSE = '''Map each travel-planning request to the requested preference. Return JSON only: {"queries":[{"id":"same id","domain":"hotel or restaurant or unknown","slot":"..."}]}.
Allowed hotel slots: area, pricerange, stars, parking, internet, type. Allowed restaurant slots: area, pricerange, food.
Use only what the request says. Lodging/accommodation means hotel; dining/eating means restaurant. If a question is ambiguous, use unknown. Do not supply answers.'''

HISTORY = '''Answer travel agents' preference questions using only the user's current instructions in the supplied conversation. Respect changes, domain scope and explicit references. Do not treat an assistant suggestion as a user instruction. Return JSON only: {"answers":[{"id":"same id","value":"normalized answer or UNKNOWN"}]}. Normalize price cheap/moderate/expensive, area centre/north/south/east/west, parking/internet yes/no, stars digits, type hotel/guesthouse, cuisine lower-case. Do not guess an unstated preference.'''

MEMORY = '''Answer travel agents' preference questions using the supplied current shared memories. Select the memory that applies to the question's domain and requested attribute, not merely a similar word. Respect exceptions and updates. Return JSON only: {"answers":[{"id":"same id","value":"memory value or UNKNOWN"}]}. If no applicable memory exists, answer UNKNOWN. Do not invent a new instruction.'''

def dialogue_text(messages):
    return '\n'.join('%s %s: %s' % (t['turn'], t['role'].upper(), t['text']) for t in messages)

def extraction_messages(messages):
    return [{'role':'system', 'content':EXTRACT},
            {'role':'user', 'content':dialogue_text(messages)}]
