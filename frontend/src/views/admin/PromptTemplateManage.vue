<template>
  <div class="app-page">
    <section class="section-card">
      <div class="section-head">
        <div>
          <h2 class="section-title">{{ t.title }}</h2>
          <p class="section-copy">{{ t.copy }}</p>
        </div>
        <el-button type="primary" @click="openCreateDialog">{{ t.newTemplate }}</el-button>
      </div>

      <div class="toolbar">
        <el-input v-model="filters.keyword" :placeholder="t.searchPlaceholder" clearable @change="handleSearch" />
        <el-select v-model="filters.scene" clearable :placeholder="t.scenePlaceholder" @change="handleSearch">
          <el-option label="resume_parse" value="resume_parse" />
          <el-option label="job_parse" value="job_parse" />
          <el-option label="full_analysis" value="full_analysis" />
        </el-select>
        <el-select v-model="filters.status" clearable :placeholder="t.statusPlaceholder" @change="handleSearch">
          <el-option :label="localeStatusText('active')" value="active" />
          <el-option :label="localeStatusText('inactive')" value="inactive" />
          <el-option :label="localeStatusText('deleted')" value="deleted" />
        </el-select>
      </div>

      <el-table v-loading="loading" :data="rows" stripe>
        <el-table-column prop="name" :label="t.name" min-width="180" />
        <el-table-column prop="scene" :label="t.scene" width="140" />
        <el-table-column prop="version" :label="t.version" width="90" />
        <el-table-column :label="t.status" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : row.status === 'inactive' ? 'warning' : 'info'">
              {{ localeStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_by_email" :label="t.editor" min-width="180" />
        <el-table-column prop="description" :label="t.description" min-width="220" show-overflow-tooltip />
        <el-table-column :label="t.updatedAt" min-width="160">
          <template #default="{ row }">{{ formatDate(row.updated_at) }}</template>
        </el-table-column>
        <el-table-column :label="t.actions" width="160" fixed="right">
          <template #default="{ row }">
            <div class="row-actions">
              <el-button text type="primary" @click="openEditDialog(row)">{{ t.edit }}</el-button>
              <el-button text type="danger" @click="handleDelete(row.id)">{{ t.delete }}</el-button>
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

    <el-dialog v-model="dialogVisible" :title="editingId ? t.editTitle : t.createTitle" width="760px">
      <el-form :model="form" label-position="top">
        <div class="form-grid">
          <el-form-item :label="t.formName">
            <el-input v-model="form.name" />
          </el-form-item>
          <el-form-item :label="t.formScene">
            <el-select v-model="form.scene" style="width: 100%">
              <el-option label="resume_parse" value="resume_parse" />
              <el-option label="job_parse" value="job_parse" />
              <el-option label="full_analysis" value="full_analysis" />
            </el-select>
          </el-form-item>
          <el-form-item :label="t.formVersion">
            <el-input-number v-model="form.version" :min="1" />
          </el-form-item>
          <el-form-item :label="t.formStatus">
            <el-select v-model="form.status" style="width: 100%">
              <el-option :label="localeStatusText('active')" value="active" />
              <el-option :label="localeStatusText('inactive')" value="inactive" />
            </el-select>
          </el-form-item>
        </div>
        <el-form-item :label="t.formDescription">
          <el-input v-model="form.description" />
        </el-form-item>
        <el-form-item :label="t.formContent">
          <el-input v-model="form.content" type="textarea" :rows="14" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">{{ t.cancel }}</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">{{ t.save }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";

import {
  createPromptTemplate,
  deletePromptTemplate,
  listPromptTemplates,
  updatePromptTemplate,
  type PromptTemplateItem,
  type PromptTemplatePayload,
} from "@/api/admin";
import { useAdminLocaleHelpers, useAdminMessages } from "@/utils/adminI18n";
import { formatDate } from "@/utils/format";

const loading = ref(false);
const submitting = ref(false);
const dialogVisible = ref(false);
const editingId = ref<string>("");
const rows = ref<PromptTemplateItem[]>([]);
const messages = useAdminMessages();
const t = computed(() => messages.value.promptTemplates);
const { statusText: localeStatusText } = useAdminLocaleHelpers();
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});
const filters = reactive({
  keyword: "",
  scene: "",
  status: "",
});
const form = reactive<PromptTemplatePayload>({
  name: "",
  scene: "resume_parse",
  version: 1,
  status: "active",
  description: "",
  content: "",
});

function resetForm() {
  form.name = "";
  form.scene = "resume_parse";
  form.version = 1;
  form.status = "active";
  form.description = "";
  form.content = "";
}

async function loadTemplates() {
  loading.value = true;
  try {
    const result = await listPromptTemplates({
      page: pagination.page,
      page_size: pagination.pageSize,
      keyword: filters.keyword || undefined,
      scene: filters.scene || undefined,
      status: filters.status || undefined,
    });
    rows.value = result.items;
    pagination.total = result.total;
  } finally {
    loading.value = false;
  }
}

function handleSearch() {
  pagination.page = 1;
  loadTemplates();
}

function handlePageChange(page: number) {
  pagination.page = page;
  loadTemplates();
}

function openCreateDialog() {
  editingId.value = "";
  resetForm();
  dialogVisible.value = true;
}

function openEditDialog(row: PromptTemplateItem) {
  editingId.value = row.id;
  form.name = row.name;
  form.scene = row.scene;
  form.version = row.version;
  form.status = row.status;
  form.description = row.description || "";
  form.content = row.content;
  dialogVisible.value = true;
}

async function handleSubmit() {
  submitting.value = true;
  try {
    if (editingId.value) {
      await updatePromptTemplate(editingId.value, form);
      ElMessage.success(t.value.updateSuccess);
    } else {
      await createPromptTemplate(form);
      ElMessage.success(t.value.createSuccess);
    }
    dialogVisible.value = false;
    await loadTemplates();
  } finally {
    submitting.value = false;
  }
}

async function handleDelete(templateId: string) {
  await ElMessageBox.confirm(t.value.deleteConfirmMessage, t.value.deleteConfirmTitle, {
    type: "warning",
  });
  await deletePromptTemplate(templateId);
  ElMessage.success(t.value.deleteSuccess);
  await loadTemplates();
}

onMounted(loadTemplates);
</script>

<style scoped lang="scss">
.toolbar {
  margin-bottom: 16px;
  display: grid;
  grid-template-columns: minmax(240px, 1fr) 180px 160px;
  gap: 12px;
}

.row-actions {
  display: flex;
  gap: 8px;
}

.pagination-row {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0 16px;
}

@media (max-width: 900px) {
  .toolbar,
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
