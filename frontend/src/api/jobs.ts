import { del, get, post, put } from "@/api/request";
import type { PaginatedResult } from "@/api/resumes";

export interface JobPayload {
  title: string;
  company_name?: string | null;
  industry?: string | null;
  location?: string | null;
  salary_range?: string | null;
  description_text: string;
}

export interface JobListItem {
  id: string;
  title: string;
  company_name: string | null;
  industry: string | null;
  location: string | null;
  parse_status: string;
  created_at: string;
}

export interface JobDetail extends JobListItem {
  salary_range: string | null;
  description_text: string;
  structured_data: Record<string, unknown> | null;
  parse_error: string | null;
  updated_at: string;
}

export interface JobCreateResponse {
  job_id: string;
  title: string;
  parse_status: string;
}

export function listJobs(params?: { page?: number; page_size?: number; keyword?: string }) {
  return get<PaginatedResult<JobListItem>>("/jobs", { params });
}

export function createJob(payload: JobPayload) {
  return post<JobCreateResponse>("/jobs", payload);
}

export function getJobDetail(jobId: string) {
  return get<JobDetail>(`/jobs/${jobId}`);
}

export function updateJob(jobId: string, payload: JobPayload) {
  return put<JobDetail>(`/jobs/${jobId}`, payload);
}

export function parseJob(jobId: string) {
  return post<{ job_id: string; parse_status: string }>(`/jobs/${jobId}/parse`);
}

export function deleteJob(jobId: string) {
  return del<null>(`/jobs/${jobId}`);
}
