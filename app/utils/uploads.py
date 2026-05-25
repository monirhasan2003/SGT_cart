"""File upload helpers.

Uploaded files are stored under `app/static/uploads/<subdir>/` and referenced
by a path relative to the static folder, e.g. `uploads/vendor_docs/<uuid>.pdf`.
"""
import os
import uuid

from flask import current_app

try:
    from PIL import Image, ImageOps
    _PIL_OK = True
except ImportError:
    _PIL_OK = False

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


def save_image_upload(file_storage, subdir,
                      max_width=1600, max_height=None,
                      quality=85, prefer_jpeg=True):
    """Save an uploaded image, resized + recompressed to a sane size.

    Admins routinely upload 5–10 MB photos straight from a camera or
    Figma export. For homepage banners, product thumbnails, etc. the
    display area is only ~1600px wide, so serving the original wastes
    bandwidth and slows first paint badly. This helper does, in order:

      1. Validate the extension (`ALLOWED_DOC_EXTENSIONS`).
      2. Open the image and apply EXIF orientation.
      3. If wider than `max_width` (or `max_height`, if given), downscale
         while preserving aspect ratio.
      4. Save as optimised JPEG (default) — much smaller than PNG for
         photos. PNGs with transparency are kept as PNG.
      5. Fall back to byte-for-byte save if Pillow is missing.

    Returns the static-relative path or None on failure.
    """
    if not has_file(file_storage):
        return None
    ext = _extension(file_storage.filename)
    if ext not in ALLOWED_DOC_EXTENSIONS:
        return None

    folder = os.path.join(current_app.config["UPLOAD_FOLDER"], subdir)
    os.makedirs(folder, exist_ok=True)

    if not _PIL_OK:
        # Conservative fallback so the upload still works without Pillow.
        fname = f"{uuid.uuid4().hex}.{ext}"
        file_storage.save(os.path.join(folder, fname))
        return f"uploads/{subdir}/{fname}"

    try:
        img = Image.open(file_storage.stream)
        img = ImageOps.exif_transpose(img)
    except Exception:
        return None

    has_alpha = img.mode in ("RGBA", "LA") or (
        img.mode == "P" and "transparency" in img.info)
    use_jpeg = prefer_jpeg and not has_alpha

    if use_jpeg and img.mode != "RGB":
        img = img.convert("RGB")

    # Downscale to the cap while preserving aspect ratio.
    w, h = img.size
    if max_width and w > max_width:
        h = int(h * (max_width / w))
        w = max_width
    if max_height and h > max_height:
        w = int(w * (max_height / h))
        h = max_height
    if (w, h) != img.size:
        img = img.resize((w, h), Image.LANCZOS)

    out_ext = "jpg" if use_jpeg else "png"
    fname = f"{uuid.uuid4().hex}.{out_ext}"
    out_path = os.path.join(folder, fname)
    save_kwargs = ({"format": "JPEG", "quality": quality, "optimize": True,
                    "progressive": True} if use_jpeg
                   else {"format": "PNG", "optimize": True})
    img.save(out_path, **save_kwargs)
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
