<template>
  <div class="app-page">
    <section class="hero-card">
      <p class="hero-kicker">Resume Center</p>
      <h1 class="hero-title">{{ t.resumes.list.heroTitle }}</h1>
      <p class="hero-copy">{{ t.resumes.list.heroCopy }}</p>
      <div class="action-row">
        <el-button type="primary" @click="router.push('/resumes/upload')">{{ t.resumes.list.actionUpload }}</el-button>
        <el-button @click="loadResumes">{{ t.resumes.list.actionRefresh }}</el-button>
      </div>
    </section>

    <section class="section-card">
      <div class="section-head">
        <div>
          <h2 class="section-title">{{ t.resumes.list.sectionTitle }}</h2>
          <p class="section-copy">{{ sectionCopy }}</p>
        </div>
        <el-input
          v-model="keyword"
          :placeholder="t.resumes.list.searchPlaceholder"
          clearable
          style="max-width: 240px"
          @change="handleSearch"
        />
      </div>

      <el-empty v-if="!rows.length && !loading" :description="t.resumes.list.empty" />

      <el-table v-else v-loading="loading" :data="rows" stripe>
        <el-table-column prop="title" :label="t.resumes.list.tableTitle" min-width="180" />
        <el-table-column prop="file_name" :label="t.resumes.list.tableFileName" min-width="180" />
        <el-table-column :label="t.resumes.list.tableType" width="90">
          <template #default="{ row }">{{ row.file_type.toUpperCase() }}</template>
        </el-table-column>
        <el-table-column :label="t.resumes.list.tableSize" width="100">
          <template #default="{ row }">{{ formatFileSize(row.file_size) }}</template>
        </el-table-column>
        <el-table-column :label="t.resumes.list.tableStatus" width="100">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.parse_status)">{{ statusLabel(row.parse_status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column :label="t.resumes.list.tableDefault" width="90">
          <template #default="{ row }">
            <el-tag v-if="row.is_default" type="success">{{ t.resumes.list.defaultYes }}</el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column :label="t.resumes.list.tableCreatedAt" min-width="160">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column :label="t.resumes.list.tableAction" min-width="260" fixed="right">
          <template #default="{ row }">
            <div class="row-actions">
              <el-button text type="primary" @click="router.push(`/resumes/${row.id}`)">{{ t.resumes.list.actionDetail }}</el-button>
              <el-button text @click="handleParse(row.id)">{{ t.resumes.list.actionParse }}</el-button>
              <el-button text @click="handleSetDefault(row.id)">{{ t.resumes.list.actionSetDefault }}</el-button>
              <el-button text @click="router.push(`/analysis/create?resumeId=${row.id}`)">{{ t.resumes.list.actionAnalyze }}</el-button>
              <el-button text type="danger" @click="handleDelete(row.id)">{{ t.resumes.list.actionDelete }}</el-button>
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

import { deleteResume, listResumes, parseResume, updateResume, type ResumeListItem } from "@/api/resumes";
import { formatDate, formatFileSize, statusLabel, statusTagType } from "@/utils/format";
import { useUserMessages } from "@/utils/userI18n";

const router = useRouter();
const messages = useUserMessages();
const t = computed(() => messages.value);
const loading = ref(false);
const keyword = ref("");
const rows = ref<ResumeListItem[]>([]);
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

const sectionCopy = computed(() => t.value.resumes.list.sectionCopy.replace("{total}", String(pagination.total)));

async function loadResumes() {
  loading.value = true;
  try {
    const result = await listResumes({
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

async function handleParse(resumeId: string) {
  await parseResume(resumeId);
  ElMessage.success(t.value.resumes.list.parseSuccess);
  await loadResumes();
}

async function handleSetDefault(resumeId: string) {
  await updateResume(resumeId, { is_default: true });
  ElMessage.success(t.value.resumes.list.defaultUpdated);
  await loadResumes();
}

async function handleDelete(resumeId: string) {
  await ElMessageBox.confirm(t.value.resumes.list.deleteConfirmMessage, t.value.resumes.list.deleteConfirmTitle, {
    type: "warning",
  });
  await deleteResume(resumeId);
  ElMessage.success(t.value.resumes.list.deleteSuccess);
  if (rows.value.length === 1 && pagination.page > 1) {
    pagination.page -= 1;
  }
  await loadResumes();
}

function handlePageChange(page: number) {
  pagination.page = page;
  loadResumes();
}

function handleSearch() {
  pagination.page = 1;
  loadResumes();
}

onMounted(loadResumes);
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
