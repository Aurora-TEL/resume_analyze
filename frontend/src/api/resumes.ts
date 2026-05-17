import { del, get, patch, post } from "@/api/request";

export interface PaginatedResult<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface ResumeListItem {
  id: string;
  title: string;
  file_name: string;
  file_type: string;
  file_size: number;
  parse_status: string;
  version: number;
  is_default: boolean;
  created_at: string;
}

export interface ResumeDetail extends ResumeListItem {
  raw_text: string | null;
  structured_data: Record<string, unknown> | null;
  parse_error: string | null;
  updated_at: string;
}

export interface ResumeUploadResponse {
  resume_id: string;
  title: string;
  file_name: string;
  file_type: string;
  file_size: number;
  parse_status: string;
}

export interface UpdateResumePayload {
  title?: string;
  is_default?: boolean;
}

export function listResumes(params?: { page?: number; page_size?: number; keyword?: string; status?: string }) {
  return get<PaginatedResult<ResumeListItem>>("/resumes", { params });
}

export function uploadResume(formData: FormData) {
  return post<ResumeUploadResponse>("/resumes/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
}

export function getResumeDetail(resumeId: string) {
  return get<ResumeDetail>(`/resumes/${resumeId}`);
}

export function updateResume(resumeId: string, payload: UpdateResumePayload) {
  return patch<ResumeDetail>(`/resumes/${resumeId}`, payload);
}

export function parseResume(resumeId: string) {
  return post<{ resume_id: string; parse_status: string }>(`/resumes/${resumeId}/parse`);
}

export function deleteResume(resumeId: string) {
  return del<null>(`/resumes/${resumeId}`);
}
