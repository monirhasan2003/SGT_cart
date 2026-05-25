"""File upload helpers.

Uploaded files are stored under `app/static/uploads/<subdir>/` and referenced
by a path relative to the static folder, e.g. `uploads/vendor_docs/<uuid>.pdf`.
"""
import os
import uuid

from flask import current_app

ALLOWED_DOC_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}
# Phase 15 D-7 — chat voice messages.
ALLOWED_AUDIO_EXTENSIONS = {"mp3", "ogg", "wav", "webm", "m4a"}
# Conservative cap so a malicious browser can't upload a multi-megabyte
# recording. ~5 MB covers a few minutes of compressed audio.
MAX_AUDIO_BYTES = 5 * 1024 * 1024


def _extension(filename):
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def is_allowed_doc(filename):
    """True if the filename has an allowed document/image extension."""
    return _extension(filename) in ALLOWED_DOC_EXTENSIONS


def has_file(file_storage):
    """True if a non-empty file was actually uploaded."""
    return bool(file_storage and file_storage.filename)


def save_upload(file_storage, subdir):
    """Save an uploaded file under static/uploads/<subdir>/.

    Returns the path relative to the `static` folder (usable with
    `url_for('static', filename=...)`), or None if there is no valid file.
    """
    if not has_file(file_storage):
        return None
    ext = _extension(file_storage.filename)
    if ext not in ALLOWED_DOC_EXTENSIONS:
        return None
    folder = os.path.join(current_app.config["UPLOAD_FOLDER"], subdir)
    os.makedirs(folder, exist_ok=True)
    fname = f"{uuid.uuid4().hex}.{ext}"
    file_storage.save(os.path.join(folder, fname))
    return f"uploads/{subdir}/{fname}"


def save_audio_upload(file_storage, subdir):
    """Save a chat voice-message audio file (Phase 15 D-7 C5).

    Same return shape as `save_upload`: a static-relative path, or None.
    Rejects unknown extensions and oversized files (`MAX_AUDIO_BYTES`).
    """
    if not has_file(file_storage):
        return None
    ext = _extension(file_storage.filename)
    if ext not in ALLOWED_AUDIO_EXTENSIONS:
        return None
    # Check size without consuming the stream.
    file_storage.stream.seek(0, os.SEEK_END)
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)
    if size > MAX_AUDIO_BYTES or size <= 0:
        return None
    folder = os.path.join(current_app.config["UPLOAD_FOLDER"], subdir)
    os.makedirs(folder, exist_ok=True)
    fname = f"{uuid.uuid4().hex}.{ext}"
    file_storage.save(os.path.join(folder, fname))
    return f"uploads/{subdir}/{fname}"
