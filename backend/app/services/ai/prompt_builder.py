import json
from string import Template

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.enums import PromptScene, PromptTemplateStatus
from app.models.prompt_template import PromptTemplate

FALLBACK_TEMPLATES: dict[str, str] = {
    PromptScene.RESUME_PARSE.value: """
You are an expert resume parsing assistant.
Extract structured data from the resume text and return valid JSON only.

Rules:
1. Use only information that appears in the resume text.
2. If a field is missing, return null, an empty string, or an empty array as appropriate.
3. Do not return Markdown or explanations.
4. Keep all text content in the original language found in the resume when possible.

Return this JSON structure:
{
  "schema_version": "1.0",
  "basic_info": {
    "name": null,
    "gender": null,
    "email": null,
    "phone": null,
    "location": null,
    "target_position": null,
    "work_years": null,
    "personal_website": null,
    "github": null,
    "linkedin": null
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
    "other_skills": []
  },
  "certificates": [],
  "awards": [],
  "languages": [],
  "self_evaluation": null,
  "other_sections": [],
  "parse_quality": {
    "is_readable": true,
    "missing_core_sections": [],
    "possible_parse_errors": [],
    "confidence": 0.0
  }
}

Resume text:
$resume_text

Target position (optional):
$target_position
""".strip(),
    PromptScene.JOB_PARSE.value: """
You are an expert job description parsing assistant.
Extract structured requirements from the job description and return valid JSON only.

Rules:
1. Use only information that appears in the provided text.
2. If a field is missing, return null, an empty string, or an empty array as appropriate.
3. Do not return Markdown or explanations.
4. Keep all text content in the original language found in the job description when possible.

Return this JSON structure:
{
  "schema_version": "1.0",
  "job_basic_info": {
    "title": null,
    "company_name": null,
    "industry": null,
    "location": null,
    "salary_range": null,
    "seniority_level": null,
    "employment_type": null
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
    "other": []
  },
  "soft_skills": [],
  "experience_requirement": {
    "years_min": null,
    "years_max": null,
    "description": null
  },
  "education_requirement": {
    "degree": null,
    "major": null,
    "description": null
  },
  "industry_background_requirement": [],
  "certification_requirement": [],
  "keywords": [],
  "priority_weights": {
    "skills": 0.35,
    "experience": 0.25,
    "projects": 0.20,
    "education": 0.10,
    "soft_skills": 0.10
  },
  "parse_quality": {
    "is_complete_jd": true,
    "missing_sections": [],
    "confidence": 0.0
  }
}

Job title:
$job_title

Company name:
$company_name

Industry:
$industry

Job description:
$job_text
""".strip(),
    PromptScene.FULL_ANALYSIS.value: """
You are an expert resume reviewer and job matching assistant.
Compare the resume against the target job description and return valid JSON only.

Rules:
1. Base every conclusion on the supplied resume and job description.
2. Do not invent skills, experiences, projects, certifications, or metrics.
3. Give actionable suggestions that the candidate can honestly apply.
4. Do not return Markdown or explanations outside the JSON.
5. Keep all text content in the original language found in the input when possible.

Return this JSON structure:
{
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
    "quantified_results": 0
  },
  "match_breakdown": {
    "skill_match": 0,
    "work_experience_match": 0,
    "project_experience_match": 0,
    "industry_background_match": 0,
    "keyword_coverage_match": 0,
    "soft_skill_education_match": 0
  },
  "strengths": [],
  "weaknesses": [],
  "keyword_analysis": {
    "coverage_rate": 0,
    "matched_keywords": [],
    "missing_keywords": [],
    "partially_covered_keywords": [],
    "keyword_suggestions": []
  },
  "matched_requirements": [],
  "missing_requirements": [],
  "risk_items": [],
  "suggestions": [],
  "rewrite_examples": [],
  "next_actions": [],
  "risk_notes": []
}

Structured resume data:
$resume_structured_data

Resume text:
$resume_text

Structured job data:
$job_structured_data

Job description:
$job_text
""".strip(),
}


def select_prompt_template(db: Session | None, scene: str) -> PromptTemplate | None:
    if db is None:
        return None

    return db.scalar(
        select(PromptTemplate)
        .where(
            PromptTemplate.scene == scene,
            PromptTemplate.status == PromptTemplateStatus.ACTIVE,
        )
        .order_by(desc(PromptTemplate.version))
        .limit(1)
    )


def build_prompt(db: Session | None, scene: str, variables: dict) -> tuple[str, str, str | None]:
    template_record = select_prompt_template(db, scene)
    template_text = template_record.content if template_record else FALLBACK_TEMPLATES[scene]
    prompt = Template(template_text).safe_substitute(
        {
            key: json.dumps(value, ensure_ascii=False, indent=2) if isinstance(value, (dict, list)) else (value or "")
            for key, value in variables.items()
        }
    )
    return prompt, template_record.id if template_record else None, template_record.name if template_record else "fallback"
