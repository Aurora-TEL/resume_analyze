<template>
  <div class="app-page">
    <section class="hero-card">
      <p class="hero-kicker">Job Center</p>
      <h1 class="hero-title">把目标岗位整理成可匹配的结构化输入。</h1>
      <p class="hero-copy">
        岗位越清晰，后面的关键词覆盖、经验差距和建议项就越稳定。
      </p>
      <div class="action-row">
        <el-button type="primary" @click="router.push('/jobs/create')">创建岗位</el-button>
        <el-button @click="loadJobs">刷新列表</el-button>
      </div>
    </section>

    <section class="section-card">
      <div class="section-head">
        <div>
          <h2 class="section-title">岗位列表</h2>
          <p class="section-copy">当前共 {{ pagination.total }} 个岗位。</p>
        </div>
        <el-input v-model="keyword" placeholder="按岗位或公司搜索" clearable style="max-width: 260px" @change="handleSearch" />
      </div>

      <el-empty v-if="!rows.length && !loading" description="还没有岗位描述，先创建一个吧。" />

      <el-table v-else v-loading="loading" :data="rows" stripe>
        <el-table-column prop="title" label="岗位名称" min-width="180" />
        <el-table-column prop="company_name" label="公司" min-width="160" />
        <el-table-column prop="industry" label="行业" min-width="120" />
        <el-table-column prop="location" label="地点" min-width="110" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.parse_status)">{{ statusLabel(row.parse_status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" min-width="160">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" min-width="240" fixed="right">
          <template #default="{ row }">
            <div class="row-actions">
              <el-button text type="primary" @click="router.push(`/jobs/${row.id}`)">详情</el-button>
              <el-button text @click="handleParse(row.id)">重新解析</el-button>
              <el-button text @click="router.push(`/analysis/create?jobId=${row.id}`)">去分析</el-button>
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
import { ElMessage, ElMessageBox } from "element-plus";

import { deleteJob, listJobs, parseJob, type JobListItem } from "@/api/jobs";
import { formatDate, statusLabel, statusTagType } from "@/utils/format";

const router = useRouter();
const loading = ref(false);
const keyword = ref("");
const rows = ref<JobListItem[]>([]);
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

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
  ElMessage.success("岗位解析完成");
  await loadJobs();
}

async function handleDelete(jobId: string) {
  await ElMessageBox.confirm("删除后将不再出现在当前列表中，确认继续吗？", "删除岗位", {
    type: "warning",
  });
  await deleteJob(jobId);
  ElMessage.success("岗位已删除");
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
