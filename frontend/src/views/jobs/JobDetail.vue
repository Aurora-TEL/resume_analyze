<template>
  <div class="app-page" v-loading="loading">
    <section class="hero-card" v-if="detail">
      <p class="hero-kicker">Job Detail</p>
      <h1 class="hero-title">{{ detail.title }}</h1>
      <p class="hero-copy">
        {{ t.statusPrefix }}
        <el-tag :type="statusTagType(detail.parse_status)">{{ statusLabel(detail.parse_status) }}</el-tag>
        {{ t.statusSuffix }}
      </p>
      <div class="action-row">
        <el-button type="primary" @click="handleSave">{{ t.actionSave }}</el-button>
        <el-button @click="handleParse">{{ t.actionParse }}</el-button>
        <el-button @click="router.push(`/analysis/create?jobId=${detail.id}`)">{{ t.actionAnalyze }}</el-button>
        <el-button type="danger" plain @click="handleDelete">{{ t.actionDelete }}</el-button>
      </div>
    </section>

    <div v-if="detail" class="two-column">
      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">{{ t.contentTitle }}</h2>
            <p class="section-copy">{{ t.contentCopy }}</p>
          </div>
        </div>

        <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
          <div class="form-grid">
            <el-form-item :label="t.labelTitle" prop="title">
              <el-input v-model="form.title" maxlength="200" />
            </el-form-item>
            <el-form-item :label="t.labelCompany">
              <el-input v-model="form.company_name" maxlength="200" />
            </el-form-item>
            <el-form-item :label="t.labelIndustry">
              <el-input v-model="form.industry" maxlength="100" />
            </el-form-item>
            <el-form-item :label="t.labelLocation">
              <el-input v-model="form.location" maxlength="100" />
            </el-form-item>
            <el-form-item :label="t.labelSalary">
              <el-input v-model="form.salary_range" maxlength="100" />
            </el-form-item>
          </div>

          <el-form-item :label="t.labelDescription" prop="description_text">
            <el-input v-model="form.description_text" type="textarea" :rows="14" />
          </el-form-item>
        </el-form>

        <el-alert v-if="detail.parse_error" type="warning" :closable="false" show-icon :title="detail.parse_error" />
      </section>

      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">{{ t.resultTitle }}</h2>
            <p class="section-copy">{{ t.resultCopy }}</p>
          </div>
        </div>

        <div class="summary-block">
          <h3>{{ t.keywordsTitle }}</h3>
          <div class="pill-list">
            <el-tag v-for="keyword in keywordTags" :key="keyword" type="success" effect="plain">{{ keyword }}</el-tag>
            <span v-if="!keywordTags.length">{{ t.emptyKeywords }}</span>
          </div>
        </div>

        <div class="summary-block">
          <h3>{{ t.responsibilityTitle }}</h3>
          <p>{{ responsibilityCount }} {{ t.itemUnit }}</p>
        </div>

        <div class="summary-block">
          <h3>{{ t.structuredJsonTitle }}</h3>
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
import { useLocaleStore } from "@/stores/locale";
import { asArray, statusLabel, statusTagType } from "@/utils/format";

const zh = {
  statusPrefix: "\u5f53\u524d\u89e3\u6790\u72b6\u6001\u4e3a",
  statusSuffix: "\uff0c\u4f60\u53ef\u4ee5\u7ee7\u7eed\u8865\u5145\u6587\u672c\u3001\u91cd\u8dd1\u89e3\u6790\u6216\u76f4\u63a5\u5f00\u59cb\u5339\u914d\u5206\u6790\u3002",
  actionSave: "\u4fdd\u5b58\u4fee\u6539",
  actionParse: "\u91cd\u65b0\u89e3\u6790",
  actionAnalyze: "\u53bb\u5206\u6790",
  actionDelete: "\u5220\u9664\u5c97\u4f4d",
  contentTitle: "\u5c97\u4f4d\u5185\u5bb9",
  contentCopy: "\u53ef\u4ee5\u76f4\u63a5\u5728\u8fd9\u91cc\u7ef4\u62a4 JD \u539f\u6587\u4e0e\u57fa\u7840\u4fe1\u606f\u3002",
  labelTitle: "\u5c97\u4f4d\u540d\u79f0",
  labelCompany: "\u516c\u53f8\u540d\u79f0",
  labelIndustry: "\u884c\u4e1a",
  labelLocation: "\u5de5\u4f5c\u5730\u70b9",
  labelSalary: "\u85aa\u8d44\u8303\u56f4",
  labelDescription: "\u5c97\u4f4d\u63cf\u8ff0",
  resultTitle: "\u89e3\u6790\u7ed3\u679c",
  resultCopy: "\u8fd9\u91cc\u5c55\u793a AI \u62bd\u53d6\u51fa\u7684\u6280\u80fd\u3001\u5173\u952e\u8bcd\u548c\u4f18\u5148\u7ea7\u3002",
  keywordsTitle: "\u5173\u952e\u8bcd",
  emptyKeywords: "\u6682\u65e0\u5173\u952e\u8bcd",
  responsibilityTitle: "\u6838\u5fc3\u804c\u8d23\u6761\u76ee",
  structuredJsonTitle: "\u7ed3\u6784\u5316 JSON",
  itemUnit: "\u6761",
  validationTitle: "\u8bf7\u8f93\u5165\u5c97\u4f4d\u540d\u79f0",
  validationDescription: "\u8bf7\u8f93\u5165\u5c97\u4f4d\u63cf\u8ff0",
  saveSuccess: "\u5c97\u4f4d\u5df2\u66f4\u65b0",
  parseSuccess: "\u5c97\u4f4d\u89e3\u6790\u5b8c\u6210",
  deleteConfirmTitle: "\u5220\u9664\u5c97\u4f4d",
  deleteConfirmMessage: "\u5220\u9664\u540e\u5c06\u4ece\u5f53\u524d\u5de5\u4f5c\u6d41\u4e2d\u79fb\u9664\u8be5\u5c97\u4f4d\uff0c\u786e\u8ba4\u7ee7\u7eed\u5417\uff1f",
  deleteSuccess: "\u5c97\u4f4d\u5df2\u5220\u9664",
};

const en = {
  statusPrefix: "Current parsing status is",
  statusSuffix: ", and you can continue editing the text, rerun parsing, or start matching analysis directly.",
  actionSave: "Save Changes",
  actionParse: "Re-parse",
  actionAnalyze: "Analyze",
  actionDelete: "Delete Job",
  contentTitle: "Job Content",
  contentCopy: "You can maintain the raw JD text and basic metadata directly here.",
  labelTitle: "Job Title",
  labelCompany: "Company Name",
  labelIndustry: "Industry",
  labelLocation: "Work Location",
  labelSalary: "Salary Range",
  labelDescription: "Job Description",
  resultTitle: "Parsed Result",
  resultCopy: "This section shows the skills, keywords, and priorities extracted by AI.",
  keywordsTitle: "Keywords",
  emptyKeywords: "No keywords yet",
  responsibilityTitle: "Core Responsibility Items",
  structuredJsonTitle: "Structured JSON",
  itemUnit: "items",
  validationTitle: "Please enter the job title",
  validationDescription: "Please enter the job description",
  saveSuccess: "Job updated",
  parseSuccess: "Job parsing completed",
  deleteConfirmTitle: "Delete Job",
  deleteConfirmMessage: "This job will be removed from the current workflow. Do you want to continue?",
  deleteSuccess: "Job deleted",
};

const route = useRoute();
const router = useRouter();
const localeStore = useLocaleStore();
const t = computed(() => (localeStore.locale === "zh-CN" ? zh : en));
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

const rules = computed<FormRules>(() => ({
  title: [{ required: true, message: t.value.validationTitle, trigger: "blur" }],
  description_text: [{ required: true, message: t.value.validationDescription, trigger: "blur" }],
}));

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
  ElMessage.success(t.value.saveSuccess);
  await loadDetail();
}

async function handleParse() {
  await parseJob(String(route.params.id));
  ElMessage.success(t.value.parseSuccess);
  await loadDetail();
}

async function handleDelete() {
  await ElMessageBox.confirm(t.value.deleteConfirmMessage, t.value.deleteConfirmTitle, {
    type: "warning",
  });
  await deleteJob(String(route.params.id));
  ElMessage.success(t.value.deleteSuccess);
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
