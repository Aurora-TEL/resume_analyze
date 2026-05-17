<template>
  <div class="admin-shell">
    <aside class="admin-sidebar">
      <div class="sidebar-top">
        <p class="brand-kicker">{{ t.layout.brandKicker }}</p>
        <h1 class="brand-title">{{ t.layout.brandTitle }}</h1>
        <p class="brand-copy">{{ t.layout.brandCopy }}</p>
      </div>

      <nav class="admin-nav">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="admin-link"
          active-class="is-active"
        >
          <span class="admin-link-title">{{ item.label }}</span>
          <span class="admin-link-copy">{{ item.hint }}</span>
        </RouterLink>
      </nav>

      <div class="sidebar-footer">
        <div class="admin-user">
          <p>{{ userStore.currentUser?.nickname || t.layout.defaultAdminName }}</p>
          <span>{{ userStore.currentUser?.email || "" }}</span>
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
        <el-button plain @click="router.push('/dashboard')">{{ t.layout.backToUserApp }}</el-button>
      </div>
    </aside>

    <main class="admin-main">
      <header class="admin-header">
        <div>
          <p class="admin-kicker">{{ t.layout.operations }}</p>
          <h2>{{ pageTitle }}</h2>
        </div>
      </header>

      <section class="admin-content">
        <router-view />
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";

import { useAdminMessages } from "@/utils/adminI18n";
import { useLocaleStore, type AppLocale } from "@/stores/locale";
import { useUserStore } from "@/stores/user";

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();
const localeStore = useLocaleStore();
const messages = useAdminMessages();

const t = computed(() => messages.value);

const navItems = computed(() => [
  { to: "/admin", label: t.value.layout.navOverview, hint: t.value.layout.navOverviewHint },
  { to: "/admin/analysis-tasks", label: t.value.layout.navTasks, hint: t.value.layout.navTasksHint },
  { to: "/admin/api-logs", label: t.value.layout.navApiLogs, hint: t.value.layout.navApiLogsHint },
  { to: "/admin/prompt-templates", label: t.value.layout.navPromptTemplates, hint: t.value.layout.navPromptTemplatesHint },
]);

const localeOptions = computed(() => [
  { label: t.value.layout.languageChinese, value: "zh-CN" },
  { label: t.value.layout.languageEnglish, value: "en-US" },
]);

function handleLocaleChange(value: string | number | boolean) {
  localeStore.setLocale(value as AppLocale);
}

const pageTitle = computed(() => {
  if (route.path === "/admin") {
    return t.value.layout.titleOverview;
  }
  if (route.path === "/admin/analysis-tasks") {
    return t.value.layout.titleTasks;
  }
  if (route.path === "/admin/api-logs") {
    return t.value.layout.titleApiLogs;
  }
  if (route.path === "/admin/prompt-templates") {
    return t.value.layout.titlePromptTemplates;
  }
  return t.value.layout.titleDefault;
});
</script>

<style scoped lang="scss">
.admin-shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 300px 1fr;
  background:
    radial-gradient(circle at top right, rgba(26, 145, 128, 0.18), transparent 30%),
    linear-gradient(180deg, #f5f8f7 0%, #eef2f6 100%);
}

.admin-sidebar {
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  background: linear-gradient(180deg, #132827 0%, #1a3436 100%);
  color: #f5f8f6;
}

.sidebar-top,
.sidebar-footer {
  display: grid;
  gap: 10px;
}

.brand-kicker,
.admin-kicker {
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: rgba(245, 248, 246, 0.65);
}

.brand-title {
  margin: 0;
  font-size: 34px;
  line-height: 1.05;
}

.brand-copy {
  margin: 0;
  line-height: 1.7;
  color: rgba(245, 248, 246, 0.75);
}

.admin-nav {
  display: grid;
  gap: 12px;
}

.admin-link {
  padding: 14px;
  display: grid;
  gap: 6px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid transparent;
}

.admin-link.is-active,
.admin-link:hover {
  border-color: rgba(255, 255, 255, 0.18);
  background: rgba(255, 255, 255, 0.12);
}

.admin-link-title {
  font-weight: 700;
}

.admin-link-copy {
  font-size: 13px;
  color: rgba(245, 248, 246, 0.72);
}

.sidebar-footer {
  margin-top: auto;
}

.locale-switch {
  display: grid;
  gap: 8px;
}

.locale-label {
  font-size: 12px;
  color: rgba(245, 248, 246, 0.72);
}

.admin-user p,
.admin-user span {
  margin: 0;
}

.admin-user span {
  color: rgba(245, 248, 246, 0.7);
  font-size: 13px;
}

.admin-main {
  padding: 24px;
}

.admin-header {
  padding: 22px 24px;
  border: 1px solid var(--panel-border);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.86);
  box-shadow: var(--shadow-soft);
}

.admin-header h2 {
  margin: 8px 0 0;
  font-size: 30px;
}

.admin-kicker {
  color: var(--brand-primary);
}

.admin-content {
  padding-top: 24px;
}

@media (max-width: 980px) {
  .admin-shell {
    grid-template-columns: 1fr;
  }
}
</style>
