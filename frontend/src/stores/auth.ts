import { computed, ref } from "vue";
import { defineStore } from "pinia";

const TOKEN_KEY = "resume-token";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem(TOKEN_KEY) || "");

  const isAuthenticated = computed(() => Boolean(token.value));

  function setToken(value: string) {
    token.value = value;

    if (value) {
      localStorage.setItem(TOKEN_KEY, value);
      return;
    }

    localStorage.removeItem(TOKEN_KEY);
  }

  function logout() {
    setToken("");
  }

  return {
    token,
    isAuthenticated,
    setToken,
    logout,
  };
});
