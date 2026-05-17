"""initial core tables

Revision ID: 20260517_0001
Revises:
Create Date: 2026-05-17 10:45:00
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "20260517_0001"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("nickname", sa.String(length=100), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("avatar_url", sa.String(length=500), nullable=True),
        sa.Column("target_position", sa.String(length=100), nullable=True),
        sa.Column("target_city", sa.String(length=100), nullable=True),
        sa.Column("work_years", sa.Numeric(4, 1), nullable=True),
        sa.Column("role", sa.String(length=30), nullable=False, server_default="user"),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="active"),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("idx_users_status", "users", ["status"])
    op.create_index("idx_users_created_at", "users", ["created_at"])

    op.create_table(
        "resumes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("file_type", sa.String(length=20), nullable=False),
        sa.Column("file_size", sa.BigInteger(), nullable=False),
        sa.Column("file_path", sa.String(length=500), nullable=False),
        sa.Column("raw_text", sa.Text(), nullable=True),
        sa.Column("structured_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("parse_status", sa.String(length=30), nullable=False, server_default="pending"),
        sa.Column("parse_error", sa.Text(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default=sa.text("FALSE")),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_index("idx_resumes_user_id", "resumes", ["user_id"])
    op.create_index("idx_resumes_status", "resumes", ["status"])
    op.create_index("idx_resumes_created_at", "resumes", ["created_at"])
    op.create_index("idx_resumes_structured_data", "resumes", ["structured_data"], postgresql_using="gin")

    op.create_table(
        "job_descriptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("company_name", sa.String(length=200), nullable=True),
        sa.Column("industry", sa.String(length=100), nullable=True),
        sa.Column("location", sa.String(length=100), nullable=True),
        sa.Column("salary_range", sa.String(length=100), nullable=True),
        sa.Column("description_text", sa.Text(), nullable=False),
        sa.Column("structured_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("parse_status", sa.String(length=30), nullable=False, server_default="pending"),
        sa.Column("parse_error", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_index("idx_job_descriptions_user_id", "job_descriptions", ["user_id"])
    op.create_index("idx_job_descriptions_status", "job_descriptions", ["status"])
    op.create_index("idx_job_descriptions_created_at", "job_descriptions", ["created_at"])
    op.create_index("idx_job_descriptions_structured_data", "job_descriptions", ["structured_data"], postgresql_using="gin")

    op.create_table(
        "analysis_tasks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("resume_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("job_description_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("task_type", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="pending"),
        sa.Column("progress", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("retry_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.CheckConstraint("progress >= 0 AND progress <= 100", name="ck_analysis_tasks_progress_range"),
        sa.ForeignKeyConstraint(["job_description_id"], ["job_descriptions.id"]),
        sa.ForeignKeyConstraint(["resume_id"], ["resumes.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_index("idx_analysis_tasks_user_id", "analysis_tasks", ["user_id"])
    op.create_index("idx_analysis_tasks_resume_id", "analysis_tasks", ["resume_id"])
    op.create_index("idx_analysis_tasks_status", "analysis_tasks", ["status"])
    op.create_index("idx_analysis_tasks_created_at", "analysis_tasks", ["created_at"])
    op.create_index("idx_analysis_tasks_user_status", "analysis_tasks", ["user_id", "status"])

    op.create_table(
        "prompt_templates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("scene", sa.String(length=100), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="active"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
    )
    op.create_index("idx_prompt_templates_scene", "prompt_templates", ["scene"])
    op.create_index("idx_prompt_templates_status", "prompt_templates", ["status"])
    op.create_index("idx_prompt_templates_scene_version", "prompt_templates", ["scene", "version"])

    op.create_table(
        "analysis_reports",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("task_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("resume_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("job_description_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("total_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("match_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("report_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("model_provider", sa.String(length=50), nullable=False),
        sa.Column("model_name", sa.String(length=100), nullable=False),
        sa.Column("report_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.ForeignKeyConstraint(["job_description_id"], ["job_descriptions.id"]),
        sa.ForeignKeyConstraint(["resume_id"], ["resumes.id"]),
        sa.ForeignKeyConstraint(["task_id"], ["analysis_tasks.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.UniqueConstraint("task_id", name="uq_analysis_reports_task_id"),
    )
    op.create_index("idx_analysis_reports_user_id", "analysis_reports", ["user_id"])
    op.create_index("idx_analysis_reports_resume_id", "analysis_reports", ["resume_id"])
    op.create_index("idx_analysis_reports_created_at", "analysis_reports", ["created_at"])
    op.create_index("idx_analysis_reports_report_data", "analysis_reports", ["report_data"], postgresql_using="gin")

    op.create_table(
        "api_call_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("task_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("prompt_template_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("model_name", sa.String(length=100), nullable=False),
        sa.Column("scene", sa.String(length=100), nullable=False),
        sa.Column("request_length", sa.Integer(), nullable=True),
        sa.Column("response_length", sa.Integer(), nullable=True),
        sa.Column("prompt_tokens", sa.Integer(), nullable=True),
        sa.Column("completion_tokens", sa.Integer(), nullable=True),
        sa.Column("total_tokens", sa.Integer(), nullable=True),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("error_type", sa.String(length=100), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("request_id", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.ForeignKeyConstraint(["prompt_template_id"], ["prompt_templates.id"]),
        sa.ForeignKeyConstraint(["task_id"], ["analysis_tasks.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_index("idx_api_call_logs_user_id", "api_call_logs", ["user_id"])
    op.create_index("idx_api_call_logs_task_id", "api_call_logs", ["task_id"])
    op.create_index("idx_api_call_logs_scene", "api_call_logs", ["scene"])
    op.create_index("idx_api_call_logs_status", "api_call_logs", ["status"])
    op.create_index("idx_api_call_logs_created_at", "api_call_logs", ["created_at"])


def downgrade() -> None:
    op.drop_index("idx_api_call_logs_created_at", table_name="api_call_logs")
    op.drop_index("idx_api_call_logs_status", table_name="api_call_logs")
    op.drop_index("idx_api_call_logs_scene", table_name="api_call_logs")
    op.drop_index("idx_api_call_logs_task_id", table_name="api_call_logs")
    op.drop_index("idx_api_call_logs_user_id", table_name="api_call_logs")
    op.drop_table("api_call_logs")

    op.drop_index("idx_analysis_reports_report_data", table_name="analysis_reports", postgresql_using="gin")
    op.drop_index("idx_analysis_reports_created_at", table_name="analysis_reports")
    op.drop_index("idx_analysis_reports_resume_id", table_name="analysis_reports")
    op.drop_index("idx_analysis_reports_user_id", table_name="analysis_reports")
    op.drop_table("analysis_reports")

    op.drop_index("idx_prompt_templates_scene_version", table_name="prompt_templates")
    op.drop_index("idx_prompt_templates_status", table_name="prompt_templates")
    op.drop_index("idx_prompt_templates_scene", table_name="prompt_templates")
    op.drop_table("prompt_templates")

    op.drop_index("idx_analysis_tasks_user_status", table_name="analysis_tasks")
    op.drop_index("idx_analysis_tasks_created_at", table_name="analysis_tasks")
    op.drop_index("idx_analysis_tasks_status", table_name="analysis_tasks")
    op.drop_index("idx_analysis_tasks_resume_id", table_name="analysis_tasks")
    op.drop_index("idx_analysis_tasks_user_id", table_name="analysis_tasks")
    op.drop_table("analysis_tasks")

    op.drop_index("idx_job_descriptions_structured_data", table_name="job_descriptions", postgresql_using="gin")
    op.drop_index("idx_job_descriptions_created_at", table_name="job_descriptions")
    op.drop_index("idx_job_descriptions_status", table_name="job_descriptions")
    op.drop_index("idx_job_descriptions_user_id", table_name="job_descriptions")
    op.drop_table("job_descriptions")

    op.drop_index("idx_resumes_structured_data", table_name="resumes", postgresql_using="gin")
    op.drop_index("idx_resumes_created_at", table_name="resumes")
    op.drop_index("idx_resumes_status", table_name="resumes")
    op.drop_index("idx_resumes_user_id", table_name="resumes")
    op.drop_table("resumes")

    op.drop_index("idx_users_created_at", table_name="users")
    op.drop_index("idx_users_status", table_name="users")
    op.drop_table("users")
