import { ref } from "vue";
import { defineStore } from "pinia";

import { getCurrentUser, type CurrentUserResponse } from "@/api/auth";

export const useUserStore = defineStore("user", () => {
  const currentUser = ref<CurrentUserResponse | null>(null);
  const hydrated = ref(false);

  async function fetchCurrentUser(force = false) {
    if (!force && currentUser.value) {
      hydrated.value = true;
      return currentUser.value;
    }

    const user = await getCurrentUser();
    currentUser.value = user;
    hydrated.value = true;
    return user;
  }

  function setCurrentUser(user: CurrentUserResponse | null) {
    currentUser.value = user;
    hydrated.value = true;
  }

  function clearCurrentUser() {
    currentUser.value = null;
    hydrated.value = false;
  }

  return {
    currentUser,
    hydrated,
    fetchCurrentUser,
    setCurrentUser,
    clearCurrentUser,
  };
});
