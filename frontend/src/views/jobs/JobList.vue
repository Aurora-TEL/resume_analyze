<template>
  <div class="app-page">
    <section class="hero-card">
      <p class="hero-kicker">Job Center</p>
      <h1 class="hero-title">{{ t.jobs.list.heroTitle }}</h1>
      <p class="hero-copy">{{ t.jobs.list.heroCopy }}</p>
      <div class="action-row">
        <el-button type="primary" @click="router.push('/jobs/create')">{{ t.jobs.list.actionCreate }}</el-button>
        <el-button @click="loadJobs">{{ t.jobs.list.actionRefresh }}</el-button>
      </div>
    </section>

    <section class="section-card">
      <div class="section-head">
        <div>
          <h2 class="section-title">{{ t.jobs.list.sectionTitle }}</h2>
          <p class="section-copy">{{ sectionCopy }}</p>
        </div>
        <el-input
          v-model="keyword"
          :placeholder="t.jobs.list.searchPlaceholder"
          clearable
          style="max-width: 260px"
          @change="handleSearch"
        />
      </div>

      <el-empty v-if="!rows.length && !loading" :description="t.jobs.list.empty" />

      <el-table v-else v-loading="loading" :data="rows" stripe>
        <el-table-column prop="title" :label="t.jobs.list.tableTitle" min-width="180" />
        <el-table-column prop="company_name" :label="t.jobs.list.tableCompany" min-width="160" />
        <el-table-column prop="industry" :label="t.jobs.list.tableIndustry" min-width="120" />
        <el-table-column prop="location" :label="t.jobs.list.tableLocation" min-width="110" />
        <el-table-column :label="t.jobs.list.tableStatus" width="100">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.parse_status)">{{ statusLabel(row.parse_status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column :label="t.jobs.list.tableCreatedAt" min-width="160">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column :label="t.jobs.list.tableAction" min-width="240" fixed="right">
          <template #default="{ row }">
            <div class="row-actions">
              <el-button text type="primary" @click="router.push(`/jobs/${row.id}`)">{{ t.jobs.list.actionDetail }}</el-button>
              <el-button text @click="handleParse(row.id)">{{ t.jobs.list.actionParse }}</el-button>
              <el-button text @click="router.push(`/analysis/create?jobId=${row.id}`)">{{ t.jobs.list.actionAnalyze }}</el-button>
              <el-button text type="danger" @click="handleDelete(row.id)">{{ t.jobs.list.actionDelete }}</el-button>
            </div>
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
import { ElMessage, ElMessageBox } from "element-plus";

import { deleteJob, listJobs, parseJob, type JobListItem } from "@/api/jobs";
import { formatDate, statusLabel, statusTagType } from "@/utils/format";
import { useUserMessages } from "@/utils/userI18n";

const router = useRouter();
const messages = useUserMessages();
const t = computed(() => messages.value);
const loading = ref(false);
const keyword = ref("");
const rows = ref<JobListItem[]>([]);
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

const sectionCopy = computed(() => t.value.jobs.list.sectionCopy.replace("{total}", String(pagination.total)));

async function loadJobs() {
  loading.value = true;
  try {
    const result = await listJobs({
      page: pagination.page,
      page_size: pagination.pageSize,
      keyword: keyword.value || undefined,
    });
    rows.value = result.items;
    pagination.total = result.total;
  } finally {
    loading.value = false;
  }
}

async function handleParse(jobId: string) {
  await parseJob(jobId);
  ElMessage.success(t.value.jobs.list.parseSuccess);
  await loadJobs();
}

async function handleDelete(jobId: string) {
  await ElMessageBox.confirm(t.value.jobs.list.deleteConfirmMessage, t.value.jobs.list.deleteConfirmTitle, {
    type: "warning",
  });
  await deleteJob(jobId);
  ElMessage.success(t.value.jobs.list.deleteSuccess);
  if (rows.value.length === 1 && pagination.page > 1) {
    pagination.page -= 1;
  }
  await loadJobs();
}

function handlePageChange(page: number) {
  pagination.page = page;
  loadJobs();
}

function handleSearch() {
  pagination.page = 1;
  loadJobs();
}

onMounted(loadJobs);
</script>

<style scoped lang="scss">
.row-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 4px 8px;
}

.pagination-row {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
