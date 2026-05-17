import { get } from "@/api/request";
import type { PaginatedResult } from "@/api/resumes";

export interface ReportListItem {
  id: string;
  task_id: string;
  resume_title: string;
  job_title: string | null;
  total_score: string | number | null;
  match_score: string | number | null;
  summary: string | null;
  created_at: string;
}

export interface ReportDetail {
  id: string;
  task_id: string;
  resume_id: string;
  job_description_id: string | null;
  total_score: string | number | null;
  match_score: string | number | null;
  summary: string | null;
  report_data: Record<string, unknown>;
  model_provider: string;
  model_name: string;
  created_at: string;
}

export function listReports(params?: { page?: number; page_size?: number; resume_id?: string; job_description_id?: string }) {
  return get<PaginatedResult<ReportListItem>>("/reports", { params });
}

export function getReportDetail(reportId: string) {
  return get<ReportDetail>(`/reports/${reportId}`);
}
