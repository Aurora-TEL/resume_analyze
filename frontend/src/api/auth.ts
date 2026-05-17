import { get, post } from "@/api/request";

export interface AuthUser {
  id: string;
  email: string;
  nickname: string | null;
  role: "user" | "admin";
  status: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  email: string;
  password: string;
  nickname?: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: AuthUser;
}

export interface RegisterResponse {
  user_id: string;
  email: string;
  nickname: string | null;
  role: "user" | "admin";
  access_token: string;
  token_type: string;
}

export interface CurrentUserResponse {
  id: string;
  email: string;
  nickname: string | null;
  phone: string | null;
  avatar_url: string | null;
  target_position: string | null;
  target_city: string | null;
  work_years: number | null;
  role: "user" | "admin";
  status: string;
}

export function login(payload: LoginPayload) {
  return post<LoginResponse>("/auth/login", payload);
}

export function register(payload: RegisterPayload) {
  return post<RegisterResponse>("/auth/register", payload);
}

export function getCurrentUser() {
  return get<CurrentUserResponse>("/auth/me");
}

export function logout() {
  return post<{ logged_out: boolean }>("/auth/logout");
}
