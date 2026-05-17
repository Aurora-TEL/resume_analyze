<template>
  <div class="app-page">
    <section class="hero-card">
      <p class="hero-kicker">Report Archive</p>
      <h1 class="hero-title">把每一次分析结果沉淀成可复看的报告。</h1>
      <p class="hero-copy">
        这里适合回看不同岗位下的匹配差异，观察关键词覆盖和建议项的变化趋势。
      </p>
      <div class="action-row">
        <el-button type="primary" @click="router.push('/analysis/create')">新建分析</el-button>
        <el-button @click="loadReports">刷新列表</el-button>
      </div>
    </section>

    <section class="section-card">
      <div class="section-head">
        <div>
          <h2 class="section-title">报告列表</h2>
          <p class="section-copy">当前共 {{ pagination.total }} 份报告。</p>
        </div>
      </div>

      <el-empty v-if="!rows.length && !loading" description="还没有报告，先跑一条分析链路吧。" />

      <el-table v-else v-loading="loading" :data="rows" stripe>
        <el-table-column prop="resume_title" label="简历" min-width="180" />
        <el-table-column prop="job_title" label="岗位" min-width="180" />
        <el-table-column label="总分" width="90">
          <template #default="{ row }">{{ formatScore(row.total_score) }}</template>
        </el-table-column>
        <el-table-column label="匹配度" width="90">
          <template #default="{ row }">{{ formatScore(row.match_score) }}</template>
        </el-table-column>
        <el-table-column prop="summary" label="摘要" min-width="280" show-overflow-tooltip />
        <el-table-column label="生成时间" min-width="160">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button text type="primary" @click="router.push(`/reports/${row.id}`)">详情</el-button>
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

import { listReports, type ReportListItem } from "@/api/reports";
import { formatDate, formatScore } from "@/utils/format";

const router = useRouter();
const loading = ref(false);
const rows = ref<ReportListItem[]>([]);
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

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
