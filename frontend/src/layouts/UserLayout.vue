<template>
  <div class="shell">
    <aside class="sidebar">
      <div class="brand-block">
        <p class="brand-kicker">Resume Studio</p>
        <h1 class="brand-title">AI Resume Analyzer</h1>
        <p class="brand-copy">{{ t.layout.brandCopy }}</p>
      </div>

      <nav class="nav-list">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="nav-link"
          active-class="is-active"
        >
          <span class="nav-label">{{ item.label }}</span>
          <span class="nav-hint">{{ item.hint }}</span>
        </RouterLink>
      </nav>

      <div class="sidebar-footer">
        <div class="user-card">
          <p class="user-name">{{ userStore.currentUser?.nickname || t.layout.defaultUserName }}</p>
          <p class="user-email">{{ userStore.currentUser?.email || t.layout.loggedOut }}</p>
        </div>

        <div class="locale-switch">
          <span class="locale-label">{{ t.layout.languageLabel }}</span>
          <el-segmented
            v-model="localeStore.locale"
            :options="localeOptions"
            size="small"
            @change="handleLocaleChange"
          />
        </div>

        <el-button plain @click="handleLogout">{{ t.layout.logout }}</el-button>
      </div>
    </aside>

    <main class="main-panel">
      <header class="topbar">
        <div>
          <p class="topbar-kicker">Local + DeepSeek</p>
          <h2 class="topbar-title">{{ currentRouteTitle }}</h2>
        </div>
        <div class="topbar-actions">
          <el-button @click="router.push('/analysis/create')">{{ t.layout.newAnalysis }}</el-button>
          <el-button type="primary" @click="router.push('/resumes/upload')">{{ t.layout.uploadResume }}</el-button>
        </div>
      </header>

      <section class="main-content">
        <router-view />
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";

import { logout as requestLogout } from "@/api/auth";
import { useAuthStore } from "@/stores/auth";
import { useLocaleStore, type AppLocale } from "@/stores/locale";
import { useUserStore } from "@/stores/user";
import { useUserMessages } from "@/utils/userI18n";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const localeStore = useLocaleStore();
const userStore = useUserStore();
const messages = useUserMessages();

const t = computed(() => messages.value);

const navItems = computed(() => [
  { to: "/dashboard", label: t.value.layout.navDashboard, hint: t.value.layout.navDashboardHint },
  { to: "/resumes", label: t.value.layout.navResumes, hint: t.value.layout.navResumesHint },
  { to: "/jobs", label: t.value.layout.navJobs, hint: t.value.layout.navJobsHint },
  { to: "/analysis/create", label: t.value.layout.navAnalysis, hint: t.value.layout.navAnalysisHint },
  { to: "/reports", label: t.value.layout.navReports, hint: t.value.layout.navReportsHint },
  { to: "/profile", label: t.value.layout.navProfile, hint: t.value.layout.navProfileHint },
]);

const localeOptions = computed(() => [
  { label: t.value.layout.languageChinese, value: "zh-CN" },
  { label: t.value.layout.languageEnglish, value: "en-US" },
]);

const currentRouteTitle = computed(() => {
  if (route.path === "/dashboard") {
    return t.value.layout.titleDashboard;
  }
  if (route.path === "/resumes") {
    return t.value.layout.titleResumes;
  }
  if (route.path === "/resumes/upload") {
    return t.value.layout.titleResumeUpload;
  }
  if (route.path.startsWith("/resumes/")) {
    return t.value.layout.titleResumeDetail;
  }
  if (route.path === "/jobs") {
    return t.value.layout.titleJobs;
  }
  if (route.path === "/jobs/create") {
    return t.value.layout.titleJobCreate;
  }
  if (route.path.startsWith("/jobs/")) {
    return t.value.layout.titleJobDetail;
  }
  if (route.path === "/analysis/create") {
    return t.value.layout.titleAnalysisCreate;
  }
  if (route.path.startsWith("/analysis/tasks/")) {
    return t.value.layout.titleAnalysisTask;
  }
  if (route.path === "/reports") {
    return t.value.layout.titleReports;
  }
  if (route.path.startsWith("/reports/")) {
    return t.value.layout.titleReportDetail;
  }
  if (route.path === "/profile") {
    return t.value.layout.titleProfile;
  }
  return t.value.layout.titleFallback;
});

function handleLocaleChange(value: string | number | boolean) {
  localeStore.setLocale(value as AppLocale);
}

async function handleLogout() {
  try {
    await requestLogout();
  } catch {
    // Ignore logout API errors and clear local session anyway.
  }

  authStore.logout();
  userStore.clearCurrentUser();
  router.push("/login");
}
</script>

<style scoped lang="scss">
.shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 320px 1fr;
  background:
    radial-gradient(circle at top left, rgba(24, 111, 92, 0.26), transparent 30%),
    linear-gradient(180deg, #f5efe3 0%, #eef3f1 100%);
}

.sidebar {
  padding: 28px 22px;
  display: flex;
  flex-direction: column;
  gap: 28px;
  background: linear-gradient(180deg, #173732 0%, #214d45 100%);
  color: #f5f7f2;
}

.brand-block {
  display: grid;
  gap: 10px;
}

.brand-kicker,
.topbar-kicker {
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.65);
}

.brand-title,
.topbar-title {
  margin: 0;
  font-size: 30px;
  line-height: 1.1;
}

.brand-copy {
  margin: 0;
  color: rgba(245, 247, 242, 0.78);
  line-height: 1.7;
}

.nav-list {
  display: grid;
  gap: 12px;
}

.nav-link {
  padding: 14px 16px;
  display: grid;
  gap: 6px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid transparent;
  transition:
    transform 0.18s ease,
    border-color 0.18s ease,
    background 0.18s ease;
}

.nav-link:hover,
.nav-link.is-active {
  transform: translateY(-1px);
  border-color: rgba(255, 255, 255, 0.22);
  background: rgba(255, 255, 255, 0.14);
}

.nav-label {
  font-size: 16px;
  font-weight: 700;
}

.nav-hint {
  font-size: 13px;
  color: rgba(245, 247, 242, 0.72);
}

.sidebar-footer {
  margin-top: auto;
  display: grid;
  gap: 14px;
}

.user-card {
  padding: 16px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.08);
}

.user-name,
.user-email {
  margin: 0;
}

.user-name {
  font-size: 15px;
  font-weight: 700;
}

.user-email {
  margin-top: 6px;
  font-size: 13px;
  color: rgba(245, 247, 242, 0.72);
}

.locale-switch {
  display: grid;
  gap: 8px;
}

.locale-label {
  font-size: 12px;
  color: rgba(245, 247, 242, 0.72);
}

.main-panel {
  min-width: 0;
  padding: 24px;
}

.topbar {
  padding: 22px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  border: 1px solid rgba(49, 62, 82, 0.1);
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.74);
  backdrop-filter: blur(16px);
  box-shadow: var(--shadow-soft);
}

.topbar-kicker {
  color: var(--brand-primary);
}

.topbar-title {
  font-size: 26px;
  color: var(--text-primary);
}

.topbar-actions {
  display: flex;
  gap: 12px;
}

.main-content {
  padding-top: 24px;
}

@media (max-width: 1080px) {
  .shell {
    grid-template-columns: 1fr;
  }

  .topbar {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 640px) {
  .main-panel {
    padding: 16px;
  }

  .topbar-actions {
    width: 100%;
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
}
</style>
