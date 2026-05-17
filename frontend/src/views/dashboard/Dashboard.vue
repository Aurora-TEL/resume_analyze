<template>
  <div class="app-page">
    <section class="hero-card">
      <p class="hero-kicker">Workspace Snapshot</p>
      <h1 class="hero-title">你的简历分析工作台已经进入可用状态。</h1>
      <p class="hero-copy">
        当前前端会直接连接本地后端和 DeepSeek。你可以从这里快速跳到上传简历、创建岗位或查看最近的分析结果。
      </p>
      <div class="action-row">
        <el-button type="primary" @click="router.push('/resumes/upload')">上传新简历</el-button>
        <el-button @click="router.push('/jobs/create')">创建岗位</el-button>
        <el-button @click="router.push('/analysis/create')">发起分析</el-button>
      </div>
    </section>

    <section class="metric-grid">
      <article class="metric-card">
        <p class="metric-label">简历数量</p>
        <p class="metric-value">{{ metrics.resumeTotal }}</p>
        <p class="metric-note">已上传并纳入当前工作流的简历总数。</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">岗位数量</p>
        <p class="metric-value">{{ metrics.jobTotal }}</p>
        <p class="metric-note">已整理并可直接匹配的岗位描述。</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">分析任务</p>
        <p class="metric-value">{{ metrics.taskTotal }}</p>
        <p class="metric-note">包含已完成和进行中的分析任务。</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">报告沉淀</p>
        <p class="metric-value">{{ metrics.reportTotal }}</p>
        <p class="metric-note">已经生成，可供回看和迭代的分析报告。</p>
      </article>
    </section>

    <section class="two-column">
      <article class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">最近报告</h2>
            <p class="section-copy">优先回看最新结果，快速进入下一轮优化。</p>
          </div>
          <el-button text @click="router.push('/reports')">查看全部</el-button>
        </div>

        <el-empty v-if="!latestReports.length && !loading" description="还没有报告，先发起一次分析吧。" />

        <el-table v-else :data="latestReports" stripe>
          <el-table-column prop="resume_title" label="简历" min-width="170" />
          <el-table-column prop="job_title" label="岗位" min-width="180" />
          <el-table-column label="总分" width="96">
            <template #default="{ row }">{{ formatScore(row.total_score) }}</template>
          </el-table-column>
          <el-table-column label="匹配度" width="100">
            <template #default="{ row }">{{ formatScore(row.match_score) }}</template>
          </el-table-column>
          <el-table-column label="生成时间" min-width="160">
            <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
          </el-table-column>
          <el-table-column label="操作" width="110" fixed="right">
            <template #default="{ row }">
              <el-button text type="primary" @click="router.push(`/reports/${row.id}`)">查看</el-button>
            </template>
          </el-table-column>
        </el-table>
      </article>

      <article class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">下一步建议</h2>
            <p class="section-copy">按照这条顺序推进，会更快进入稳定产出。</p>
          </div>
        </div>

        <el-steps direction="vertical" :active="activeStep">
          <el-step title="上传简历" description="至少准备一份可以参与 AI 解析的简历文件。" />
          <el-step title="整理岗位" description="补充目标岗位 JD，帮助模型判断技能与关键词匹配度。" />
          <el-step title="生成报告" description="发起 full_analysis，查看 strengths、weaknesses 和 next actions。" />
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

const router = useRouter();
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
