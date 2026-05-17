<template>
  <div class="app-page">
    <section class="hero-card">
      <p class="hero-kicker">Workspace Snapshot</p>
      <h1 class="hero-title">{{ t.dashboard.heroTitle }}</h1>
      <p class="hero-copy">{{ t.dashboard.heroCopy }}</p>
      <div class="action-row">
        <el-button type="primary" @click="router.push('/resumes/upload')">{{ t.dashboard.actionUpload }}</el-button>
        <el-button @click="router.push('/jobs/create')">{{ t.dashboard.actionCreateJob }}</el-button>
        <el-button @click="router.push('/analysis/create')">{{ t.dashboard.actionStartAnalysis }}</el-button>
      </div>
    </section>

    <section class="metric-grid">
      <article class="metric-card">
        <p class="metric-label">{{ t.dashboard.metricResumes }}</p>
        <p class="metric-value">{{ metrics.resumeTotal }}</p>
        <p class="metric-note">{{ t.dashboard.metricResumesNote }}</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">{{ t.dashboard.metricJobs }}</p>
        <p class="metric-value">{{ metrics.jobTotal }}</p>
        <p class="metric-note">{{ t.dashboard.metricJobsNote }}</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">{{ t.dashboard.metricTasks }}</p>
        <p class="metric-value">{{ metrics.taskTotal }}</p>
        <p class="metric-note">{{ t.dashboard.metricTasksNote }}</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">{{ t.dashboard.metricReports }}</p>
        <p class="metric-value">{{ metrics.reportTotal }}</p>
        <p class="metric-note">{{ t.dashboard.metricReportsNote }}</p>
      </article>
    </section>

    <section class="two-column">
      <article class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">{{ t.dashboard.recentReportsTitle }}</h2>
            <p class="section-copy">{{ t.dashboard.recentReportsCopy }}</p>
          </div>
          <el-button text @click="router.push('/reports')">{{ t.dashboard.recentReportsAll }}</el-button>
        </div>

        <el-empty v-if="!latestReports.length && !loading" :description="t.dashboard.recentReportsEmpty" />

        <el-table v-else :data="latestReports" stripe>
          <el-table-column prop="resume_title" :label="t.dashboard.tableResume" min-width="170" />
          <el-table-column prop="job_title" :label="t.dashboard.tableJob" min-width="180" />
          <el-table-column :label="t.dashboard.tableTotalScore" width="96">
            <template #default="{ row }">{{ formatScore(row.total_score) }}</template>
          </el-table-column>
          <el-table-column :label="t.dashboard.tableMatchScore" width="100">
            <template #default="{ row }">{{ formatScore(row.match_score) }}</template>
          </el-table-column>
          <el-table-column :label="t.dashboard.tableCreatedAt" min-width="160">
            <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
          </el-table-column>
          <el-table-column :label="t.dashboard.tableAction" width="110" fixed="right">
            <template #default="{ row }">
              <el-button text type="primary" @click="router.push(`/reports/${row.id}`)">{{ t.dashboard.tableView }}</el-button>
            </template>
          </el-table-column>
        </el-table>
      </article>

      <article class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">{{ t.dashboard.nextStepsTitle }}</h2>
            <p class="section-copy">{{ t.dashboard.nextStepsCopy }}</p>
          </div>
        </div>

        <el-steps direction="vertical" :active="activeStep">
          <el-step :title="t.dashboard.stepUploadTitle" :description="t.dashboard.stepUploadDesc" />
          <el-step :title="t.dashboard.stepJobTitle" :description="t.dashboard.stepJobDesc" />
          <el-step :title="t.dashboard.stepReportTitle" :description="t.dashboard.stepReportDesc" />
        </el-steps>
      </article>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";

import { listAnalysisTasks } from "@/api/analysis";
import { listJobs } from "@/api/jobs";
import { listReports, type ReportListItem } from "@/api/reports";
import { listResumes } from "@/api/resumes";
import { formatDate, formatScore } from "@/utils/format";
import { useUserMessages } from "@/utils/userI18n";

const router = useRouter();
const messages = useUserMessages();
const t = computed(() => messages.value);
const loading = ref(false);
const latestReports = ref<ReportListItem[]>([]);
const metrics = reactive({
  resumeTotal: 0,
  jobTotal: 0,
  taskTotal: 0,
  reportTotal: 0,
});

const activeStep = computed(() => {
  if (!metrics.resumeTotal) {
    return 0;
  }
  if (!metrics.jobTotal) {
    return 1;
  }
  if (!metrics.reportTotal) {
    return 2;
  }
  return 3;
});

async function loadDashboard() {
  loading.value = true;
  try {
    const [resumes, jobs, tasks, reports] = await Promise.all([
      listResumes({ page: 1, page_size: 1 }),
      listJobs({ page: 1, page_size: 1 }),
      listAnalysisTasks({ page: 1, page_size: 1 }),
      listReports({ page: 1, page_size: 5 }),
    ]);

    metrics.resumeTotal = resumes.total;
    metrics.jobTotal = jobs.total;
    metrics.taskTotal = tasks.total;
    metrics.reportTotal = reports.total;
    latestReports.value = reports.items;
  } finally {
    loading.value = false;
  }
}

onMounted(loadDashboard);
</script>
