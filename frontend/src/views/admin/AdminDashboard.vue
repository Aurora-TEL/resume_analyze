<template>
  <div class="app-page" v-loading="loading">
    <section class="hero-card">
      <p class="hero-kicker">{{ t.kicker }}</p>
      <h1 class="hero-title">{{ t.title }}</h1>
      <p class="hero-copy">{{ t.copy }}</p>
    </section>

    <section class="metric-grid" v-if="overview">
      <article class="metric-card">
        <p class="metric-label">{{ t.users }}</p>
        <p class="metric-value">{{ overview.total_users }}</p>
        <p class="metric-note">{{ t.usersNote }}</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">{{ t.resumesJobs }}</p>
        <p class="metric-value">{{ overview.total_resumes }} / {{ overview.total_jobs }}</p>
        <p class="metric-note">{{ t.resumesJobsNote }}</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">{{ t.analysisTasks }}</p>
        <p class="metric-value">{{ overview.total_analysis_tasks }}</p>
        <p class="metric-note">{{ t.analysisTasksNote(overview.pending_tasks, overview.running_tasks) }}</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">{{ t.aiCalls }}</p>
        <p class="metric-value">{{ overview.total_api_calls }}</p>
        <p class="metric-note">{{ t.aiCallsNote(overview.failed_api_calls) }}</p>
      </article>
    </section>

    <div class="two-column" v-if="overview">
      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">{{ t.alertsTitle }}</h2>
            <p class="section-copy">{{ t.alertsCopy }}</p>
          </div>
        </div>

        <el-alert
          :type="overview.failed_api_calls > 0 || overview.failed_tasks > 0 ? 'warning' : 'success'"
          :closable="false"
          show-icon
          :title="
            overview.failed_api_calls > 0 || overview.failed_tasks > 0
              ? t.alertsWarning
              : t.alertsOk
          "
        />

        <el-descriptions :column="1" border class="dashboard-descriptions">
          <el-descriptions-item :label="t.failedTasks">{{ overview.failed_tasks }}</el-descriptions-item>
          <el-descriptions-item :label="t.promptTemplates">{{ overview.total_prompt_templates }}</el-descriptions-item>
          <el-descriptions-item :label="t.reports">{{ overview.total_reports }}</el-descriptions-item>
          <el-descriptions-item :label="t.latestApiError">
            {{ overview.latest_api_error_message || t.noRecentError }}
          </el-descriptions-item>
        </el-descriptions>
      </section>

      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">{{ t.quickLinksTitle }}</h2>
            <p class="section-copy">{{ t.quickLinksCopy }}</p>
          </div>
        </div>

        <div class="quick-links">
          <button class="quick-link" @click="router.push('/admin/analysis-tasks')">
            <strong>{{ t.taskCenterTitle }}</strong>
            <span>{{ t.taskCenterCopy }}</span>
          </button>
          <button class="quick-link" @click="router.push('/admin/api-logs')">
            <strong>{{ t.apiLogsTitle }}</strong>
            <span>{{ t.apiLogsCopy }}</span>
          </button>
          <button class="quick-link" @click="router.push('/admin/prompt-templates')">
            <strong>{{ t.promptTitle }}</strong>
            <span>{{ t.promptCopy }}</span>
          </button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import { getAdminOverview, type AdminOverview } from "@/api/admin";
import { useAdminMessages } from "@/utils/adminI18n";

const router = useRouter();
const loading = ref(false);
const overview = ref<AdminOverview | null>(null);
const messages = useAdminMessages();
const t = computed(() => messages.value.overview);

async function loadOverview() {
  loading.value = true;
  try {
    overview.value = await getAdminOverview();
  } finally {
    loading.value = false;
  }
}

onMounted(loadOverview);
</script>

<style scoped lang="scss">
.dashboard-descriptions {
  margin-top: 18px;
}

.quick-links {
  display: grid;
  gap: 12px;
}

.quick-link {
  padding: 16px;
  display: grid;
  gap: 8px;
  text-align: left;
  border: 1px solid var(--panel-border);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.88);
  cursor: pointer;
}

.quick-link span {
  color: var(--text-secondary);
}
</style>
