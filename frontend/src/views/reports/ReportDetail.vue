<template>
  <div class="app-page" v-loading="loading">
    <section class="hero-card" v-if="report">
      <p class="hero-kicker">Analysis Report</p>
      <h1 class="hero-title">一次完整的简历匹配分析已经落成。</h1>
      <p class="hero-copy">
        {{ report.summary || "这份报告已经准备好，可以从总分、匹配度、关键词覆盖和行动建议几部分往下看。" }}
      </p>
      <div class="action-row">
        <el-button type="primary" @click="router.push('/analysis/create')">再做一次分析</el-button>
        <el-button @click="router.push('/reports')">返回报告列表</el-button>
      </div>
    </section>

    <section v-if="report" class="metric-grid">
      <article class="metric-card">
        <p class="metric-label">总分</p>
        <p class="metric-value">{{ formatScore(report.total_score) }}</p>
        <p class="metric-note">简历整体完成度和表达质量。</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">匹配度</p>
        <p class="metric-value">{{ formatScore(report.match_score) }}</p>
        <p class="metric-note">与当前岗位要求的贴合程度。</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">模型</p>
        <p class="metric-value metric-value--small">{{ report.model_name }}</p>
        <p class="metric-note">{{ report.model_provider }}</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">生成时间</p>
        <p class="metric-value metric-value--small">{{ formatDate(report.created_at) }}</p>
        <p class="metric-note">报告已经持久化，可重复查看。</p>
      </article>
    </section>

    <div v-if="report" class="two-column">
      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">亮点与短板</h2>
            <p class="section-copy">先看当前优势，再聚焦最影响投递结果的差距。</p>
          </div>
        </div>

        <div class="list-section">
          <h3>优势</h3>
          <el-empty v-if="!strengths.length" description="暂无结构化优势" />
          <ul v-else class="bullet-list">
            <li v-for="item in strengths" :key="item">{{ item }}</li>
          </ul>
        </div>

        <div class="list-section">
          <h3>短板</h3>
          <el-empty v-if="!weaknesses.length" description="暂无结构化短板" />
          <ul v-else class="bullet-list">
            <li v-for="item in weaknesses" :key="item">{{ item }}</li>
          </ul>
        </div>

        <div class="list-section">
          <h3>缺失要求</h3>
          <el-empty v-if="!missingRequirements.length" description="暂无缺失项" />
          <ul v-else class="bullet-list">
            <li v-for="item in missingRequirements" :key="item">{{ item }}</li>
          </ul>
        </div>
      </section>

      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">关键词覆盖</h2>
            <p class="section-copy">覆盖率和缺口会直接影响简历可见性。</p>
          </div>
        </div>

        <el-progress :percentage="keywordCoverage" :stroke-width="12" />

        <div class="list-section">
          <h3>已覆盖关键词</h3>
          <div class="pill-list">
            <el-tag v-for="item in matchedKeywords" :key="item" type="success" effect="plain">{{ item }}</el-tag>
            <span v-if="!matchedKeywords.length">暂无</span>
          </div>
        </div>

        <div class="list-section">
          <h3>缺失关键词</h3>
          <div class="pill-list">
            <el-tag v-for="item in missingKeywords" :key="item" type="danger" effect="plain">{{ item }}</el-tag>
            <span v-if="!missingKeywords.length">暂无</span>
          </div>
        </div>
      </section>
    </div>

    <div v-if="report" class="two-column">
      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">优化建议</h2>
            <p class="section-copy">这些动作最适合直接落到下一版简历里。</p>
          </div>
        </div>

        <el-empty v-if="!suggestions.length" description="暂无建议项" />
        <ul v-else class="bullet-list">
          <li v-for="item in suggestions" :key="item">{{ item }}</li>
        </ul>

        <div class="list-section">
          <h3>下一步动作</h3>
          <el-empty v-if="!nextActions.length" description="暂无下一步动作" />
          <ul v-else class="bullet-list">
            <li v-for="item in nextActions" :key="item">{{ item }}</li>
          </ul>
        </div>
      </section>

      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">改写示例与风险提示</h2>
            <p class="section-copy">避免为了匹配岗位而虚构经历，这部分主要用于守住边界。</p>
          </div>
        </div>

        <div class="list-section">
          <h3>改写示例</h3>
          <el-empty v-if="!rewriteExamples.length" description="暂无改写示例" />
          <ul v-else class="bullet-list">
            <li v-for="item in rewriteExamples" :key="item">{{ item }}</li>
          </ul>
        </div>

        <div class="list-section">
          <h3>风险提示</h3>
          <el-empty v-if="!riskNotes.length" description="暂无风险提示" />
          <ul v-else class="bullet-list">
            <li v-for="item in riskNotes" :key="item">{{ item }}</li>
          </ul>
        </div>
      </section>
    </div>

    <section v-if="report" class="section-card">
      <div class="section-head">
        <div>
          <h2 class="section-title">原始 JSON</h2>
          <p class="section-copy">需要调试或核对字段时，可以直接看完整结构。</p>
        </div>
      </div>
      <div class="json-panel">
        <pre>{{ reportJson }}</pre>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { getReportDetail, type ReportDetail } from "@/api/reports";
import { asArray, formatDate, formatListItem, formatScore } from "@/utils/format";

const route = useRoute();
const router = useRouter();
const loading = ref(false);
const report = ref<ReportDetail | null>(null);

const reportData = computed(() => (report.value?.report_data || {}) as Record<string, unknown>);
const reportJson = computed(() => JSON.stringify(report.value?.report_data || {}, null, 2));
const strengths = computed(() => asArray(reportData.value.strengths).map(formatListItem));
const weaknesses = computed(() => asArray(reportData.value.weaknesses).map(formatListItem));
const suggestions = computed(() => asArray(reportData.value.suggestions).map(formatListItem));
const nextActions = computed(() => asArray(reportData.value.next_actions).map(formatListItem));
const rewriteExamples = computed(() => asArray(reportData.value.rewrite_examples).map(formatListItem));
const riskNotes = computed(() => asArray(reportData.value.risk_notes).map(formatListItem));
const missingRequirements = computed(() => asArray(reportData.value.missing_requirements).map(formatListItem));
const keywordAnalysis = computed(() => (reportData.value.keyword_analysis || {}) as Record<string, unknown>);
const matchedKeywords = computed(() => asArray(keywordAnalysis.value.matched_keywords).map(String));
const missingKeywords = computed(() => asArray(keywordAnalysis.value.missing_keywords).map(String));
const keywordCoverage = computed(() => Number(keywordAnalysis.value.coverage_rate || 0));

async function loadReport() {
  loading.value = true;
  try {
    report.value = await getReportDetail(String(route.params.id));
  } finally {
    loading.value = false;
  }
}

onMounted(loadReport);
</script>

<style scoped lang="scss">
.metric-value--small {
  font-size: 24px;
  line-height: 1.35;
}

.list-section + .list-section {
  margin-top: 24px;
}

.list-section h3 {
  margin: 0 0 12px;
}

.bullet-list {
  margin: 0;
  padding-left: 18px;
  display: grid;
  gap: 10px;
  line-height: 1.7;
}
</style>
