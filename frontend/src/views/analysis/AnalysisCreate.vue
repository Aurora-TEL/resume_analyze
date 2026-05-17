<template>
  <div class="app-page">
    <section class="hero-card">
      <p class="hero-kicker">Full Analysis</p>
      <h1 class="hero-title">{{ t.analysis.create.heroTitle }}</h1>
      <p class="hero-copy">{{ t.analysis.create.heroCopy }}</p>
    </section>

    <section class="section-card">
      <div class="section-head">
        <div>
          <h2 class="section-title">{{ t.analysis.create.sectionTitle }}</h2>
          <p class="section-copy">{{ t.analysis.create.sectionCopy }}</p>
        </div>
      </div>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <el-form-item :label="t.analysis.create.labelResume" prop="resume_id">
          <el-select v-model="form.resume_id" :placeholder="t.analysis.create.placeholderResume" filterable style="width: 100%">
            <el-option v-for="item in resumes" :key="item.id" :label="item.title" :value="item.id" />
          </el-select>
        </el-form-item>

        <el-form-item :label="t.analysis.create.labelJob" prop="job_description_id">
          <el-select v-model="form.job_description_id" :placeholder="t.analysis.create.placeholderJob" filterable style="width: 100%">
            <el-option
              v-for="item in jobs"
              :key="item.id"
              :label="`${item.title}${item.company_name ? ` / ${item.company_name}` : ''}`"
              :value="item.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item :label="t.analysis.create.labelTaskType">
          <el-input :model-value="t.analysis.create.taskTypeValue" disabled />
        </el-form-item>

        <div class="action-row">
          <el-button type="primary" :loading="submitting" @click="handleSubmit">{{ t.analysis.create.actionSubmit }}</el-button>
          <el-button @click="router.push('/reports')">{{ t.analysis.create.actionViewReports }}</el-button>
        </div>
      </el-form>
    </section>

    <section class="two-column">
      <article class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">{{ t.analysis.create.resumeSectionTitle }}</h2>
            <p class="section-copy">{{ t.analysis.create.resumeSectionCopy }}</p>
          </div>
        </div>
        <el-empty v-if="!resumes.length && !loading" :description="t.analysis.create.resumeEmpty" />
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
            <h2 class="section-title">{{ t.analysis.create.jobSectionTitle }}</h2>
            <p class="section-copy">{{ t.analysis.create.jobSectionCopy }}</p>
          </div>
        </div>
        <el-empty v-if="!jobs.length && !loading" :description="t.analysis.create.jobEmpty" />
        <div v-else class="selection-list">
          <button
            v-for="item in jobs"
            :key="item.id"
            class="selection-card"
            :class="{ active: form.job_description_id === item.id }"
            @click="form.job_description_id = item.id"
          >
            <strong>{{ item.title }}</strong>
            <span>{{ item.company_name || t.analysis.create.companyFallback }}</span>
          </button>
        </div>
      </article>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage, type FormInstance, type FormRules } from "element-plus";

import { createAnalysisTask } from "@/api/analysis";
import { listJobs, type JobListItem } from "@/api/jobs";
import { listResumes, type ResumeListItem } from "@/api/resumes";
import { statusLabel } from "@/utils/format";
import { useUserMessages } from "@/utils/userI18n";

const route = useRoute();
const router = useRouter();
const messages = useUserMessages();
const t = computed(() => messages.value);
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

const rules = computed<FormRules>(() => ({
  resume_id: [{ required: true, message: t.value.analysis.create.validationResumeRequired, trigger: "change" }],
  job_description_id: [{ required: true, message: t.value.analysis.create.validationJobRequired, trigger: "change" }],
}));

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
    ElMessage.success(t.value.analysis.create.success);
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
