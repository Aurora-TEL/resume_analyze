<template>
  <div class="app-page" v-loading="loading">
    <section class="hero-card" v-if="report">
      <p class="hero-kicker">Analysis Report</p>
      <h1 class="hero-title">{{ t.heroTitle }}</h1>
      <p class="hero-copy">{{ report.summary || t.heroFallback }}</p>
      <div class="action-row">
        <el-button type="primary" @click="router.push('/analysis/create')">{{ t.actionAnalyzeAgain }}</el-button>
        <el-button @click="router.push('/reports')">{{ t.actionBack }}</el-button>
      </div>
    </section>

    <section v-if="report" class="metric-grid">
      <article class="metric-card">
        <p class="metric-label">{{ t.metricTotalScore }}</p>
        <p class="metric-value">{{ formatScore(report.total_score) }}</p>
        <p class="metric-note">{{ t.metricTotalScoreNote }}</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">{{ t.metricMatchScore }}</p>
        <p class="metric-value">{{ formatScore(report.match_score) }}</p>
        <p class="metric-note">{{ t.metricMatchScoreNote }}</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">{{ t.metricModel }}</p>
        <p class="metric-value metric-value--small">{{ report.model_name }}</p>
        <p class="metric-note">{{ report.model_provider }}</p>
      </article>
      <article class="metric-card">
        <p class="metric-label">{{ t.metricCreatedAt }}</p>
        <p class="metric-value metric-value--small">{{ formatDate(report.created_at) }}</p>
        <p class="metric-note">{{ t.metricCreatedAtNote }}</p>
      </article>
    </section>

    <div v-if="report" class="two-column">
      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">{{ t.strengthSectionTitle }}</h2>
            <p class="section-copy">{{ t.strengthSectionCopy }}</p>
          </div>
        </div>

        <div class="list-section">
          <h3>{{ t.strengthsTitle }}</h3>
          <el-empty v-if="!strengths.length" :description="t.emptyStrengths" />
          <ul v-else class="bullet-list">
            <li v-for="item in strengths" :key="item">{{ item }}</li>
          </ul>
        </div>

        <div class="list-section">
          <h3>{{ t.weaknessesTitle }}</h3>
          <el-empty v-if="!weaknesses.length" :description="t.emptyWeaknesses" />
          <ul v-else class="bullet-list">
            <li v-for="item in weaknesses" :key="item">{{ item }}</li>
          </ul>
        </div>

        <div class="list-section">
          <h3>{{ t.missingRequirementsTitle }}</h3>
          <el-empty v-if="!missingRequirements.length" :description="t.emptyMissingRequirements" />
          <ul v-else class="bullet-list">
            <li v-for="item in missingRequirements" :key="item">{{ item }}</li>
          </ul>
        </div>
      </section>

      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">{{ t.keywordSectionTitle }}</h2>
            <p class="section-copy">{{ t.keywordSectionCopy }}</p>
          </div>
        </div>

        <el-progress :percentage="keywordCoverage" :stroke-width="12" />

        <div class="list-section">
          <h3>{{ t.matchedKeywordsTitle }}</h3>
          <div class="pill-list">
            <el-tag v-for="item in matchedKeywords" :key="item" type="success" effect="plain">{{ item }}</el-tag>
            <span v-if="!matchedKeywords.length">{{ t.emptyGeneric }}</span>
          </div>
        </div>

        <div class="list-section">
          <h3>{{ t.missingKeywordsTitle }}</h3>
          <div class="pill-list">
            <el-tag v-for="item in missingKeywords" :key="item" type="danger" effect="plain">{{ item }}</el-tag>
            <span v-if="!missingKeywords.length">{{ t.emptyGeneric }}</span>
          </div>
        </div>
      </section>
    </div>

    <div v-if="report" class="two-column">
      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">{{ t.suggestionSectionTitle }}</h2>
            <p class="section-copy">{{ t.suggestionSectionCopy }}</p>
          </div>
        </div>

        <el-empty v-if="!suggestions.length" :description="t.emptySuggestions" />
        <ul v-else class="bullet-list">
          <li v-for="item in suggestions" :key="item">{{ item }}</li>
        </ul>

        <div class="list-section">
          <h3>{{ t.nextActionsTitle }}</h3>
          <el-empty v-if="!nextActions.length" :description="t.emptyNextActions" />
          <ul v-else class="bullet-list">
            <li v-for="item in nextActions" :key="item">{{ item }}</li>
          </ul>
        </div>
      </section>

      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">{{ t.rewriteSectionTitle }}</h2>
            <p class="section-copy">{{ t.rewriteSectionCopy }}</p>
          </div>
        </div>

        <div class="list-section">
          <h3>{{ t.rewriteExamplesTitle }}</h3>
          <el-empty v-if="!rewriteExamples.length" :description="t.emptyRewriteExamples" />
          <ul v-else class="bullet-list">
            <li v-for="item in rewriteExamples" :key="item">{{ item }}</li>
          </ul>
        </div>

        <div class="list-section">
          <h3>{{ t.riskNotesTitle }}</h3>
          <el-empty v-if="!riskNotes.length" :description="t.emptyRiskNotes" />
          <ul v-else class="bullet-list">
            <li v-for="item in riskNotes" :key="item">{{ item }}</li>
          </ul>
        </div>
      </section>
    </div>

    <section v-if="report" class="section-card">
      <div class="section-head">
        <div>
          <h2 class="section-title">{{ t.rawJsonTitle }}</h2>
          <p class="section-copy">{{ t.rawJsonCopy }}</p>
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
import { useLocaleStore } from "@/stores/locale";
import { asArray, formatDate, formatListItem, formatScore } from "@/utils/format";

const zh = {
  heroTitle: "\u4e00\u6b21\u5b8c\u6574\u7684\u7b80\u5386\u5339\u914d\u5206\u6790\u5df2\u7ecf\u843d\u6210\u3002",
  heroFallback: "\u8fd9\u4efd\u62a5\u544a\u5df2\u7ecf\u51c6\u5907\u597d\u4e86\uff0c\u53ef\u4ee5\u4ece\u603b\u5206\u3001\u5339\u914d\u5ea6\u3001\u5173\u952e\u8bcd\u8986\u76d6\u548c\u884c\u52a8\u5efa\u8bae\u51e0\u90e8\u5206\u5f80\u4e0b\u770b\u3002",
  actionAnalyzeAgain: "\u518d\u505a\u4e00\u6b21\u5206\u6790",
  actionBack: "\u8fd4\u56de\u62a5\u544a\u5217\u8868",
  metricTotalScore: "\u603b\u5206",
  metricTotalScoreNote: "\u7b80\u5386\u6574\u4f53\u5b8c\u6210\u5ea6\u548c\u8868\u8fbe\u8d28\u91cf\u3002",
  metricMatchScore: "\u5339\u914d\u5ea6",
  metricMatchScoreNote: "\u4e0e\u5f53\u524d\u5c97\u4f4d\u8981\u6c42\u7684\u8d34\u5408\u7a0b\u5ea6\u3002",
  metricModel: "\u6a21\u578b",
  metricCreatedAt: "\u751f\u6210\u65f6\u95f4",
  metricCreatedAtNote: "\u62a5\u544a\u5df2\u7ecf\u6301\u4e45\u5316\uff0c\u53ef\u91cd\u590d\u67e5\u770b\u3002",
  strengthSectionTitle: "\u4eae\u70b9\u4e0e\u77ed\u677f",
  strengthSectionCopy: "\u5148\u770b\u5f53\u524d\u4f18\u52bf\uff0c\u518d\u805a\u7126\u6700\u5f71\u54cd\u6295\u9012\u7ed3\u679c\u7684\u5dee\u8ddd\u3002",
  strengthsTitle: "\u4f18\u52bf",
  emptyStrengths: "\u6682\u65e0\u7ed3\u6784\u5316\u4f18\u52bf",
  weaknessesTitle: "\u77ed\u677f",
  emptyWeaknesses: "\u6682\u65e0\u7ed3\u6784\u5316\u77ed\u677f",
  missingRequirementsTitle: "\u7f3a\u5931\u8981\u6c42",
  emptyMissingRequirements: "\u6682\u65e0\u7f3a\u5931\u9879",
  keywordSectionTitle: "\u5173\u952e\u8bcd\u8986\u76d6",
  keywordSectionCopy: "\u8986\u76d6\u7387\u548c\u7f3a\u53e3\u4f1a\u76f4\u63a5\u5f71\u54cd\u7b80\u5386\u53ef\u89c1\u6027\u3002",
  matchedKeywordsTitle: "\u5df2\u8986\u76d6\u5173\u952e\u8bcd",
  missingKeywordsTitle: "\u7f3a\u5931\u5173\u952e\u8bcd",
  emptyGeneric: "\u6682\u65e0",
  suggestionSectionTitle: "\u4f18\u5316\u5efa\u8bae",
  suggestionSectionCopy: "\u8fd9\u4e9b\u52a8\u4f5c\u6700\u9002\u5408\u76f4\u63a5\u843d\u5230\u4e0b\u4e00\u7248\u7b80\u5386\u91cc\u3002",
  emptySuggestions: "\u6682\u65e0\u5efa\u8bae\u9879",
  nextActionsTitle: "\u4e0b\u4e00\u6b65\u52a8\u4f5c",
  emptyNextActions: "\u6682\u65e0\u4e0b\u4e00\u6b65\u52a8\u4f5c",
  rewriteSectionTitle: "\u6539\u5199\u793a\u4f8b\u4e0e\u98ce\u9669\u63d0\u793a",
  rewriteSectionCopy: "\u907f\u514d\u4e3a\u4e86\u5339\u914d\u5c97\u4f4d\u800c\u865a\u6784\u7ecf\u5386\uff0c\u8fd9\u90e8\u5206\u4e3b\u8981\u7528\u4e8e\u5b88\u4f4f\u8fb9\u754c\u3002",
  rewriteExamplesTitle: "\u6539\u5199\u793a\u4f8b",
  emptyRewriteExamples: "\u6682\u65e0\u6539\u5199\u793a\u4f8b",
  riskNotesTitle: "\u98ce\u9669\u63d0\u793a",
  emptyRiskNotes: "\u6682\u65e0\u98ce\u9669\u63d0\u793a",
  rawJsonTitle: "\u539f\u59cb JSON",
  rawJsonCopy: "\u9700\u8981\u8c03\u8bd5\u6216\u6838\u5bf9\u5b57\u6bb5\u65f6\uff0c\u53ef\u4ee5\u76f4\u63a5\u770b\u5b8c\u6574\u7ed3\u6784\u3002",
};

const en = {
  heroTitle: "A complete resume matching analysis has been generated.",
  heroFallback: "This report is ready. You can continue by reviewing the total score, match score, keyword coverage, and suggested next actions.",
  actionAnalyzeAgain: "Run Another Analysis",
  actionBack: "Back to Reports",
  metricTotalScore: "Score",
  metricTotalScoreNote: "Overall resume completeness and communication quality.",
  metricMatchScore: "Match",
  metricMatchScoreNote: "How closely the resume fits the current job requirements.",
  metricModel: "Model",
  metricCreatedAt: "Created At",
  metricCreatedAtNote: "The report has been persisted and can be reviewed again later.",
  strengthSectionTitle: "Strengths and Gaps",
  strengthSectionCopy: "Review current strengths first, then focus on the gaps that most affect application outcomes.",
  strengthsTitle: "Strengths",
  emptyStrengths: "No structured strengths yet",
  weaknessesTitle: "Weaknesses",
  emptyWeaknesses: "No structured weaknesses yet",
  missingRequirementsTitle: "Missing Requirements",
  emptyMissingRequirements: "No missing requirements",
  keywordSectionTitle: "Keyword Coverage",
  keywordSectionCopy: "Coverage rate and gaps directly affect how visible the resume is.",
  matchedKeywordsTitle: "Covered Keywords",
  missingKeywordsTitle: "Missing Keywords",
  emptyGeneric: "None",
  suggestionSectionTitle: "Optimization Suggestions",
  suggestionSectionCopy: "These actions are the best candidates to land directly in the next resume revision.",
  emptySuggestions: "No suggestions yet",
  nextActionsTitle: "Next Actions",
  emptyNextActions: "No next actions yet",
  rewriteSectionTitle: "Rewrite Examples and Risk Notes",
  rewriteSectionCopy: "This section helps keep clear boundaries and avoids inventing experience just to match a job.",
  rewriteExamplesTitle: "Rewrite Examples",
  emptyRewriteExamples: "No rewrite examples yet",
  riskNotesTitle: "Risk Notes",
  emptyRiskNotes: "No risk notes yet",
  rawJsonTitle: "Raw JSON",
  rawJsonCopy: "If you need to debug or verify fields, you can inspect the full structure directly here.",
};

const route = useRoute();
const router = useRouter();
const localeStore = useLocaleStore();
const t = computed(() => (localeStore.locale === "zh-CN" ? zh : en));
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
