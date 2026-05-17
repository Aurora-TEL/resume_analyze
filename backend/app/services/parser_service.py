import re
from pathlib import Path

from docx import Document
from pypdf import PdfReader


def parse_txt(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8", errors="ignore").strip()


def parse_docx(file_path: Path) -> str:
    document = Document(file_path)
    paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]
    return "\n".join(paragraphs).strip()


def parse_pdf(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    contents: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        text = text.strip()
        if text:
            contents.append(text)
    return "\n\n".join(contents).strip()


def extract_text(file_path: Path, file_type: str) -> str:
    if file_type == "txt":
        return parse_txt(file_path)
    if file_type == "docx":
        return parse_docx(file_path)
    if file_type == "pdf":
        return parse_pdf(file_path)
    raise ValueError("Unsupported file type for parsing")


def build_structured_resume_data(raw_text: str) -> dict:
    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw_text)
    phone_match = re.search(r"(?<!\d)(1\d{10})(?!\d)", raw_text)

    known_skills = [
        "Python",
        "FastAPI",
        "PostgreSQL",
        "SQLAlchemy",
        "Docker",
        "Redis",
        "Celery",
        "Vue",
        "TypeScript",
        "Java",
        "Go",
        "SQL",
    ]
    matched_skills = [skill for skill in known_skills if skill.lower() in raw_text.lower()]

    preview_lines = [line.strip() for line in raw_text.splitlines() if line.strip()][:8]

    return {
        "basic_info": {
            "email": email_match.group(0) if email_match else None,
            "phone": phone_match.group(1) if phone_match else None,
        },
        "skills": matched_skills,
        "preview_lines": preview_lines,
        "parser": "local_mvp_parser",
    }
