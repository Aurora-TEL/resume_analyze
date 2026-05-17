<template>
  <div class="app-page">
    <section class="section-card">
      <div class="section-head">
        <div>
          <h2 class="section-title">{{ t.title }}</h2>
          <p class="section-copy">{{ t.copy }}</p>
        </div>
      </div>

      <div class="toolbar">
        <el-input v-model="filters.keyword" :placeholder="t.searchPlaceholder" clearable @change="handleSearch" />
        <el-select v-model="filters.status" clearable :placeholder="t.statusPlaceholder" @change="handleSearch">
          <el-option :label="localeStatusText('pending')" value="pending" />
          <el-option :label="localeStatusText('running')" value="running" />
          <el-option :label="localeStatusText('success')" value="success" />
          <el-option :label="localeStatusText('failed')" value="failed" />
        </el-select>
        <el-select v-model="filters.taskType" clearable :placeholder="t.taskTypePlaceholder" @change="handleSearch">
          <el-option :label="taskTypeText('full_analysis')" value="full_analysis" />
          <el-option :label="taskTypeText('job_match')" value="job_match" />
          <el-option :label="taskTypeText('resume_score')" value="resume_score" />
        </el-select>
      </div>

      <el-table v-loading="loading" :data="rows" stripe>
        <el-table-column prop="user_email" :label="t.user" min-width="190" />
        <el-table-column prop="resume_title" :label="t.resume" min-width="160" />
        <el-table-column prop="job_title" :label="t.job" min-width="170" />
        <el-table-column :label="t.taskType" width="120">
          <template #default="{ row }">{{ taskTypeText(row.task_type) }}</template>
        </el-table-column>
        <el-table-column :label="t.status" width="100">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)">{{ localeStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column :label="t.progress" width="120">
          <template #default="{ row }">
            <el-progress :percentage="row.progress" :stroke-width="10" />
          </template>
        </el-table-column>
        <el-table-column :label="t.createdAt" min-width="160">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column :label="t.errorMessage" min-width="220" show-overflow-tooltip>
          <template #default="{ row }">{{ row.error_message || "-" }}</template>
        </el-table-column>
      </el-table>

      <div class="pagination-row">
        <el-pagination
          layout="prev, pager, next, total"
          :current-page="pagination.page"
          :page-size="pagination.pageSize"
          :total="pagination.total"
          @current-change="handlePageChange"
        />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";

import { listAdminAnalysisTasks, type AdminAnalysisTaskItem } from "@/api/admin";
import { useAdminLocaleHelpers, useAdminMessages } from "@/utils/adminI18n";
import { formatDate, statusTagType } from "@/utils/format";

const loading = ref(false);
const rows = ref<AdminAnalysisTaskItem[]>([]);
const messages = useAdminMessages();
const t = computed(() => messages.value.tasks);
const { statusText: localeStatusText, taskTypeText } = useAdminLocaleHelpers();
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});
const filters = reactive({
  keyword: "",
  status: "",
  taskType: "",
});

async function loadTasks() {
  loading.value = true;
  try {
    const result = await listAdminAnalysisTasks({
      page: pagination.page,
      page_size: pagination.pageSize,
      keyword: filters.keyword || undefined,
      status: filters.status || undefined,
      task_type: filters.taskType || undefined,
    });
    rows.value = result.items;
    pagination.total = result.total;
  } finally {
    loading.value = false;
  }
}

function handleSearch() {
  pagination.page = 1;
  loadTasks();
}

function handlePageChange(page: number) {
  pagination.page = page;
  loadTasks();
}

onMounted(loadTasks);
</script>

<style scoped lang="scss">
.toolbar {
  margin-bottom: 16px;
  display: grid;
  grid-template-columns: minmax(240px, 1fr) 160px 160px;
  gap: 12px;
}

.pagination-row {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 900px) {
  .toolbar {
    grid-template-columns: 1fr;
  }
}
</style>
