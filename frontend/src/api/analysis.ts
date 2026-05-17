import { get, post } from "@/api/request";
import type { PaginatedResult } from "@/api/resumes";

export interface AnalysisTaskPayload {
  resume_id: string;
  job_description_id: string;
  task_type: "full_analysis";
}

export interface AnalysisTaskResponse {
  task_id: string;
  status: string;
  report_id: string | null;
}

export interface AnalysisTaskItem {
  id?: string;
  task_id?: string;
  task_type: string;
  status: string;
  progress: number;
  error_message: string | null;
  report_id?: string | null;
  created_at: string;
  started_at: string | null;
  finished_at: string | null;
}

export function createAnalysisTask(payload: AnalysisTaskPayload) {
  return post<AnalysisTaskResponse>("/analysis/tasks", payload);
}

export function getAnalysisTask(taskId: string) {
  return get<AnalysisTaskItem>(`/analysis/tasks/${taskId}`);
}

export function listAnalysisTasks(params?: { page?: number; page_size?: number; status?: string; task_type?: string }) {
  return get<PaginatedResult<AnalysisTaskItem>>("/analysis/tasks", { params });
}
