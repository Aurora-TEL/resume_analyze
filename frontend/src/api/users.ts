import { put } from "@/api/request";
import type { CurrentUserResponse } from "@/api/auth";

export interface UpdateProfilePayload {
  nickname?: string | null;
  phone?: string | null;
  target_position?: string | null;
  target_city?: string | null;
  work_years?: number | null;
}

export interface UpdatePasswordPayload {
  old_password: string;
  new_password: string;
}

export function updateCurrentUser(payload: UpdateProfilePayload) {
  return put<CurrentUserResponse>("/users/me", payload);
}

export function updatePassword(payload: UpdatePasswordPayload) {
  return put<{ updated: boolean }>("/users/me/password", payload);
}
