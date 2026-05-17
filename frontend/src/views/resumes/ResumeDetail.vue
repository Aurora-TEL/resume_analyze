<template>
  <div class="app-page" v-loading="loading">
    <section class="hero-card" v-if="detail">
      <p class="hero-kicker">Resume Detail</p>
      <h1 class="hero-title">{{ detail.title }}</h1>
      <p class="hero-copy">
        {{ t.statusPrefix }}
        <el-tag :type="statusTagType(detail.parse_status)">{{ statusLabel(detail.parse_status) }}</el-tag>
        {{ t.statusSuffix }}
      </p>
      <div class="action-row">
        <el-button type="primary" @click="handleParse">{{ t.actionParse }}</el-button>
        <el-button @click="handleSetDefault">{{ t.actionSetDefault }}</el-button>
        <el-button @click="router.push(`/analysis/create?resumeId=${detail.id}`)">{{ t.actionAnalyze }}</el-button>
        <el-button type="danger" plain @click="handleDelete">{{ t.actionDelete }}</el-button>
      </div>
    </section>

    <div v-if="detail" class="two-column">
      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">{{ t.basicTitle }}</h2>
            <p class="section-copy">{{ t.basicCopy }}</p>
          </div>
        </div>

        <el-descriptions :column="2" border>
          <el-descriptions-item :label="t.labelFileName">{{ detail.file_name }}</el-descriptions-item>
          <el-descriptions-item :label="t.labelFileType">{{ detail.file_type.toUpperCase() }}</el-descriptions-item>
          <el-descriptions-item :label="t.labelFileSize">{{ formatFileSize(detail.file_size) }}</el-descriptions-item>
          <el-descriptions-item :label="t.labelCreatedAt">{{ formatDate(detail.created_at) }}</el-descriptions-item>
          <el-descriptions-item :label="t.labelUpdatedAt">{{ formatDate(detail.updated_at) }}</el-descriptions-item>
          <el-descriptions-item :label="t.labelDefaultResume">
            <el-tag v-if="detail.is_default" type="success">{{ t.yes }}</el-tag>
            <span v-else>{{ t.no }}</span>
          </el-descriptions-item>
        </el-descriptions>

        <div class="inline-form">
          <el-input v-model="titleDraft" maxlength="200" :placeholder="t.titlePlaceholder" />
          <el-button @click="handleUpdateTitle">{{ t.saveTitle }}</el-button>
        </div>

        <el-alert v-if="detail.parse_error" type="warning" :closable="false" show-icon :title="detail.parse_error" />

        <el-tabs class="detail-tabs">
          <el-tab-pane :label="t.tabRawText">
            <div class="json-panel raw-panel">
              <pre>{{ detail.raw_text || t.emptyRawText }}</pre>
            </div>
          </el-tab-pane>
          <el-tab-pane :label="t.tabStructuredJson">
            <div class="json-panel">
              <pre>{{ structuredJson }}</pre>
            </div>
          </el-tab-pane>
        </el-tabs>
      </section>

      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">{{ t.summaryTitle }}</h2>
            <p class="section-copy">{{ t.summaryCopy }}</p>
          </div>
        </div>

        <el-descriptions :column="1" border v-if="basicInfo">
          <el-descriptions-item :label="t.labelName">{{ basicInfo.name || "-" }}</el-descriptions-item>
          <el-descriptions-item :label="t.labelEmail">{{ basicInfo.email || "-" }}</el-descriptions-item>
          <el-descriptions-item :label="t.labelPhone">{{ basicInfo.phone || "-" }}</el-descriptions-item>
          <el-descriptions-item :label="t.labelTargetPosition">{{ basicInfo.target_position || "-" }}</el-descriptions-item>
          <el-descriptions-item :label="t.labelWorkYears">{{ basicInfo.work_years || "-" }}</el-descriptions-item>
        </el-descriptions>

        <div class="summary-block">
          <h3>{{ t.skillsTitle }}</h3>
          <div class="pill-list">
            <el-tag v-for="skill in skillTags" :key="skill" effect="plain">{{ skill }}</el-tag>
            <span v-if="!skillTags.length">{{ t.emptySkills }}</span>
          </div>
        </div>

        <div class="summary-block">
          <h3>{{ t.educationTitle }}</h3>
          <p>{{ educationCount }} {{ t.itemUnit }}</p>
        </div>

        <div class="summary-block">
          <h3>{{ t.projectTitle }}</h3>
          <p>{{ projectCount }} {{ t.itemUnit }}</p>
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
import { useLocaleStore } from "@/stores/locale";
import { asArray, formatDate, formatFileSize, statusLabel, statusTagType } from "@/utils/format";

const zh = {
  statusPrefix: "\u5f53\u524d\u89e3\u6790\u72b6\u6001\u4e3a",
  statusSuffix: "\uff0c\u4f60\u53ef\u4ee5\u91cd\u65b0\u89e3\u6790\u3001\u8bbe\u4e3a\u9ed8\u8ba4\uff0c\u6216\u8005\u76f4\u63a5\u53d1\u8d77\u5c97\u4f4d\u5339\u914d\u5206\u6790\u3002",
  actionParse: "\u91cd\u65b0\u89e3\u6790",
  actionSetDefault: "\u8bbe\u4e3a\u9ed8\u8ba4",
  actionAnalyze: "\u53bb\u5206\u6790",
  actionDelete: "\u5220\u9664",
  basicTitle: "\u57fa\u672c\u4fe1\u606f",
  basicCopy: "\u8fd9\u91cc\u4fdd\u7559\u6587\u4ef6\u4fe1\u606f\u3001\u539f\u6587\u548c\u539f\u59cb\u7ed3\u6784\u5316\u6570\u636e\u3002",
  labelFileName: "\u6587\u4ef6\u540d",
  labelFileType: "\u6587\u4ef6\u7c7b\u578b",
  labelFileSize: "\u6587\u4ef6\u5927\u5c0f",
  labelCreatedAt: "\u521b\u5efa\u65f6\u95f4",
  labelUpdatedAt: "\u66f4\u65b0\u65f6\u95f4",
  labelDefaultResume: "\u9ed8\u8ba4\u7b80\u5386",
  yes: "\u662f",
  no: "\u5426",
  titlePlaceholder: "\u4fee\u6539\u7b80\u5386\u6807\u9898",
  saveTitle: "\u4fdd\u5b58\u6807\u9898",
  tabRawText: "\u539f\u59cb\u6587\u672c",
  tabStructuredJson: "\u7ed3\u6784\u5316 JSON",
  emptyRawText: "\u6682\u65e0\u63d0\u53d6\u6587\u672c",
  summaryTitle: "\u89e3\u6790\u6458\u8981",
  summaryCopy: "\u4ece\u7ed3\u6784\u5316\u7ed3\u679c\u91cc\u5148\u63d0\u70bc\u51fa\u6700\u5e38\u7528\u7684\u4fe1\u606f\u3002",
  labelName: "\u59d3\u540d",
  labelEmail: "\u90ae\u7bb1",
  labelPhone: "\u7535\u8bdd",
  labelTargetPosition: "\u76ee\u6807\u5c97\u4f4d",
  labelWorkYears: "\u5de5\u4f5c\u5e74\u9650",
  skillsTitle: "\u6280\u80fd\u6807\u7b7e",
  emptySkills: "\u6682\u65e0\u7ed3\u6784\u5316\u6280\u80fd\u6807\u7b7e",
  educationTitle: "\u6559\u80b2\u7ecf\u5386\u6761\u76ee",
  projectTitle: "\u9879\u76ee\u7ecf\u5386\u6761\u76ee",
  itemUnit: "\u6761",
  parseSuccess: "\u7b80\u5386\u89e3\u6790\u5b8c\u6210",
  defaultUpdated: "\u9ed8\u8ba4\u7b80\u5386\u5df2\u66f4\u65b0",
  titleRequired: "\u6807\u9898\u4e0d\u80fd\u4e3a\u7a7a",
  titleSaved: "\u6807\u9898\u5df2\u4fdd\u5b58",
  deleteConfirmTitle: "\u5220\u9664\u7b80\u5386",
  deleteConfirmMessage: "\u5220\u9664\u540e\u5c06\u4ece\u5f53\u524d\u5de5\u4f5c\u6d41\u4e2d\u79fb\u9664\u8fd9\u4efd\u7b80\u5386\uff0c\u786e\u8ba4\u7ee7\u7eed\u5417\uff1f",
  deleteSuccess: "\u7b80\u5386\u5df2\u5220\u9664",
};

const en = {
  statusPrefix: "Current parsing status is",
  statusSuffix: ", and you can re-run parsing, mark it as default, or start job matching analysis directly.",
  actionParse: "Re-parse",
  actionSetDefault: "Set Default",
  actionAnalyze: "Analyze",
  actionDelete: "Delete",
  basicTitle: "Basic Information",
  basicCopy: "This section keeps file metadata, extracted raw text, and the original structured output.",
  labelFileName: "File Name",
  labelFileType: "File Type",
  labelFileSize: "File Size",
  labelCreatedAt: "Created At",
  labelUpdatedAt: "Updated At",
  labelDefaultResume: "Default Resume",
  yes: "Yes",
  no: "No",
  titlePlaceholder: "Update the resume title",
  saveTitle: "Save Title",
  tabRawText: "Raw Text",
  tabStructuredJson: "Structured JSON",
  emptyRawText: "No extracted text yet",
  summaryTitle: "Parsed Summary",
  summaryCopy: "This section surfaces the most commonly used information from the structured result first.",
  labelName: "Name",
  labelEmail: "Email",
  labelPhone: "Phone",
  labelTargetPosition: "Target Position",
  labelWorkYears: "Work Years",
  skillsTitle: "Skill Tags",
  emptySkills: "No structured skill tags yet",
  educationTitle: "Education Items",
  projectTitle: "Project Items",
  itemUnit: "items",
  parseSuccess: "Resume parsing completed",
  defaultUpdated: "Default resume updated",
  titleRequired: "Title cannot be empty",
  titleSaved: "Title saved",
  deleteConfirmTitle: "Delete Resume",
  deleteConfirmMessage: "This resume will be removed from the current workflow. Do you want to continue?",
  deleteSuccess: "Resume deleted",
};

const route = useRoute();
const router = useRouter();
const localeStore = useLocaleStore();
const t = computed(() => (localeStore.locale === "zh-CN" ? zh : en));

const loading = ref(false);
const detail = ref<ResumeDetail | null>(null);
const titleDraft = ref("");

const structuredJson = computed(() => JSON.stringify(detail.value?.structured_data || {}, null, 2));
const basicInfo = computed(() => (detail.value?.structured_data as Record<string, any> | null)?.basic_info || null);
const educationCount = computed(() => asArray((detail.value?.structured_data as Record<string, any> | null)?.education).length);
const projectCount = computed(() =>
  asArray((detail.value?.structured_data as Record<string, any> | null)?.project_experience).length,
);
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
  ElMessage.success(t.value.parseSuccess);
  await loadDetail();
}

async function handleSetDefault() {
  await updateResume(String(route.params.id), { is_default: true });
  ElMessage.success(t.value.defaultUpdated);
  await loadDetail();
}

async function handleUpdateTitle() {
  if (!titleDraft.value.trim()) {
    ElMessage.warning(t.value.titleRequired);
    return;
  }

  await updateResume(String(route.params.id), { title: titleDraft.value.trim() });
  ElMessage.success(t.value.titleSaved);
  await loadDetail();
}

async function handleDelete() {
  await ElMessageBox.confirm(t.value.deleteConfirmMessage, t.value.deleteConfirmTitle, {
    type: "warning",
  });
  await deleteResume(String(route.params.id));
  ElMessage.success(t.value.deleteSuccess);
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
