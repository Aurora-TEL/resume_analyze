<template>
  <div class="app-page" v-loading="loading">
    <section class="hero-card" v-if="task">
      <p class="hero-kicker">Task Status</p>
      <h1 class="hero-title">分析任务 {{ statusLabel(task.status) }}</h1>
      <p class="hero-copy">
        当前进度 {{ task.progress }}%。如果报告已经生成，可以直接进入详情页继续查看结果。
      </p>
      <div class="action-row">
        <el-button v-if="task.report_id" type="primary" @click="router.push(`/reports/${task.report_id}`)">查看报告</el-button>
        <el-button @click="loadTask">刷新状态</el-button>
        <el-button @click="router.push('/analysis/create')">再来一次</el-button>
      </div>
    </section>

    <section class="section-card" v-if="task">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="任务类型">{{ task.task_type }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="statusTagType(task.status)">{{ statusLabel(task.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatDate(task.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="开始时间">{{ formatDate(task.started_at) }}</el-descriptions-item>
        <el-descriptions-item label="完成时间">{{ formatDate(task.finished_at) }}</el-descriptions-item>
        <el-descriptions-item label="报告 ID">{{ task.report_id || "-" }}</el-descriptions-item>
      </el-descriptions>

      <el-alert
        v-if="task.error_message"
        class="task-alert"
        type="warning"
        :closable="false"
        show-icon
        :title="task.error_message"
      />
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { getAnalysisTask, type AnalysisTaskItem } from "@/api/analysis";
import { formatDate, statusLabel, statusTagType } from "@/utils/format";

const route = useRoute();
const router = useRouter();
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
