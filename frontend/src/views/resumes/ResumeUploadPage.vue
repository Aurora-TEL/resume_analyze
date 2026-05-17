<template>
  <div class="app-page">
    <section class="hero-card">
      <p class="hero-kicker">Upload Flow</p>
      <h1 class="hero-title">上传一份可直接进入分析链路的简历。</h1>
      <p class="hero-copy">
        支持 PDF、DOCX、TXT。默认会在上传后继续触发一次 AI 解析，方便你直接进入岗位匹配。
      </p>
    </section>

    <section class="section-card">
      <div class="section-head">
        <div>
          <h2 class="section-title">上传设置</h2>
          <p class="section-copy">支持文件上传，也支持直接粘贴简历文本生成 TXT 提交。</p>
        </div>
      </div>

      <el-form ref="formRef" :model="form" label-position="top">
        <el-form-item label="录入方式">
          <el-radio-group v-model="form.uploadMode">
            <el-radio-button value="file">上传文件</el-radio-button>
            <el-radio-button value="text">粘贴文本</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="简历标题">
          <el-input v-model="form.title" maxlength="200" placeholder="例如：后端开发简历 2026" />
        </el-form-item>

        <el-form-item v-if="form.uploadMode === 'file'" label="选择文件">
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
            <div class="el-upload__text">将文件拖到这里，或 <em>点击选择</em></div>
            <template #tip>
              <div class="el-upload__tip">支持 PDF / DOCX / TXT</div>
            </template>
          </el-upload>
        </el-form-item>

        <el-form-item v-else label="简历文本">
          <el-input
            v-model="form.textContent"
            type="textarea"
            :rows="16"
            placeholder="直接粘贴简历原文，例如教育经历、工作经历、项目经历和技能列表。"
          />
        </el-form-item>

        <el-form-item>
          <el-switch v-model="form.parseAfterUpload" />
          <span class="switch-label">上传后立即执行 AI 解析</span>
        </el-form-item>

        <div class="action-row">
          <el-button type="primary" :loading="submitting" @click="handleSubmit">上传并继续</el-button>
          <el-button @click="router.push('/resumes')">返回列表</el-button>
        </div>
      </el-form>
    </section>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import type { UploadFile } from "element-plus";

import { parseResume, uploadResume } from "@/api/resumes";

const router = useRouter();
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
    ElMessage.warning("请先粘贴简历文本");
    return null;
  }

  const baseName = (form.title.trim() || "resume-text")
    .replace(/[\\/:*?\"<>|]+/g, "-")
    .replace(/\s+/g, "-");

  return new File([trimmedText], `${baseName}.txt`, {
    type: "text/plain",
  });
}

async function handleSubmit() {
  const fileToUpload = form.uploadMode === "file" ? selectedFile.value : buildTextResumeFile();
  if (!fileToUpload) {
    if (form.uploadMode === "file") {
      ElMessage.warning("请先选择一份简历文件");
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
    ElMessage.success("简历上传成功");
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
