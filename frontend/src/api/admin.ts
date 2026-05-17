import { del, get, post, put } from "@/api/request";

export interface AdminOverview {
  total_users: number;
  total_resumes: number;
  total_jobs: number;
  total_analysis_tasks: number;
  total_reports: number;
  total_prompt_templates: number;
  total_api_calls: number;
  failed_api_calls: number;
  pending_tasks: number;
  running_tasks: number;
  failed_tasks: number;
  latest_api_error_message: string | null;
}

export interface AdminPaginatedResult<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface AdminAnalysisTaskItem {
  id: string;
  task_type: string;
  status: string;
  progress: number;
  error_message: string | null;
  user_email: string;
  resume_title: string;
  job_title: string | null;
  created_at: string;
  started_at: string | null;
  finished_at: string | null;
}

export interface AdminApiLogItem {
  id: string;
  provider: string;
  model_name: string;
  scene: string;
  status: string;
  user_email: string | null;
  task_id: string | null;
  prompt_template_name: string | null;
  prompt_tokens: number | null;
  completion_tokens: number | null;
  total_tokens: number | null;
  latency_ms: number | null;
  error_type: string | null;
  error_message: string | null;
  created_at: string;
}

export interface PromptTemplateItem {
  id: string;
  name: string;
  scene: string;
  version: number;
  status: string;
  description: string | null;
  content: string;
  created_by_email: string | null;
  updated_at: string;
  created_at: string;
}

export interface PromptTemplatePayload {
  name: string;
  scene: string;
  version: number;
  status: string;
  description?: string | null;
  content: string;
}

export function getAdminOverview() {
  return get<AdminOverview>("/admin/overview");
}

export function listAdminAnalysisTasks(params?: {
  page?: number;
  page_size?: number;
  status?: string;
  task_type?: string;
  keyword?: string;
}) {
  return get<AdminPaginatedResult<AdminAnalysisTaskItem>>("/admin/analysis-tasks", { params });
}

export function listAdminApiLogs(params?: {
  page?: number;
  page_size?: number;
  status?: string;
  scene?: string;
  keyword?: string;
}) {
  return get<AdminPaginatedResult<AdminApiLogItem>>("/admin/api-logs", { params });
}

export function listPromptTemplates(params?: {
  page?: number;
  page_size?: number;
  scene?: string;
  status?: string;
  keyword?: string;
}) {
  return get<AdminPaginatedResult<PromptTemplateItem>>("/admin/prompt-templates", { params });
}

export function createPromptTemplate(payload: PromptTemplatePayload) {
  return post<PromptTemplateItem>("/admin/prompt-templates", payload);
}

export function updatePromptTemplate(templateId: string, payload: PromptTemplatePayload) {
  return put<PromptTemplateItem>(`/admin/prompt-templates/${templateId}`, payload);
}

export function deletePromptTemplate(templateId: string) {
  return del<{ deleted: boolean }>(`/admin/prompt-templates/${templateId}`);
}
