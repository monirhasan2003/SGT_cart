"""Pre-set quick-question buttons for the product page — Phase 15 D-7 C4.

Static bilingual list. One-tap buttons next to "Chat Now" send the
canonical question as a chat message via `POST /messages/quick-question`.
The keys are stable identifiers; the templates and the route only know
about these keys, so the wording can change without breaking links.
"""

QUICK_QUESTIONS = [
    {
        "key": "delivery_time",
        "label_en": "Delivery time?",
        "label_bn": "ডেলিভারি কত দিনে?",
        "body": "Hi, how long will delivery take?",
    },
    {
        "key": "original",
        "label_en": "Is it original?",
        "label_bn": "Original কি?",
        "body": "Is this product original / authentic?",
    },
    {
        "key": "warranty",
        "label_en": "Warranty?",
        "label_bn": "Warranty আছে?",
        "body": "Does this product come with a warranty?",
    },
    {
        "key": "stock",
        "label_en": "In stock?",
        "label_bn": "Stock আছে?",
        "body": "Is this product currently in stock?",
    },
]

_BY_KEY = {q["key"]: q for q in QUICK_QUESTIONS}


def question_body(key):
    """Resolve a quick-question key to its canonical message body."""
    q = _BY_KEY.get(key)
    return q["body"] if q else None
