<template>
  <div class="app-page" v-loading="loading">
    <section class="hero-card" v-if="task">
      <p class="hero-kicker">Task Status</p>
      <h1 class="hero-title">{{ `${t.heroTitle} ${statusLabel(task.status)}` }}</h1>
      <p class="hero-copy">{{ t.progressCopy.replace("{progress}", String(task.progress)) }}</p>
      <div class="action-row">
        <el-button v-if="task.report_id" type="primary" @click="router.push(`/reports/${task.report_id}`)">{{ t.viewReport }}</el-button>
        <el-button @click="loadTask">{{ t.refresh }}</el-button>
        <el-button @click="router.push('/analysis/create')">{{ t.tryAgain }}</el-button>
      </div>
    </section>

    <section class="section-card" v-if="task">
      <el-descriptions :column="2" border>
        <el-descriptions-item :label="t.labelTaskType">{{ task.task_type }}</el-descriptions-item>
        <el-descriptions-item :label="t.labelStatus">
          <el-tag :type="statusTagType(task.status)">{{ statusLabel(task.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item :label="t.labelCreatedAt">{{ formatDate(task.created_at) }}</el-descriptions-item>
        <el-descriptions-item :label="t.labelStartedAt">{{ formatDate(task.started_at) }}</el-descriptions-item>
        <el-descriptions-item :label="t.labelFinishedAt">{{ formatDate(task.finished_at) }}</el-descriptions-item>
        <el-descriptions-item :label="t.labelReportId">{{ task.report_id || "-" }}</el-descriptions-item>
      </el-descriptions>

      <el-alert v-if="task.error_message" class="task-alert" type="warning" :closable="false" show-icon :title="task.error_message" />
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { getAnalysisTask, type AnalysisTaskItem } from "@/api/analysis";
import { useLocaleStore } from "@/stores/locale";
import { formatDate, statusLabel, statusTagType } from "@/utils/format";

const zh = {
  heroTitle: "\u5206\u6790\u4efb\u52a1",
  progressCopy: "\u5f53\u524d\u8fdb\u5ea6 {progress}%\u3002\u5982\u679c\u62a5\u544a\u5df2\u7ecf\u751f\u6210\uff0c\u53ef\u4ee5\u76f4\u63a5\u8fdb\u5165\u8be6\u60c5\u9875\u7ee7\u7eed\u67e5\u770b\u7ed3\u679c\u3002",
  viewReport: "\u67e5\u770b\u62a5\u544a",
  refresh: "\u5237\u65b0\u72b6\u6001",
  tryAgain: "\u518d\u6765\u4e00\u6b21",
  labelTaskType: "\u4efb\u52a1\u7c7b\u578b",
  labelStatus: "\u72b6\u6001",
  labelCreatedAt: "\u521b\u5efa\u65f6\u95f4",
  labelStartedAt: "\u5f00\u59cb\u65f6\u95f4",
  labelFinishedAt: "\u5b8c\u6210\u65f6\u95f4",
  labelReportId: "\u62a5\u544a ID",
};

const en = {
  heroTitle: "Analysis Task",
  progressCopy: "Current progress is {progress}%. If the report has already been generated, you can go straight to the detail page to review it.",
  viewReport: "View Report",
  refresh: "Refresh Status",
  tryAgain: "Run Again",
  labelTaskType: "Task Type",
  labelStatus: "Status",
  labelCreatedAt: "Created At",
  labelStartedAt: "Started At",
  labelFinishedAt: "Finished At",
  labelReportId: "Report ID",
};

const route = useRoute();
const router = useRouter();
const localeStore = useLocaleStore();
const t = computed(() => (localeStore.locale === "zh-CN" ? zh : en));
const loading = ref(false);
const task = ref<AnalysisTaskItem | null>(null);

async function loadTask() {
  loading.value = true;
  try {
    task.value = await getAnalysisTask(String(route.params.id));
  } finally {
    loading.value = false;
  }
}

onMounted(loadTask);
</script>

<style scoped lang="scss">
.task-alert {
  margin-top: 20px;
}
</style>
