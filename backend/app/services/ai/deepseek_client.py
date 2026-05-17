from time import perf_counter
from uuid import UUID

import httpx
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.exceptions import AppException
from app.models.api_call_log import ApiCallLog
from app.models.enums import ApiCallStatus
from app.services.ai.prompt_builder import build_prompt
from app.services.ai.response_parser import parse_json_response
from app.services.ai.response_validator import validate_scene_payload

settings = get_settings()


class DeepSeekClient:
    def __init__(self) -> None:
        base_url = settings.deepseek_base_url.rstrip("/")
        self.chat_completions_url = f"{base_url}/chat/completions"

    def _build_headers(self) -> dict[str, str]:
        if not settings.deepseek_api_key:
            raise AppException(message="DeepSeek API key is not configured", code=5002, status_code=500)
        return {
            "Authorization": f"Bearer {settings.deepseek_api_key}",
            "Content-Type": "application/json",
        }

    def call_scene(
        self,
        db: Session | None,
        scene: str,
        variables: dict,
        *,
        user_id: UUID | None = None,
        task_id: UUID | None = None,
    ) -> dict:
        prompt, prompt_template_id, _ = build_prompt(db, scene, variables)
        payload = {
            "model": settings.deepseek_model,
            "messages": [
                {"role": "system", "content": "You are a precise JSON-only assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
        }

        started_at = perf_counter()
        log = ApiCallLog(
            user_id=user_id,
            task_id=task_id,
            prompt_template_id=prompt_template_id,
            provider="deepseek",
            model_name=settings.deepseek_model,
            scene=scene,
            request_length=len(prompt),
            status=ApiCallStatus.FAILED,
        )
        if db is not None:
            db.add(log)
            db.commit()
            db.refresh(log)

        try:
            with httpx.Client(timeout=settings.deepseek_timeout_seconds) as client:
                response = client.post(
                    self.chat_completions_url,
                    headers=self._build_headers(),
                    json=payload,
                )
                response.raise_for_status()
                response_json = response.json()

            content = response_json["choices"][0]["message"]["content"]
            parsed = parse_json_response(content)
            validated = validate_scene_payload(scene, parsed)

            usage = response_json.get("usage", {}) or {}
            if db is not None:
                log.response_length = len(content)
                log.prompt_tokens = usage.get("prompt_tokens")
                log.completion_tokens = usage.get("completion_tokens")
                log.total_tokens = usage.get("total_tokens")
                log.latency_ms = int((perf_counter() - started_at) * 1000)
                log.status = ApiCallStatus.SUCCESS
                log.request_id = response_json.get("id")
                db.add(log)
                db.commit()

            return validated
        except Exception as exc:  # noqa: BLE001
            if db is not None:
                log.status = ApiCallStatus.FAILED
                log.error_type = exc.__class__.__name__
                log.error_message = str(exc)
                log.latency_ms = int((perf_counter() - started_at) * 1000)
                db.add(log)
                db.commit()
            raise AppException(message=f"DeepSeek call failed for scene {scene}", code=5003, status_code=500, errors=str(exc)) from exc
