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
          <el-option :label="localeStatusText('success')" value="success" />
          <el-option :label="localeStatusText('failed')" value="failed" />
        </el-select>
        <el-select v-model="filters.scene" clearable :placeholder="t.scenePlaceholder" @change="handleSearch">
          <el-option label="resume_parse" value="resume_parse" />
          <el-option label="job_parse" value="job_parse" />
          <el-option label="full_analysis" value="full_analysis" />
        </el-select>
      </div>

      <el-table v-loading="loading" :data="rows" stripe>
        <el-table-column prop="user_email" :label="t.user" min-width="180" />
        <el-table-column prop="scene" :label="t.scene" width="130" />
        <el-table-column prop="model_name" :label="t.model" min-width="130" />
        <el-table-column :label="t.status" width="100">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)">{{ localeStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column :label="t.tokens" width="110">
          <template #default="{ row }">{{ row.total_tokens || 0 }}</template>
        </el-table-column>
        <el-table-column :label="t.latency" width="100">
          <template #default="{ row }">{{ row.latency_ms ? `${row.latency_ms} ms` : "-" }}</template>
        </el-table-column>
        <el-table-column prop="prompt_template_name" :label="t.template" min-width="150" />
        <el-table-column :label="t.errorMessage" min-width="260" show-overflow-tooltip>
          <template #default="{ row }">{{ row.error_message || "-" }}</template>
        </el-table-column>
        <el-table-column :label="t.createdAt" min-width="160">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
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

import { listAdminApiLogs, type AdminApiLogItem } from "@/api/admin";
import { useAdminLocaleHelpers, useAdminMessages } from "@/utils/adminI18n";
import { formatDate, statusTagType } from "@/utils/format";

const loading = ref(false);
const rows = ref<AdminApiLogItem[]>([]);
const messages = useAdminMessages();
const t = computed(() => messages.value.apiLogs);
const { statusText: localeStatusText } = useAdminLocaleHelpers();
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});
const filters = reactive({
  keyword: "",
  status: "",
  scene: "",
});

async function loadLogs() {
  loading.value = true;
  try {
    const result = await listAdminApiLogs({
      page: pagination.page,
      page_size: pagination.pageSize,
      keyword: filters.keyword || undefined,
      status: filters.status || undefined,
      scene: filters.scene || undefined,
    });
    rows.value = result.items;
    pagination.total = result.total;
  } finally {
    loading.value = false;
  }
}

function handleSearch() {
  pagination.page = 1;
  loadLogs();
}

function handlePageChange(page: number) {
  pagination.page = page;
  loadLogs();
}

onMounted(loadLogs);
</script>

<style scoped lang="scss">
.toolbar {
  margin-bottom: 16px;
  display: grid;
  grid-template-columns: minmax(240px, 1fr) 150px 180px;
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
