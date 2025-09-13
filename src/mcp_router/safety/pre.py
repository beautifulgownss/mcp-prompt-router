import re

EMAIL_RE = re.compile(r"([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
PHONE_RE = re.compile(r"\b(\+?\d[\d\-\s]{7,}\d)\b")

def mask_pii(text: str) -> str:
    if not text:
        return text
    text = EMAIL_RE.sub(r"***@***", text)
    text = PHONE_RE.sub("***-***-****", text)
    return text
