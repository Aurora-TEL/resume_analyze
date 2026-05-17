<template>
  <div class="app-page">
    <section class="hero-card">
      <p class="hero-kicker">Job Intake</p>
      <h1 class="hero-title">{{ t.heroTitle }}</h1>
      <p class="hero-copy">{{ t.heroCopy }}</p>
    </section>

    <section class="section-card">
      <div class="section-head">
        <div>
          <h2 class="section-title">{{ t.sectionTitle }}</h2>
          <p class="section-copy">{{ t.sectionCopy }}</p>
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
          <el-input v-model="form.description_text" type="textarea" :rows="14" :placeholder="t.descriptionPlaceholder" />
        </el-form-item>

        <div class="action-row">
          <el-button type="primary" :loading="submitting" @click="handleSubmit">{{ t.submit }}</el-button>
          <el-button @click="router.push('/jobs')">{{ t.back }}</el-button>
        </div>
      </el-form>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage, type FormInstance, type FormRules } from "element-plus";

import { createJob } from "@/api/jobs";
import { useLocaleStore } from "@/stores/locale";

const zh = {
  heroTitle: "\u65b0\u5efa\u4e00\u4e2a\u5c97\u4f4d\u63cf\u8ff0\uff0c\u7ed9\u540e\u7eed\u5339\u914d\u63d0\u4f9b\u5224\u65ad\u57fa\u51c6\u3002",
  heroCopy: "\u521b\u5efa\u65f6\u540e\u7aef\u4f1a\u81ea\u52a8\u5c1d\u8bd5\u6267\u884c\u4e00\u6b21 AI \u89e3\u6790\uff0c\u4f60\u53ef\u4ee5\u7a0d\u540e\u5728\u8be6\u60c5\u9875\u7ee7\u7eed\u7f16\u8f91\u6216\u91cd\u8dd1\u3002",
  sectionTitle: "\u5c97\u4f4d\u4fe1\u606f",
  sectionCopy: "\u5efa\u8bae\u5c3d\u91cf\u8d34\u8fd1\u539f\u59cb JD\uff0c\u6a21\u578b\u4f1a\u4ece\u4e2d\u63d0\u53d6\u5173\u952e\u8bcd\u548c\u8981\u6c42\u3002",
  labelTitle: "\u5c97\u4f4d\u540d\u79f0",
  labelCompany: "\u516c\u53f8\u540d\u79f0",
  labelIndustry: "\u884c\u4e1a",
  labelLocation: "\u5de5\u4f5c\u5730\u70b9",
  labelSalary: "\u85aa\u8d44\u8303\u56f4",
  labelDescription: "\u5c97\u4f4d\u63cf\u8ff0",
  descriptionPlaceholder: "\u7c98\u8d34\u5b8c\u6574 JD \u6587\u672c",
  submit: "\u521b\u5efa\u5c97\u4f4d",
  back: "\u8fd4\u56de\u5217\u8868",
  validationTitle: "\u8bf7\u8f93\u5165\u5c97\u4f4d\u540d\u79f0",
  validationDescription: "\u8bf7\u8f93\u5165\u5c97\u4f4d\u63cf\u8ff0",
  success: "\u5c97\u4f4d\u521b\u5efa\u6210\u529f",
};

const en = {
  heroTitle: "Create a job description and give the matching flow a clear judging baseline.",
  heroCopy: "After creation, the backend will automatically try one AI parsing pass. You can keep editing or rerun it later on the detail page.",
  sectionTitle: "Job Information",
  sectionCopy: "It is best to stay close to the original JD so the model can extract keywords and requirements accurately.",
  labelTitle: "Job Title",
  labelCompany: "Company Name",
  labelIndustry: "Industry",
  labelLocation: "Work Location",
  labelSalary: "Salary Range",
  labelDescription: "Job Description",
  descriptionPlaceholder: "Paste the full JD text",
  submit: "Create Job",
  back: "Back to List",
  validationTitle: "Please enter the job title",
  validationDescription: "Please enter the job description",
  success: "Job created successfully",
};

const router = useRouter();
const localeStore = useLocaleStore();
const t = computed(() => (localeStore.locale === "zh-CN" ? zh : en));
const formRef = ref<FormInstance>();
const submitting = ref(false);

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

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false);
  if (!valid) {
    return;
  }

  submitting.value = true;
  try {
    const result = await createJob(form);
    ElMessage.success(t.value.success);
    router.push(`/jobs/${result.job_id}`);
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped lang="scss">
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0 16px;
}

@media (max-width: 800px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
