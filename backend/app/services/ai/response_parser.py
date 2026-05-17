import json
import re


def strip_markdown_code_fence(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()
    return cleaned


def extract_json_payload(text: str) -> str:
    cleaned = strip_markdown_code_fence(text)
    try:
        json.loads(cleaned)
        return cleaned
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidate = cleaned[start : end + 1]
            json.loads(candidate)
            return candidate
        raise


def parse_json_response(text: str) -> dict:
    payload = extract_json_payload(text)
    data = json.loads(payload)
    if not isinstance(data, dict):
        raise ValueError("AI response root must be an object")
    return data
