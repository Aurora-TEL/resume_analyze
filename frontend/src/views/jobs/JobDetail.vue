<template>
  <div class="app-page" v-loading="loading">
    <section class="hero-card" v-if="detail">
      <p class="hero-kicker">Job Detail</p>
      <h1 class="hero-title">{{ detail.title }}</h1>
      <p class="hero-copy">
        当前解析状态为
        <el-tag :type="statusTagType(detail.parse_status)">{{ statusLabel(detail.parse_status) }}</el-tag>
        ，你可以继续补充文本、重跑解析或直接开始匹配分析。
      </p>
      <div class="action-row">
        <el-button type="primary" @click="handleSave">保存修改</el-button>
        <el-button @click="handleParse">重新解析</el-button>
        <el-button @click="router.push(`/analysis/create?jobId=${detail.id}`)">去分析</el-button>
        <el-button type="danger" plain @click="handleDelete">删除岗位</el-button>
      </div>
    </section>

    <div v-if="detail" class="two-column">
      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">岗位内容</h2>
            <p class="section-copy">可以直接在这里维护 JD 原文与基础信息。</p>
          </div>
        </div>

        <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
          <div class="form-grid">
            <el-form-item label="岗位名称" prop="title">
              <el-input v-model="form.title" maxlength="200" />
            </el-form-item>
            <el-form-item label="公司名称">
              <el-input v-model="form.company_name" maxlength="200" />
            </el-form-item>
            <el-form-item label="行业">
              <el-input v-model="form.industry" maxlength="100" />
            </el-form-item>
            <el-form-item label="工作地点">
              <el-input v-model="form.location" maxlength="100" />
            </el-form-item>
            <el-form-item label="薪资范围">
              <el-input v-model="form.salary_range" maxlength="100" />
            </el-form-item>
          </div>

          <el-form-item label="岗位描述" prop="description_text">
            <el-input v-model="form.description_text" type="textarea" :rows="14" />
          </el-form-item>
        </el-form>

        <el-alert v-if="detail.parse_error" type="warning" :closable="false" show-icon :title="detail.parse_error" />
      </section>

      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">解析结果</h2>
            <p class="section-copy">这里展示 AI 抽取出的技能、关键词和优先级。</p>
          </div>
        </div>

        <div class="summary-block">
          <h3>关键词</h3>
          <div class="pill-list">
            <el-tag
              v-for="keyword in keywordTags"
              :key="keyword"
              type="success"
              effect="plain"
            >
              {{ keyword }}
            </el-tag>
            <span v-if="!keywordTags.length">暂无关键词</span>
          </div>
        </div>

        <div class="summary-block">
          <h3>核心职责条目</h3>
          <p>{{ responsibilityCount }} 条</p>
        </div>

        <div class="summary-block">
          <h3>结构化 JSON</h3>
          <div class="json-panel">
            <pre>{{ structuredJson }}</pre>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from "element-plus";

import { deleteJob, getJobDetail, parseJob, updateJob, type JobDetail } from "@/api/jobs";
import { asArray, statusLabel, statusTagType } from "@/utils/format";

const route = useRoute();
const router = useRouter();
const formRef = ref<FormInstance>();
const loading = ref(false);
const detail = ref<JobDetail | null>(null);
const form = reactive({
  title: "",
  company_name: "",
  industry: "",
  location: "",
  salary_range: "",
  description_text: "",
});

const rules: FormRules = {
  title: [{ required: true, message: "请输入岗位名称", trigger: "blur" }],
  description_text: [{ required: true, message: "请输入岗位描述", trigger: "blur" }],
};

const structuredJson = computed(() => JSON.stringify(detail.value?.structured_data || {}, null, 2));
const keywordTags = computed(() =>
  asArray((detail.value?.structured_data as Record<string, any> | null)?.keywords).map((item) => String(item)).slice(0, 16),
);
const responsibilityCount = computed(() =>
  asArray((detail.value?.structured_data as Record<string, any> | null)?.core_responsibilities).length,
);

async function loadDetail() {
  loading.value = true;
  try {
    detail.value = await getJobDetail(String(route.params.id));
    Object.assign(form, {
      title: detail.value.title,
      company_name: detail.value.company_name || "",
      industry: detail.value.industry || "",
      location: detail.value.location || "",
      salary_range: detail.value.salary_range || "",
      description_text: detail.value.description_text,
    });
  } finally {
    loading.value = false;
  }
}

async function handleSave() {
  const valid = await formRef.value?.validate().catch(() => false);
  if (!valid) {
    return;
  }

  await updateJob(String(route.params.id), form);
  ElMessage.success("岗位已更新");
  await loadDetail();
}

async function handleParse() {
  await parseJob(String(route.params.id));
  ElMessage.success("岗位解析完成");
  await loadDetail();
}

async function handleDelete() {
  await ElMessageBox.confirm("删除后将从当前工作流中移除该岗位，确认继续吗？", "删除岗位", {
    type: "warning",
  });
  await deleteJob(String(route.params.id));
  ElMessage.success("岗位已删除");
  router.push("/jobs");
}

onMounted(loadDetail);
</script>

<style scoped lang="scss">
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0 16px;
}

.summary-block + .summary-block {
  margin-top: 20px;
}

.summary-block h3,
.summary-block p {
  margin: 0;
}

.summary-block h3 {
  margin-bottom: 10px;
}

@media (max-width: 800px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
