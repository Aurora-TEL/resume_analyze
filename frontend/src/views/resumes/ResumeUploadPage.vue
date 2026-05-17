<template>
  <div class="app-page">
    <section class="hero-card">
      <p class="hero-kicker">Upload Flow</p>
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

      <el-form ref="formRef" :model="form" label-position="top">
        <el-form-item :label="t.modeLabel">
          <el-radio-group v-model="form.uploadMode">
            <el-radio-button value="file">{{ t.modeFile }}</el-radio-button>
            <el-radio-button value="text">{{ t.modeText }}</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-form-item :label="t.titleLabel">
          <el-input v-model="form.title" maxlength="200" :placeholder="t.titlePlaceholder" />
        </el-form-item>

        <el-form-item v-if="form.uploadMode === 'file'" :label="t.fileLabel">
          <el-upload
            class="upload-box"
            drag
            :auto-upload="false"
            :limit="1"
            :show-file-list="true"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
            accept=".pdf,.doc,.docx,.txt"
          >
            <div class="el-upload__text">{{ t.dropPrefix }} <em>{{ t.dropAction }}</em></div>
            <template #tip>
              <div class="el-upload__tip">{{ t.fileTip }}</div>
            </template>
          </el-upload>
        </el-form-item>

        <el-form-item v-else :label="t.textLabel">
          <el-input v-model="form.textContent" type="textarea" :rows="16" :placeholder="t.textPlaceholder" />
        </el-form-item>

        <el-form-item>
          <el-switch v-model="form.parseAfterUpload" />
          <span class="switch-label">{{ t.parseAfterUpload }}</span>
        </el-form-item>

        <div class="action-row">
          <el-button type="primary" :loading="submitting" @click="handleSubmit">{{ t.submit }}</el-button>
          <el-button @click="router.push('/resumes')">{{ t.back }}</el-button>
        </div>
      </el-form>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import type { UploadFile } from "element-plus";

import { parseResume, uploadResume } from "@/api/resumes";
import { useLocaleStore } from "@/stores/locale";

const zh = {
  heroTitle: "\u4e0a\u4f20\u4e00\u4efd\u53ef\u76f4\u63a5\u8fdb\u5165\u5206\u6790\u94fe\u8def\u7684\u7b80\u5386\u3002",
  heroCopy: "\u652f\u6301 PDF\u3001DOCX\u3001TXT\u3002\u9ed8\u8ba4\u4f1a\u5728\u4e0a\u4f20\u540e\u7ee7\u7eed\u89e6\u53d1\u4e00\u6b21 AI \u89e3\u6790\uff0c\u65b9\u4fbf\u4f60\u76f4\u63a5\u8fdb\u5165\u5c97\u4f4d\u5339\u914d\u3002",
  sectionTitle: "\u4e0a\u4f20\u8bbe\u7f6e",
  sectionCopy: "\u652f\u6301\u6587\u4ef6\u4e0a\u4f20\uff0c\u4e5f\u652f\u6301\u76f4\u63a5\u7c98\u8d34\u7b80\u5386\u6587\u672c\u751f\u6210 TXT \u63d0\u4ea4\u3002",
  modeLabel: "\u5f55\u5165\u65b9\u5f0f",
  modeFile: "\u4e0a\u4f20\u6587\u4ef6",
  modeText: "\u7c98\u8d34\u6587\u672c",
  titleLabel: "\u7b80\u5386\u6807\u9898",
  titlePlaceholder: "\u4f8b\u5982\uff1a\u540e\u7aef\u5f00\u53d1\u7b80\u5386 2026",
  fileLabel: "\u9009\u62e9\u6587\u4ef6",
  dropPrefix: "\u5c06\u6587\u4ef6\u62d6\u5230\u8fd9\u91cc\uff0c\u6216",
  dropAction: "\u70b9\u51fb\u9009\u62e9",
  fileTip: "\u652f\u6301 PDF / DOCX / TXT",
  textLabel: "\u7b80\u5386\u6587\u672c",
  textPlaceholder: "\u76f4\u63a5\u7c98\u8d34\u7b80\u5386\u539f\u6587\uff0c\u4f8b\u5982\u6559\u80b2\u7ecf\u5386\u3001\u5de5\u4f5c\u7ecf\u5386\u3001\u9879\u76ee\u7ecf\u5386\u548c\u6280\u80fd\u5217\u8868\u3002",
  parseAfterUpload: "\u4e0a\u4f20\u540e\u7acb\u5373\u6267\u884c AI \u89e3\u6790",
  submit: "\u4e0a\u4f20\u5e76\u7ee7\u7eed",
  back: "\u8fd4\u56de\u5217\u8868",
  warnPasteText: "\u8bf7\u5148\u7c98\u8d34\u7b80\u5386\u6587\u672c",
  warnSelectFile: "\u8bf7\u5148\u9009\u62e9\u4e00\u4efd\u7b80\u5386\u6587\u4ef6",
  success: "\u7b80\u5386\u4e0a\u4f20\u6210\u529f",
};

const en = {
  heroTitle: "Upload a resume that can move straight into the analysis flow.",
  heroCopy: "PDF, DOCX, and TXT are supported. By default, an AI parse runs right after upload so you can continue directly into job matching.",
  sectionTitle: "Upload Setup",
  sectionCopy: "You can upload a file or paste resume text directly and submit it as a generated TXT file.",
  modeLabel: "Input Mode",
  modeFile: "Upload File",
  modeText: "Paste Text",
  titleLabel: "Resume Title",
  titlePlaceholder: "For example: Backend Resume 2026",
  fileLabel: "Choose File",
  dropPrefix: "Drop the file here, or",
  dropAction: "click to select",
  fileTip: "Supports PDF / DOCX / TXT",
  textLabel: "Resume Text",
  textPlaceholder: "Paste the original resume text here, such as education, work experience, projects, and skills.",
  parseAfterUpload: "Run AI parsing immediately after upload",
  submit: "Upload and Continue",
  back: "Back to List",
  warnPasteText: "Please paste the resume text first",
  warnSelectFile: "Please choose a resume file first",
  success: "Resume uploaded successfully",
};

const router = useRouter();
const localeStore = useLocaleStore();
const t = computed(() => (localeStore.locale === "zh-CN" ? zh : en));
const submitting = ref(false);
const selectedFile = ref<File | null>(null);
const form = reactive({
  uploadMode: "file" as "file" | "text",
  title: "",
  textContent: "",
  parseAfterUpload: true,
});

function handleFileChange(file: UploadFile) {
  selectedFile.value = file.raw || null;
  if (!form.title && file.name) {
    form.title = file.name.replace(/\.[^.]+$/, "");
  }
}

function handleFileRemove() {
  selectedFile.value = null;
}

function buildTextResumeFile() {
  const trimmedText = form.textContent.trim();
  if (!trimmedText) {
    ElMessage.warning(t.value.warnPasteText);
    return null;
  }

  const baseName = (form.title.trim() || "resume-text").replace(/[\\/:*?\"<>|]+/g, "-").replace(/\s+/g, "-");

  return new File([trimmedText], `${baseName}.txt`, {
    type: "text/plain",
  });
}

async function handleSubmit() {
  const fileToUpload = form.uploadMode === "file" ? selectedFile.value : buildTextResumeFile();
  if (!fileToUpload) {
    if (form.uploadMode === "file") {
      ElMessage.warning(t.value.warnSelectFile);
    }
    return;
  }

  submitting.value = true;
  try {
    const formData = new FormData();
    formData.append("file", fileToUpload);
    if (form.title) {
      formData.append("title", form.title);
    }

    const result = await uploadResume(formData);
    if (form.parseAfterUpload) {
      await parseResume(result.resume_id);
    }
    ElMessage.success(t.value.success);
    router.push(`/resumes/${result.resume_id}`);
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped lang="scss">
.upload-box {
  width: 100%;
}

.switch-label {
  margin-left: 12px;
  color: var(--text-secondary);
}

:deep(.el-radio-button__inner) {
  min-width: 110px;
}
</style>
