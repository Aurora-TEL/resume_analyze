import { computed, ref } from "vue";
import { defineStore } from "pinia";

export type AppLocale = "zh-CN" | "en-US";

export const LOCALE_KEY = "resume-locale";

export const useLocaleStore = defineStore("locale", () => {
  const locale = ref<AppLocale>((localStorage.getItem(LOCALE_KEY) as AppLocale) || "zh-CN");

  const isChinese = computed(() => locale.value === "zh-CN");

  function setLocale(value: AppLocale) {
    locale.value = value;
    localStorage.setItem(LOCALE_KEY, value);
  }

  function toggleLocale() {
    setLocale(locale.value === "zh-CN" ? "en-US" : "zh-CN");
  }

  return {
    locale,
    isChinese,
    setLocale,
    toggleLocale,
  };
});
