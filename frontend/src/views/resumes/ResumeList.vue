<template>
  <div class="app-page">
    <section class="hero-card">
      <p class="hero-kicker">Resume Center</p>
      <h1 class="hero-title">把可分析的简历整理成一个稳定入口。</h1>
      <p class="hero-copy">
        上传之后你可以重新解析、设为默认简历，或者直接带着它发起岗位匹配分析。
      </p>
      <div class="action-row">
        <el-button type="primary" @click="router.push('/resumes/upload')">上传简历</el-button>
        <el-button @click="loadResumes">刷新列表</el-button>
      </div>
    </section>

    <section class="section-card">
      <div class="section-head">
        <div>
          <h2 class="section-title">简历列表</h2>
          <p class="section-copy">当前共 {{ pagination.total }} 份简历。</p>
        </div>
        <el-input v-model="keyword" placeholder="按标题搜索" clearable style="max-width: 240px" @change="handleSearch" />
      </div>

      <el-empty v-if="!rows.length && !loading" description="还没有简历，先上传第一份吧。" />

      <el-table v-else v-loading="loading" :data="rows" stripe>
        <el-table-column prop="title" label="标题" min-width="180" />
        <el-table-column prop="file_name" label="文件名" min-width="180" />
        <el-table-column label="类型" width="90">
          <template #default="{ row }">{{ row.file_type.toUpperCase() }}</template>
        </el-table-column>
        <el-table-column label="大小" width="100">
          <template #default="{ row }">{{ formatFileSize(row.file_size) }}</template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.parse_status)">{{ statusLabel(row.parse_status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="默认" width="90">
          <template #default="{ row }">
            <el-tag v-if="row.is_default" type="success">默认</el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" min-width="160">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" min-width="260" fixed="right">
          <template #default="{ row }">
            <div class="row-actions">
              <el-button text type="primary" @click="router.push(`/resumes/${row.id}`)">详情</el-button>
              <el-button text @click="handleParse(row.id)">AI解析</el-button>
              <el-button text @click="handleSetDefault(row.id)">设默认</el-button>
              <el-button text @click="router.push(`/analysis/create?resumeId=${row.id}`)">去分析</el-button>
              <el-button text type="danger" @click="handleDelete(row.id)">删除</el-button>
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
import { onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessageBox, ElMessage } from "element-plus";

import { deleteResume, listResumes, parseResume, updateResume, type ResumeListItem } from "@/api/resumes";
import { formatDate, formatFileSize, statusLabel, statusTagType } from "@/utils/format";

const router = useRouter();
const loading = ref(false);
const keyword = ref("");
const rows = ref<ResumeListItem[]>([]);
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

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
  ElMessage.success("简历解析完成");
  await loadResumes();
}

async function handleSetDefault(resumeId: string) {
  await updateResume(resumeId, { is_default: true });
  ElMessage.success("默认简历已更新");
  await loadResumes();
}

async function handleDelete(resumeId: string) {
  await ElMessageBox.confirm("删除后将不再出现在当前列表中，确认继续吗？", "删除简历", {
    type: "warning",
  });
  await deleteResume(resumeId);
  ElMessage.success("简历已删除");
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
