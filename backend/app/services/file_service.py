from pathlib import Path
from uuid import UUID, uuid4

from app.core.config import ROOT_DIR, get_settings

settings = get_settings()

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
ALLOWED_MIME_TYPES = {
    "pdf": {"application/pdf", "application/x-pdf", "application/octet-stream"},
    "docx": {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
        "application/octet-stream",
    },
    "txt": {"text/plain", "application/octet-stream", ""},
}


def get_upload_root() -> Path:
    upload_root = ROOT_DIR / settings.upload_dir
    upload_root.mkdir(parents=True, exist_ok=True)
    return upload_root


def detect_extension(filename: str) -> str:
    suffix = Path(filename).suffix.lower().lstrip(".")
    return suffix


def validate_resume_file(filename: str, content_type: str | None, file_size: int) -> str:
    extension = detect_extension(filename)
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type. Only PDF, DOCX, and TXT are allowed.")

    normalized_content_type = (content_type or "").lower()
    if normalized_content_type not in ALLOWED_MIME_TYPES[extension]:
        raise ValueError("Invalid file MIME type.")

    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if file_size > max_bytes:
        raise ValueError(f"File size exceeds {settings.max_upload_size_mb} MB limit.")

    return extension


def build_resume_storage_path(user_id: UUID, extension: str) -> tuple[Path, str]:
    relative_path = Path(str(user_id)) / f"{uuid4()}.{extension}"
    absolute_path = get_upload_root() / relative_path
    absolute_path.parent.mkdir(parents=True, exist_ok=True)
    return absolute_path, str(Path(settings.upload_dir) / relative_path).replace("\\", "/")


def write_file(absolute_path: Path, content: bytes) -> None:
    absolute_path.write_bytes(content)
