import { LOCALE_KEY, type AppLocale } from "@/stores/locale";

function getCurrentLocale(): AppLocale {
  const locale = localStorage.getItem(LOCALE_KEY);
  return locale === "en-US" ? "en-US" : "zh-CN";
}

export function formatDate(value?: string | null) {
  if (!value) {
    return "-";
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat(getCurrentLocale(), {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

export function formatFileSize(size?: number | null) {
  if (!size) {
    return "0 B";
  }

  if (size < 1024) {
    return `${size} B`;
  }

  if (size < 1024 * 1024) {
    return `${(size / 1024).toFixed(1)} KB`;
  }

  return `${(size / (1024 * 1024)).toFixed(1)} MB`;
}

export function formatScore(value?: string | number | null) {
  if (value === null || value === undefined || value === "") {
    return "-";
  }

  const numericValue = Number(value);
  if (Number.isNaN(numericValue)) {
    return String(value);
  }

  return `${numericValue.toFixed(0)}`;
}

export function statusLabel(status?: string | null) {
  const locale = getCurrentLocale();
  const map: Record<AppLocale, Record<string, string>> = {
    "zh-CN": {
      pending: "\u7b49\u5f85\u4e2d",
      success: "\u6210\u529f",
      failed: "\u5931\u8d25",
      running: "\u8fdb\u884c\u4e2d",
      canceled: "\u5df2\u53d6\u6d88",
      active: "\u542f\u7528",
      inactive: "\u505c\u7528",
      deleted: "\u5df2\u5220\u9664",
      user: "\u7528\u6237",
      admin: "\u7ba1\u7406\u5458",
    },
    "en-US": {
      pending: "Pending",
      success: "Success",
      failed: "Failed",
      running: "Running",
      canceled: "Canceled",
      active: "Active",
      inactive: "Inactive",
      deleted: "Deleted",
      user: "User",
      admin: "Admin",
    },
  };

  return status ? (map[locale][status] || status) : "-";
}

export function statusTagType(status?: string | null) {
  const map: Record<string, "success" | "warning" | "danger" | "info" | "primary"> = {
    success: "success",
    running: "warning",
    pending: "info",
    failed: "danger",
    active: "success",
  };

  return map[status || ""] || "info";
}

export function asArray(value: unknown) {
  return Array.isArray(value) ? value : [];
}

export function formatListItem(value: unknown) {
  if (value === null || value === undefined) {
    return "";
  }

  if (typeof value !== "object") {
    return String(value);
  }

  const item = value as Record<string, unknown>;
  const original = item.original ? String(item.original) : "";
  const suggested = item.suggested ? String(item.suggested) : "";
  const locale = getCurrentLocale();

  if (original && suggested) {
    return locale === "zh-CN"
      ? `\u539f\u6587: ${original}\n\u5efa\u8bae: ${suggested}`
      : `Original: ${original}\nSuggested: ${suggested}`;
  }

  return JSON.stringify(value, null, 2);
}
