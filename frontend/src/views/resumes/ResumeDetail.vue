<template>
  <div class="app-page" v-loading="loading">
    <section class="hero-card" v-if="detail">
      <p class="hero-kicker">Resume Detail</p>
      <h1 class="hero-title">{{ detail.title }}</h1>
      <p class="hero-copy">
        当前解析状态为
        <el-tag :type="statusTagType(detail.parse_status)">{{ statusLabel(detail.parse_status) }}</el-tag>
        ，你可以重新解析、设为默认，或者直接发起岗位匹配分析。
      </p>
      <div class="action-row">
        <el-button type="primary" @click="handleParse">重新解析</el-button>
        <el-button @click="handleSetDefault">设为默认</el-button>
        <el-button @click="router.push(`/analysis/create?resumeId=${detail.id}`)">去分析</el-button>
        <el-button type="danger" plain @click="handleDelete">删除</el-button>
      </div>
    </section>

    <div v-if="detail" class="two-column">
      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">基本信息</h2>
            <p class="section-copy">这里保留文件信息、原文和原始结构化数据。</p>
          </div>
        </div>

        <el-descriptions :column="2" border>
          <el-descriptions-item label="文件名">{{ detail.file_name }}</el-descriptions-item>
          <el-descriptions-item label="文件类型">{{ detail.file_type.toUpperCase() }}</el-descriptions-item>
          <el-descriptions-item label="文件大小">{{ formatFileSize(detail.file_size) }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDate(detail.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ formatDate(detail.updated_at) }}</el-descriptions-item>
          <el-descriptions-item label="默认简历">
            <el-tag v-if="detail.is_default" type="success">是</el-tag>
            <span v-else>否</span>
          </el-descriptions-item>
        </el-descriptions>

        <div class="inline-form">
          <el-input v-model="titleDraft" maxlength="200" placeholder="修改简历标题" />
          <el-button @click="handleUpdateTitle">保存标题</el-button>
        </div>

        <el-alert v-if="detail.parse_error" type="warning" :closable="false" show-icon :title="detail.parse_error" />

        <el-tabs class="detail-tabs">
          <el-tab-pane label="原始文本">
            <div class="json-panel raw-panel">
              <pre>{{ detail.raw_text || "暂无提取文本" }}</pre>
            </div>
          </el-tab-pane>
          <el-tab-pane label="结构化 JSON">
            <div class="json-panel">
              <pre>{{ structuredJson }}</pre>
            </div>
          </el-tab-pane>
        </el-tabs>
      </section>

      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">解析摘要</h2>
            <p class="section-copy">从结构化结果里先提炼出最常用的信息。</p>
          </div>
        </div>

        <el-descriptions :column="1" border v-if="basicInfo">
          <el-descriptions-item label="姓名">{{ basicInfo.name || "-" }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ basicInfo.email || "-" }}</el-descriptions-item>
          <el-descriptions-item label="电话">{{ basicInfo.phone || "-" }}</el-descriptions-item>
          <el-descriptions-item label="目标岗位">{{ basicInfo.target_position || "-" }}</el-descriptions-item>
          <el-descriptions-item label="工作年限">{{ basicInfo.work_years || "-" }}</el-descriptions-item>
        </el-descriptions>

        <div class="summary-block">
          <h3>技能标签</h3>
          <div class="pill-list">
            <el-tag v-for="skill in skillTags" :key="skill" effect="plain">{{ skill }}</el-tag>
            <span v-if="!skillTags.length">暂无结构化技能标签</span>
          </div>
        </div>

        <div class="summary-block">
          <h3>教育经历条目</h3>
          <p>{{ educationCount }} 条</p>
        </div>

        <div class="summary-block">
          <h3>项目经历条目</h3>
          <p>{{ projectCount }} 条</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";

import { deleteResume, getResumeDetail, parseResume, updateResume, type ResumeDetail } from "@/api/resumes";
import { asArray, formatDate, formatFileSize, statusLabel, statusTagType } from "@/utils/format";

const route = useRoute();
const router = useRouter();

const loading = ref(false);
const detail = ref<ResumeDetail | null>(null);
const titleDraft = ref("");

const structuredJson = computed(() => JSON.stringify(detail.value?.structured_data || {}, null, 2));
const basicInfo = computed(() => (detail.value?.structured_data as Record<string, any> | null)?.basic_info || null);
const educationCount = computed(() => asArray((detail.value?.structured_data as Record<string, any> | null)?.education).length);
const projectCount = computed(() => asArray((detail.value?.structured_data as Record<string, any> | null)?.project_experience).length);
const skillTags = computed(() => {
  const skills = (detail.value?.structured_data as Record<string, any> | null)?.skills as Record<string, unknown> | undefined;
  if (!skills) {
    return [];
  }

  return Object.values(skills)
    .flatMap((value) => asArray(value))
    .map((item) => String(item))
    .filter(Boolean)
    .slice(0, 16);
});

async function loadDetail() {
  loading.value = true;
  try {
    detail.value = await getResumeDetail(String(route.params.id));
    titleDraft.value = detail.value.title;
  } finally {
    loading.value = false;
  }
}

async function handleParse() {
  await parseResume(String(route.params.id));
  ElMessage.success("简历解析完成");
  await loadDetail();
}

async function handleSetDefault() {
  await updateResume(String(route.params.id), { is_default: true });
  ElMessage.success("默认简历已更新");
  await loadDetail();
}

async function handleUpdateTitle() {
  if (!titleDraft.value.trim()) {
    ElMessage.warning("标题不能为空");
    return;
  }

  await updateResume(String(route.params.id), { title: titleDraft.value.trim() });
  ElMessage.success("标题已保存");
  await loadDetail();
}

async function handleDelete() {
  await ElMessageBox.confirm("删除后将从当前工作流中移除这份简历，确认继续吗？", "删除简历", {
    type: "warning",
  });
  await deleteResume(String(route.params.id));
  ElMessage.success("简历已删除");
  router.push("/resumes");
}

onMounted(loadDetail);
</script>

<style scoped lang="scss">
.inline-form {
  margin-top: 20px;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 12px;
}

.detail-tabs {
  margin-top: 20px;
}

.raw-panel {
  max-height: 420px;
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
</style>
