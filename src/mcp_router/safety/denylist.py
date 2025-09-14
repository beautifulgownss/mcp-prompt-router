import re
PATTERNS=[re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),re.compile(r'\b(?:\d[ -]*?){13,16}\b'),re.compile(r'(?i)\b(kill|bomb|harm)\b')]

def check_denylist(text:str)->list[str]:
    hits=[]
    if not text: return hits
    for p in PATTERNS:
        if p.search(text): hits.append(p.pattern)
    return hits
