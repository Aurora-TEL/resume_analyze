<template>
  <div class="app-page">
    <section class="hero-card">
      <p class="hero-kicker">Job Intake</p>
      <h1 class="hero-title">新建一个岗位描述，给后续匹配提供判断基准。</h1>
      <p class="hero-copy">
        创建时后端会自动尝试执行一次 AI 解析，你可以稍后在详情页继续编辑或重跑。
      </p>
    </section>

    <section class="section-card">
      <div class="section-head">
        <div>
          <h2 class="section-title">岗位信息</h2>
          <p class="section-copy">建议尽量贴近原始 JD，模型会从中提取关键词和要求。</p>
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
          <el-input v-model="form.description_text" type="textarea" :rows="14" placeholder="粘贴完整 JD 文本" />
        </el-form-item>

        <div class="action-row">
          <el-button type="primary" :loading="submitting" @click="handleSubmit">创建岗位</el-button>
          <el-button @click="router.push('/jobs')">返回列表</el-button>
        </div>
      </el-form>
    </section>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage, type FormInstance, type FormRules } from "element-plus";

import { createJob } from "@/api/jobs";

const router = useRouter();
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

const rules: FormRules = {
  title: [{ required: true, message: "请输入岗位名称", trigger: "blur" }],
  description_text: [{ required: true, message: "请输入岗位描述", trigger: "blur" }],
};

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false);
  if (!valid) {
    return;
  }

  submitting.value = true;
  try {
    const result = await createJob(form);
    ElMessage.success("岗位创建成功");
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
