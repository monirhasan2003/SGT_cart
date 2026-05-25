"""Platform settings & audit log — Phase 6."""
from datetime import datetime

from app.extensions import db


class Setting(db.Model):
    """Key/value store for admin-configurable platform settings."""

    __tablename__ = "settings"

    key = db.Column(db.String(60), primary_key=True)
    value = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Setting {self.key}={self.value}>"


class AuditLog(db.Model):
    """A record of a significant admin action."""

    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    actor_name = db.Column(db.String(120))      # snapshot
    action = db.Column(db.String(120), nullable=False)
    target = db.Column(db.String(160))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    actor = db.relationship("User")

    def __repr__(self):
        return f"<AuditLog {self.action} by {self.actor_name}>"
