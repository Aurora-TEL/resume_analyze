from enum import StrEnum


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"


class UserStatus(StrEnum):
    ACTIVE = "active"
    DISABLED = "disabled"
    DELETED = "deleted"


class ResourceStatus(StrEnum):
    ACTIVE = "active"
    DELETED = "deleted"


class ParseStatus(StrEnum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class TaskType(StrEnum):
    RESUME_SCORE = "resume_score"
    JOB_MATCH = "job_match"
    FULL_ANALYSIS = "full_analysis"


class TaskStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELED = "canceled"


class ApiCallStatus(StrEnum):
    SUCCESS = "success"
    FAILED = "failed"


class PromptTemplateStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"


class PromptScene(StrEnum):
    RESUME_PARSE = "resume_parse"
    JOB_PARSE = "job_parse"
    RESUME_SCORE = "resume_score"
    JOB_MATCH = "job_match"
    KEYWORD_ANALYSIS = "keyword_analysis"
    RESUME_SUGGESTION = "resume_suggestion"
    REWRITE_EXAMPLE = "rewrite_example"
    FULL_ANALYSIS = "full_analysis"
