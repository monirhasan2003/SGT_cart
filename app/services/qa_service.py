"""Q&A service — Phase 15 Chunk D-2.

Public questions + answers attached to a product. The seller of the
product gets a notification when a customer asks; the asker gets a
notification when someone answers. Answer bodies are phone-guarded via
`policy_service` (surface=qa) — seller violations log + trip the
auto-suspend threshold.
"""
from app.extensions import db
from app.models.notification import NOTIF_PRODUCT
from app.models.policy import SURFACE_QA
from app.models.qa import Question, Answer, AnswerVote
from app.services.notification_service import notify
from app.services import policy_service
from app.utils.phone_guard import redact_phone_numbers


QUESTION_MAX = 500
ANSWER_MAX = 1000


def _truncate(text, limit):
    text = (text or "").strip()
    return text[:limit] if text else text


def ask_question(user, product, body):
    """Customer (or any user) asks a public question about a product.

    Returns ``(Question, None)`` on success or ``(None, error_str)``. Asker
    bodies are redacted (no user logging needed; only sellers can be
    auto-suspended) — but redaction protects the public surface either way.
    """
    body = _truncate(body, QUESTION_MAX)
    if not body:
        return None, "Question cannot be empty."

    # Redact (asker is usually a customer; if a seller asks on another
    # seller's product they get logged via policy_service).
    clean, flagged, _ = policy_service.redact_and_log(
        user, body, SURFACE_QA, ref_kind="question",
    )
    question = Question(
        product_id=product.id, asker_id=user.id, body=clean,
        is_public=True, is_flagged=flagged,
    )
    db.session.add(question)
    db.session.flush()

    # Notify the product's seller so they can answer.
    if product.vendor is not None and product.vendor.user_id != user.id:
        notify(
            product.vendor.user_id, NOTIF_PRODUCT,
            "New question on your product",
            f"{user.name} asked: '{clean[:120]}'",
            url=f"/product/{product.slug}/#qa",
        )
    db.session.commit()
    return question, None


def post_answer(user, question, body):
    """A logged-in user answers a question.

    The product's own seller gets a "Seller" badge on their answer.
    Returns ``(Answer, None)`` on success or ``(None, error_str)``.
    """
    body = _truncate(body, ANSWER_MAX)
    if not body:
        return None, "Answer cannot be empty."

    product = question.product
    is_seller_answer = (
        product is not None
        and product.vendor is not None
        and product.vendor.user_id == user.id
    )

    clean, flagged, _ = policy_service.redact_and_log(
        user, body, SURFACE_QA, ref_kind="answer", ref_id=question.id,
    )
    answer = Answer(
        question_id=question.id, responder_id=user.id, body=clean,
        is_seller_answer=is_seller_answer, is_flagged=flagged,
    )
    db.session.add(answer)
    db.session.flush()

    # Notify the asker (unless they answered their own question).
    if question.asker_id and question.asker_id != user.id:
        title = "Your question got an answer"
        if is_seller_answer:
            title = "Seller answered your question"
        notify(
            question.asker_id, NOTIF_PRODUCT, title,
            clean[:160],
            url=f"/product/{product.slug}/#qa" if product else None,
        )
    db.session.commit()
    return answer, None


def public_questions(product):
    """All public questions on a product, newest first."""
    return (
        Question.query.filter_by(product_id=product.id, is_public=True)
        .order_by(Question.id.desc()).all()
    )


def toggle_helpful(user, answer):
    """Toggle the helpful vote of `user` on `answer` (Phase 15 D-8 C6).

    Returns ``(now_voted, helpful_count)``. Self-vote is disallowed —
    a responder can't upvote their own answer.
    """
    if answer is None or user is None:
        return False, getattr(answer, "helpful_count", 0)
    if answer.responder_id == user.id:
        return False, answer.helpful_count

    existing = AnswerVote.query.filter_by(
        answer_id=answer.id, user_id=user.id
    ).first()
    if existing is None:
        db.session.add(AnswerVote(answer_id=answer.id, user_id=user.id))
        answer.helpful_count = (answer.helpful_count or 0) + 1
        db.session.commit()
        return True, answer.helpful_count
    db.session.delete(existing)
    answer.helpful_count = max(0, (answer.helpful_count or 0) - 1)
    db.session.commit()
    return False, answer.helpful_count


def voted_answer_ids(user, product):
    """Set of answer-ids on this product that `user` already voted helpful."""
    if user is None or getattr(user, "id", None) is None:
        return set()
    rows = (
        db.session.query(AnswerVote.answer_id)
        .join(Answer, Answer.id == AnswerVote.answer_id)
        .join(Question, Question.id == Answer.question_id)
        .filter(Question.product_id == product.id,
                AnswerVote.user_id == user.id).all()
    )
    return {row[0] for row in rows}


def answered_count(product):
    """How many of the product's questions have at least one answer."""
    return (
        Question.query.join(Answer, Answer.question_id == Question.id)
        .filter(Question.product_id == product.id, Question.is_public.is_(True))
        .distinct().count()
    )
