"""Public Question & Answer models — Phase 15 D-2.

Any logged-in customer can ask a public question on a published product.
The product's seller — or any other logged-in user — can post an answer.
Answer bodies are phone-guarded via `policy_service` (surface=`qa`), so a
seller who repeatedly tries to leak contact info gets auto-suspended on
the second strike (see [[marketplace-feature-rules]]).

Helpful-vote on answers comes later (D-8 follow-on).
"""
from datetime import datetime

from app.extensions import db


class Question(db.Model):
    """One customer-asked question pinned to a product."""

    __tablename__ = "qa_questions"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False, index=True
    )
    asker_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    body = db.Column(db.String(500), nullable=False)
    is_public = db.Column(db.Boolean, nullable=False, default=True, index=True)
    # True when the phone-number guard had to redact something on the way in.
    is_flagged = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    product = db.relationship(
        "Product", backref=db.backref("questions", cascade="all, delete-orphan"),
    )
    asker = db.relationship("User")
    answers = db.relationship(
        "Answer", back_populates="question",
        cascade="all, delete-orphan", order_by="Answer.id",
    )

    @property
    def answer_count(self):
        return len(self.answers)

    def __repr__(self):
        return f"<Question {self.id} product={self.product_id}>"


class Answer(db.Model):
    """One reply to a question. Sellers and customers can both answer."""

    __tablename__ = "qa_answers"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(
        db.Integer, db.ForeignKey("qa_questions.id"), nullable=False, index=True
    )
    responder_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    body = db.Column(db.String(1000), nullable=False)
    # True when this answer came from the product's own seller (snapshot at
    # creation — keeps the "Seller" badge stable even if the user role changes).
    is_seller_answer = db.Column(db.Boolean, nullable=False, default=False)
    # True when the phone-number guard redacted something.
    is_flagged = db.Column(db.Boolean, nullable=False, default=False)
    # Phase 15 D-8 C6 — denormalized count of helpful votes; the source of
    # truth is `AnswerVote`. Stored so the listing can sort without a JOIN.
    helpful_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    question = db.relationship("Question", back_populates="answers")
    responder = db.relationship("User")
    votes = db.relationship(
        "AnswerVote", back_populates="answer", cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Answer {self.id} question={self.question_id}>"


class AnswerVote(db.Model):
    """One helpful-vote on an answer — Phase 15 D-8 C6.

    Unique on (answer_id, user_id) — one vote per user per answer; the
    toggle endpoint deletes the row to "un-helpful". The denormalized
    `Answer.helpful_count` is updated by `qa_service.toggle_helpful`.
    """

    __tablename__ = "qa_answer_votes"
    __table_args__ = (
        db.UniqueConstraint("answer_id", "user_id",
                            name="uq_answer_vote_answer_user"),
    )

    id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(
        db.Integer, db.ForeignKey("qa_answers.id"), nullable=False, index=True
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    answer = db.relationship("Answer", back_populates="votes")
    user = db.relationship("User")

    def __repr__(self):
        return f"<AnswerVote answer={self.answer_id} user={self.user_id}>"
