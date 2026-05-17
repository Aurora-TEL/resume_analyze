import axios, { type AxiosRequestConfig } from "axios";
import { ElMessage } from "element-plus";

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api",
  timeout: 60000,
});

request.interceptors.request.use((config) => {
  const token = localStorage.getItem("resume-token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

request.interceptors.response.use(
  (response) => response.data?.data ?? response.data,
  (error) => {
    const payload = error.response?.data;
    const message = payload?.message || error.message || "Request failed";

    if (error.response?.status === 401) {
      localStorage.removeItem("resume-token");
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }

    ElMessage.error(message);
    return Promise.reject(payload ?? error);
  },
);

export function get<T>(url: string, config?: AxiosRequestConfig) {
  return request.get<unknown, T>(url, config);
}

export function post<T>(url: string, data?: unknown, config?: AxiosRequestConfig) {
  return request.post<unknown, T>(url, data, config);
}

export function put<T>(url: string, data?: unknown, config?: AxiosRequestConfig) {
  return request.put<unknown, T>(url, data, config);
}

export function patch<T>(url: string, data?: unknown, config?: AxiosRequestConfig) {
  return request.patch<unknown, T>(url, data, config);
}

export function del<T>(url: string, config?: AxiosRequestConfig) {
  return request.delete<unknown, T>(url, config);
}
