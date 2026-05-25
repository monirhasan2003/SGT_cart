"""Phone-number guard for chat — Phase 8.

Marketplace rule: sellers must never share or display phone numbers in chat,
so deals stay on the platform. Before any chat message is stored we redact
digit sequences that look like a phone number (10+ digits, even when broken
up by spaces, dashes or dots to disguise them).
"""
import re

# A run of digits, optionally split by spaces / dashes / dots / parentheses —
# the usual ways people disguise a phone number in a chat message.
_NUMBER_RUN = re.compile(r"\+?\d[\d\s().\-]{7,}\d")
_DIGIT = re.compile(r"\d")

# Minimum digits for a run to count as a phone number (BD numbers are 11).
_MIN_DIGITS = 10
REDACTION = "[number removed]"


def _is_phone_like(fragment):
    return len(_DIGIT.findall(fragment)) >= _MIN_DIGITS


def contains_phone_number(text):
    """True when `text` contains something that looks like a phone number."""
    return any(_is_phone_like(m.group()) for m in _NUMBER_RUN.finditer(text or ""))


def redact_phone_numbers(text):
    """Strip phone-number-like runs from `text`.

    Returns ``(clean_text, was_redacted)``.
    """
    if not text:
        return text, False

    redacted = False

    def _replace(match):
        nonlocal redacted
        if _is_phone_like(match.group()):
            redacted = True
            return REDACTION
        return match.group()

    return _NUMBER_RUN.sub(_replace, text), redacted
