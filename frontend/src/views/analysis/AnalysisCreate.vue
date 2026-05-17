<template>
  <div class="app-page">
    <section class="hero-card">
      <p class="hero-kicker">Full Analysis</p>
      <h1 class="hero-title">把简历和岗位放在一起，直接生成完整分析报告。</h1>
      <p class="hero-copy">
        当前 MVP 默认执行 <code>full_analysis</code>。接口会同步返回结果，所以成功后会直接跳到报告页。
      </p>
    </section>

    <section class="section-card">
      <div class="section-head">
        <div>
          <h2 class="section-title">分析配置</h2>
          <p class="section-copy">先选择一份简历，再选择一个岗位。</p>
        </div>
      </div>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <el-form-item label="选择简历" prop="resume_id">
          <el-select v-model="form.resume_id" placeholder="请选择简历" filterable style="width: 100%">
            <el-option v-for="item in resumes" :key="item.id" :label="item.title" :value="item.id" />
          </el-select>
        </el-form-item>

        <el-form-item label="选择岗位" prop="job_description_id">
          <el-select v-model="form.job_description_id" placeholder="请选择岗位" filterable style="width: 100%">
            <el-option
              v-for="item in jobs"
              :key="item.id"
              :label="`${item.title}${item.company_name ? ` / ${item.company_name}` : ''}`"
              :value="item.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="分析类型">
          <el-input model-value="full_analysis" disabled />
        </el-form-item>

        <div class="action-row">
          <el-button type="primary" :loading="submitting" @click="handleSubmit">开始分析</el-button>
          <el-button @click="router.push('/reports')">查看已有报告</el-button>
        </div>
      </el-form>
    </section>

    <section class="two-column">
      <article class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">可用简历</h2>
            <p class="section-copy">建议优先选择已完成 AI 解析的简历。</p>
          </div>
        </div>
        <el-empty v-if="!resumes.length && !loading" description="还没有简历，先上传一份吧。" />
        <div v-else class="selection-list">
          <button
            v-for="item in resumes"
            :key="item.id"
            class="selection-card"
            :class="{ active: form.resume_id === item.id }"
            @click="form.resume_id = item.id"
          >
            <strong>{{ item.title }}</strong>
            <span>{{ statusLabel(item.parse_status) }}</span>
          </button>
        </div>
      </article>

      <article class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">可用岗位</h2>
            <p class="section-copy">建议选择已经检查过 JD 内容的岗位。</p>
          </div>
        </div>
        <el-empty v-if="!jobs.length && !loading" description="还没有岗位，先创建一个吧。" />
        <div v-else class="selection-list">
          <button
            v-for="item in jobs"
            :key="item.id"
            class="selection-card"
            :class="{ active: form.job_description_id === item.id }"
            @click="form.job_description_id = item.id"
          >
            <strong>{{ item.title }}</strong>
            <span>{{ item.company_name || "未填写公司" }}</span>
          </button>
        </div>
      </article>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage, type FormInstance, type FormRules } from "element-plus";

import { createAnalysisTask } from "@/api/analysis";
import { listJobs, type JobListItem } from "@/api/jobs";
import { listResumes, type ResumeListItem } from "@/api/resumes";
import { statusLabel } from "@/utils/format";

const route = useRoute();
const router = useRouter();
const formRef = ref<FormInstance>();
const loading = ref(false);
const submitting = ref(false);
const resumes = ref<ResumeListItem[]>([]);
const jobs = ref<JobListItem[]>([]);

const form = reactive({
  resume_id: "",
  job_description_id: "",
  task_type: "full_analysis" as const,
});

const rules: FormRules = {
  resume_id: [{ required: true, message: "请选择简历", trigger: "change" }],
  job_description_id: [{ required: true, message: "请选择岗位", trigger: "change" }],
};

async function loadOptions() {
  loading.value = true;
  try {
    const [resumeResult, jobResult] = await Promise.all([
      listResumes({ page: 1, page_size: 100 }),
      listJobs({ page: 1, page_size: 100 }),
    ]);
    resumes.value = resumeResult.items;
    jobs.value = jobResult.items;

    form.resume_id = String(route.query.resumeId || resumes.value[0]?.id || "");
    form.job_description_id = String(route.query.jobId || jobs.value[0]?.id || "");
  } finally {
    loading.value = false;
  }
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false);
  if (!valid) {
    return;
  }

  submitting.value = true;
  try {
    const result = await createAnalysisTask(form);
    ElMessage.success("分析完成");
    if (result.report_id) {
      router.push(`/reports/${result.report_id}`);
      return;
    }
    router.push(`/analysis/tasks/${result.task_id}`);
  } finally {
    submitting.value = false;
  }
}

onMounted(loadOptions);
</script>

<style scoped lang="scss">
.selection-list {
  display: grid;
  gap: 12px;
}

.selection-card {
  padding: 16px 18px;
  display: grid;
  gap: 8px;
  text-align: left;
  border: 1px solid var(--panel-border);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.86);
  cursor: pointer;
}

.selection-card.active {
  border-color: rgba(27, 127, 107, 0.5);
  background: rgba(27, 127, 107, 0.08);
}

.selection-card span {
  color: var(--text-secondary);
}
</style>
