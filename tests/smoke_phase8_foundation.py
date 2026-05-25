"""Phase 8 (Chunk A) smoke test — real-time foundation.

Verifies the SocketIO setup, the new chat / notification / device-token
models, and the chat phone-number guard.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase8_foundation.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db, socketio
from app.models.user import User
from app.models.chat import ChatThread, ChatMessage, CHAT_SUPPORT, CHAT_VENDOR
from app.models.notification import Notification, DeviceToken, NOTIF_CHAT
from app.utils.phone_guard import contains_phone_number, redact_phone_numbers

CUSTOMER = "smoke_p8_customer@example.com"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        u = User.query.filter_by(email=CUSTOMER).first()
        if u:
            # session.delete() per row so chat-message cascade fires.
            for t in ChatThread.query.filter_by(customer_id=u.id).all():
                db.session.delete(t)
            db.session.delete(u)   # cascades notifications + device tokens
            db.session.commit()


def main():
    app = create_app("development")
    purge(app)

    # ---- SocketIO wired up ----
    check("SocketIO initialised (threading mode)",
          socketio.async_mode == "threading")

    # ---- phone-number guard ----
    blocked = [
        "Call me at 01712345678",
        "my number is 017 1234 5678",
        "reach me 017-1234-5678 please",
        "+8801712345678",
        "0 1 7 1 2 3 4 5 6 7 8",
    ]
    allowed = [
        "Is this product available?",
        "Order SGT260523-ABCDE is late",
        "The price is 1500 taka",
        "Postal code 1207, please deliver fast",
    ]
    check("phone guard flags disguised numbers",
          all(contains_phone_number(t) for t in blocked))
    check("phone guard ignores prices / codes / order numbers",
          not any(contains_phone_number(t) for t in allowed))

    clean, redacted = redact_phone_numbers("Call me at 01712345678 today")
    check("phone guard redacts the number",
          redacted and "01712345678" not in clean and "[number removed]" in clean)

    clean, redacted = redact_phone_numbers("Is the red one in stock?")
    check("phone guard leaves clean text untouched",
          not redacted and clean == "Is the red one in stock?")

    # ---- models ----
    with app.app_context():
        u = User(name="P8 Customer", email=CUSTOMER, role="customer", is_active=True)
        u.set_password("test1234")
        db.session.add(u)
        db.session.flush()

        thread = ChatThread(kind=CHAT_SUPPORT, customer_id=u.id,
                            subject="Where is my order?")
        db.session.add(thread)
        db.session.flush()

        db.session.add(ChatMessage(thread_id=thread.id, sender_id=u.id,
                                   sender_role="customer", body="Hello, any update?"))
        db.session.add(Notification(user_id=u.id, kind=NOTIF_CHAT,
                                    title="New message", body="You have a reply."))
        db.session.add(DeviceToken(user_id=u.id, token="smoke-fcm-token-123",
                                   platform="android"))
        db.session.commit()

        thread = ChatThread.query.filter_by(customer_id=u.id).first()
        check("ChatThread + ChatMessage persisted",
              thread is not None and len(thread.messages) == 1)
        check("ChatThread.unread_count counts the other side",
              thread.unread_count(user_id=999) == 1
              and thread.unread_count(user_id=u.id) == 0)
        check("Notification persisted",
              Notification.query.filter_by(user_id=u.id).count() == 1)
        check("DeviceToken persisted",
              DeviceToken.query.filter_by(user_id=u.id, platform="android").count() == 1)
        check("chat kinds distinct", CHAT_SUPPORT != CHAT_VENDOR)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 8 foundation smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
