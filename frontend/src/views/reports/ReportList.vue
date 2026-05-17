<template>
  <div class="app-page">
    <section class="hero-card">
      <p class="hero-kicker">Report Archive</p>
      <h1 class="hero-title">{{ t.reports.list.heroTitle }}</h1>
      <p class="hero-copy">{{ t.reports.list.heroCopy }}</p>
      <div class="action-row">
        <el-button type="primary" @click="router.push('/analysis/create')">{{ t.reports.list.actionCreate }}</el-button>
        <el-button @click="loadReports">{{ t.reports.list.actionRefresh }}</el-button>
      </div>
    </section>

    <section class="section-card">
      <div class="section-head">
        <div>
          <h2 class="section-title">{{ t.reports.list.sectionTitle }}</h2>
          <p class="section-copy">{{ sectionCopy }}</p>
        </div>
      </div>

      <el-empty v-if="!rows.length && !loading" :description="t.reports.list.empty" />

      <el-table v-else v-loading="loading" :data="rows" stripe>
        <el-table-column prop="resume_title" :label="t.reports.list.tableResume" min-width="180" />
        <el-table-column prop="job_title" :label="t.reports.list.tableJob" min-width="180" />
        <el-table-column :label="t.reports.list.tableTotalScore" width="90">
          <template #default="{ row }">{{ formatScore(row.total_score) }}</template>
        </el-table-column>
        <el-table-column :label="t.reports.list.tableMatchScore" width="90">
          <template #default="{ row }">{{ formatScore(row.match_score) }}</template>
        </el-table-column>
        <el-table-column prop="summary" :label="t.reports.list.tableSummary" min-width="280" show-overflow-tooltip />
        <el-table-column :label="t.reports.list.tableCreatedAt" min-width="160">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column :label="t.reports.list.tableAction" width="100" fixed="right">
          <template #default="{ row }">
            <el-button text type="primary" @click="router.push(`/reports/${row.id}`)">{{ t.reports.list.actionDetail }}</el-button>
          </template>
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
import { useRouter } from "vue-router";

import { listReports, type ReportListItem } from "@/api/reports";
import { formatDate, formatScore } from "@/utils/format";
import { useUserMessages } from "@/utils/userI18n";

const router = useRouter();
const messages = useUserMessages();
const t = computed(() => messages.value);
const loading = ref(false);
const rows = ref<ReportListItem[]>([]);
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

const sectionCopy = computed(() => t.value.reports.list.sectionCopy.replace("{total}", String(pagination.total)));

async function loadReports() {
  loading.value = true;
  try {
    const result = await listReports({
      page: pagination.page,
      page_size: pagination.pageSize,
    });
    rows.value = result.items;
    pagination.total = result.total;
  } finally {
    loading.value = false;
  }
}

function handlePageChange(page: number) {
  pagination.page = page;
  loadReports();
}

onMounted(loadReports);
</script>

<style scoped lang="scss">
.pagination-row {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
