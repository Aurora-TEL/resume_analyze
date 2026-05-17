from copy import deepcopy

from app.models.enums import PromptScene


RESUME_PARSE_DEFAULT = {
    "schema_version": "1.0",
    "basic_info": {
        "name": None,
        "gender": None,
        "email": None,
        "phone": None,
        "location": None,
        "target_position": None,
        "work_years": None,
        "personal_website": None,
        "github": None,
        "linkedin": None,
    },
    "education": [],
    "work_experience": [],
    "project_experience": [],
    "skills": {
        "programming_languages": [],
        "frameworks": [],
        "databases": [],
        "tools": [],
        "cloud_or_devops": [],
        "domain_skills": [],
        "soft_skills": [],
        "other_skills": [],
    },
    "certificates": [],
    "awards": [],
    "languages": [],
    "self_evaluation": None,
    "other_sections": [],
    "parse_quality": {
        "is_readable": True,
        "missing_core_sections": [],
        "possible_parse_errors": [],
        "confidence": 0.0,
    },
}

JOB_PARSE_DEFAULT = {
    "schema_version": "1.0",
    "job_basic_info": {
        "title": None,
        "company_name": None,
        "industry": None,
        "location": None,
        "salary_range": None,
        "seniority_level": None,
        "employment_type": None,
    },
    "core_responsibilities": [],
    "required_skills": [],
    "preferred_skills": [],
    "technical_skills": {
        "programming_languages": [],
        "frameworks": [],
        "databases": [],
        "tools": [],
        "cloud_or_devops": [],
        "testing": [],
        "other": [],
    },
    "soft_skills": [],
    "experience_requirement": {
        "years_min": None,
        "years_max": None,
        "description": None,
    },
    "education_requirement": {
        "degree": None,
        "major": None,
        "description": None,
    },
    "industry_background_requirement": [],
    "certification_requirement": [],
    "keywords": [],
    "priority_weights": {
        "skills": 0.35,
        "experience": 0.25,
        "projects": 0.20,
        "education": 0.10,
        "soft_skills": 0.10,
    },
    "parse_quality": {
        "is_complete_jd": True,
        "missing_sections": [],
        "confidence": 0.0,
    },
}

FULL_ANALYSIS_DEFAULT = {
    "schema_version": "1.0",
    "total_score": 0,
    "match_score": 0,
    "summary": "",
    "score_breakdown": {
        "completeness": 0,
        "structure": 0,
        "professional_expression": 0,
        "experience_quality": 0,
        "skill_match": 0,
        "quantified_results": 0,
    },
    "match_breakdown": {
        "skill_match": 0,
        "work_experience_match": 0,
        "project_experience_match": 0,
        "industry_background_match": 0,
        "keyword_coverage_match": 0,
        "soft_skill_education_match": 0,
    },
    "strengths": [],
    "weaknesses": [],
    "keyword_analysis": {
        "coverage_rate": 0,
        "matched_keywords": [],
        "missing_keywords": [],
        "partially_covered_keywords": [],
        "keyword_suggestions": [],
    },
    "matched_requirements": [],
    "missing_requirements": [],
    "risk_items": [],
    "suggestions": [],
    "rewrite_examples": [],
    "next_actions": [],
    "risk_notes": [],
}

SCENE_DEFAULTS = {
    PromptScene.RESUME_PARSE.value: RESUME_PARSE_DEFAULT,
    PromptScene.JOB_PARSE.value: JOB_PARSE_DEFAULT,
    PromptScene.FULL_ANALYSIS.value: FULL_ANALYSIS_DEFAULT,
}


def _merge_defaults(defaults: dict, payload: dict) -> dict:
    result = deepcopy(defaults)
    for key, value in payload.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge_defaults(result[key], value)
        else:
            result[key] = value
    return result


def _clamp(value: int | float | None, minimum: int, maximum: int) -> int:
    try:
        numeric = float(value if value is not None else minimum)
    except (TypeError, ValueError):
        numeric = minimum
    return max(minimum, min(maximum, round(numeric)))


def validate_scene_payload(scene: str, payload: dict) -> dict:
    if scene not in SCENE_DEFAULTS:
        return payload

    merged = _merge_defaults(SCENE_DEFAULTS[scene], payload)
    merged["schema_version"] = str(merged.get("schema_version") or "1.0")

    if scene == PromptScene.RESUME_PARSE.value:
        confidence = merged["parse_quality"].get("confidence", 0.0)
        try:
            merged["parse_quality"]["confidence"] = max(0.0, min(1.0, float(confidence)))
        except (TypeError, ValueError):
            merged["parse_quality"]["confidence"] = 0.0

    if scene == PromptScene.JOB_PARSE.value:
        confidence = merged["parse_quality"].get("confidence", 0.0)
        try:
            merged["parse_quality"]["confidence"] = max(0.0, min(1.0, float(confidence)))
        except (TypeError, ValueError):
            merged["parse_quality"]["confidence"] = 0.0

    if scene == PromptScene.FULL_ANALYSIS.value:
        merged["total_score"] = _clamp(merged.get("total_score"), 0, 100)
        merged["match_score"] = _clamp(merged.get("match_score"), 0, 100)
        max_scores = {
            "completeness": 20,
            "structure": 15,
            "professional_expression": 20,
            "experience_quality": 20,
            "skill_match": 15,
            "quantified_results": 10,
        }
        recomputed = 0
        for key, max_score in max_scores.items():
            merged["score_breakdown"][key] = _clamp(merged["score_breakdown"].get(key), 0, max_score)
            recomputed += merged["score_breakdown"][key]
        merged["total_score"] = recomputed

        for key in list(merged["match_breakdown"].keys()):
            merged["match_breakdown"][key] = _clamp(merged["match_breakdown"].get(key), 0, 100)

        coverage = merged["keyword_analysis"].get("coverage_rate", 0)
        merged["keyword_analysis"]["coverage_rate"] = _clamp(coverage, 0, 100)
        if not merged["risk_notes"]:
            merged["risk_notes"] = [
                "Only add skills, experience, projects, and metrics that are true and verifiable.",
            ]

    return merged
