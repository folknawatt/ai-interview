<template>
  <div class="report-detail-container">
    <div v-if="loading" class="loading">Loading report...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="report" class="report-content">
      <!-- Header -->
      <div class="header">
        <button @click="router.back()" class="btn-back">← Back to Reports</button>
        <button @click="handleDownloadPDF" class="btn-download">
          <ArrowDownTrayIcon class="icon-inline" />
          Download PDF
        </button>
      </div>

      <!-- Candidate Info -->
      <div class="candidate-section">
        <h1>{{ report.candidate.name }}</h1>
        <div class="candidate-info">
          <div class="info-item">
            <span class="label">Email:</span>
            <span>{{ report.candidate.email || 'N/A' }}</span>
          </div>
          <div class="info-item">
            <span class="label">Role:</span>
            <span>{{ report.candidate.role_id }}</span>
          </div>
          <div class="info-item">
            <span class="label">Interview Date:</span>
            <span>{{ formatDate(report.candidate.interview_date) }}</span>
          </div>
          <div class="info-item">
            <span class="label">Session ID:</span>
            <span class="session-id">{{ report.candidate.session_id }}</span>
          </div>
        </div>
      </div>

      <!-- Score Overview -->
      <div v-if="report.aggregated_score" class="score-section">
        <h2>Score Overview</h2>
        <div class="score-overview">
          <div class="score-circle">
            <ScoreCard :score="report.aggregated_score.total_score" :size="200" />
            <div
              class="recommendation-badge"
              :class="getRecommendationClass(report.aggregated_score.overall_recommendation)"
            >
              {{ report.aggregated_score.overall_recommendation }}
            </div>
          </div>
          <div class="score-details">
            <div class="score-item">
              <div class="score-label">Communication</div>
              <div class="score-value">
                {{ report.aggregated_score.communication_avg.toFixed(1) }} / 10
              </div>
            </div>
            <div class="score-item">
              <div class="score-label">Relevance</div>
              <div class="score-value">
                {{ report.aggregated_score.relevance_avg.toFixed(1) }} / 10
              </div>
            </div>
            <div class="score-item">
              <div class="score-label">Quality</div>
              <div class="score-value">
                {{ report.aggregated_score.quality_avg.toFixed(1) }} / 10
              </div>
            </div>
            <div class="score-item">
              <div class="score-label">Pass Rate</div>
              <div class="score-value">
                {{ report.aggregated_score.pass_rate.toFixed(1) }}%
              </div>
            </div>
            <div class="score-item">
              <div class="score-label">Questions Answered</div>
              <div class="score-value">
                {{ report.aggregated_score.questions_answered }} /
                {{ report.aggregated_score.total_questions }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts -->
      <div class="charts-section">
        <div class="chart-card">
          <h3>Skills Breakdown</h3>
          <ScoreRadarChart
            v-if="report.aggregated_score"
            :communication-avg="report.aggregated_score.communication_avg"
            :relevance-avg="report.aggregated_score.relevance_avg"
            :quality-avg="report.aggregated_score.quality_avg"
          />
        </div>
        <div class="chart-card">
          <h3>Question Scores</h3>
          <ScoreBarChart :questions="report.questions" />
        </div>
      </div>

      <!-- Question Details -->
      <div class="questions-section">
        <h2>Question-by-Question Analysis</h2>
        <div
          v-for="(question, idx) in report.questions"
          :key="question.id"
          class="question-card"
        >
          <div class="question-header" @click="toggleQuestion(idx)">
            <div class="question-title">
              <span class="question-number">Q{{ idx + 1 }}</span>
              <span class="question-text">{{ question.question }}</span>
            </div>
            <div class="question-scores">
              <span class="score-pill" :class="getScoreClass(question.total_score)">
                {{ question.total_score }}/10
              </span>
              <span class="pass-badge" :class="question.pass_prediction ? 'pass' : 'fail'">
                {{ question.pass_prediction ? '✓ Pass' : '✗ Fail' }}
              </span>
              <span class="expand-icon">{{ expandedQuestions[idx] ? '▲' : '▼' }}</span>
            </div>
          </div>

          <div v-if="expandedQuestions[idx]" class="question-details">
            <!-- Individual Scores -->
            <div class="individual-scores">
              <div class="score-badge">
                <span class="badge-label">Communication</span>
                <span class="badge-value">{{ question.communication_score }}/10</span>
              </div>
              <div class="score-badge">
                <span class="badge-label">Relevance</span>
                <span class="badge-value">{{ question.relevance_score }}/10</span>
              </div>
              <div class="score-badge">
                <span class="badge-label">Quality</span>
                <span class="badge-value">{{ question.quality_score }}/10</span>
              </div>
            </div>

            <!-- Transcript -->
            <div v-if="question.transcript" class="transcript-section">
              <h4>Candidate's Answer:</h4>
              <p class="transcript">{{ question.transcript }}</p>
            </div>

            <div v-if="question.feedback" class="feedback-section">
              <div v-if="question.feedback.strengths" class="feedback-item strengths">
                <h4 class="flex items-center gap-2">
                  <FireIcon class="icon-feedback" />
                  Strengths:
                </h4>
                <p>{{ question.feedback.strengths }}</p>
              </div>
              <div v-if="question.feedback.weaknesses" class="feedback-item weaknesses">
                <h4 class="flex items-center gap-2">
                  <ExclamationTriangleIcon class="icon-feedback" />
                  Areas for Improvement:
                </h4>
                <p>{{ question.feedback.weaknesses }}</p>
              </div>
              <div v-if="question.feedback.summary" class="feedback-item summary">
                <h4 class="flex items-center gap-2">
                  <DocumentTextIcon class="icon-feedback" />
                  Summary:
                </h4>
                <p>{{ question.feedback.summary }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  ArrowDownTrayIcon,
  FireIcon,
  ExclamationTriangleIcon,
  DocumentTextIcon
} from '@heroicons/vue/24/solid';

const route = useRoute();
const router = useRouter();
const { getReportDetails, downloadPDF } = useReports();

const sessionId = computed(() => route.params.sessionId as string);
const report = ref<any>(null);
const loading = ref(true);
const error = ref('');
const expandedQuestions = ref<Record<number, boolean>>({});

onMounted(async () => {
  await loadReport();
});

const loadReport = async () => {
  try {
    loading.value = true;
    error.value = '';
    report.value = await getReportDetails(sessionId.value);
  } catch (err: any) {
    error.value = err.message || 'Failed to load report';
  } finally {
    loading.value = false;
  }
};

const toggleQuestion = (idx: number) => {
  expandedQuestions.value[idx] = !expandedQuestions.value[idx];
};

const handleDownloadPDF = async () => {
  try {
    await downloadPDF(sessionId.value);
  } catch (err: any) {
    alert('Failed to download PDF: ' + err.message);
  }
};

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
};

const getScoreClass = (score: number) => {
  if (score >= 8) return 'excellent';
  if (score >= 6) return 'good';
  if (score >= 4) return 'fair';
  return 'poor';
};

const getRecommendationClass = (rec: string) => {
  if (rec === 'Strong Pass') return 'strong-pass';
  if (rec === 'Pass') return 'pass';
  if (rec === 'Review') return 'review';
  return 'fail';
};
</script>

<style scoped>
.report-detail-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.btn-back,
.btn-download {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-back {
  background: #f3f4f6;
  color: #374151;
}

.btn-back:hover {
  background: #e5e7eb;
}

.btn-download {
  background: #667eea;
  color: white;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-download:hover {
  background: #5568d3;
}

.icon-inline {
  width: 1.2rem;
  height: 1.2rem;
}

.icon-feedback {
  width: 1rem;
  height: 1rem;
}

.candidate-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #1a1a1a;
}

.candidate-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  gap: 0.5rem;
}

.label {
  font-weight: 600;
  color: #666;
}

.session-id {
  font-family: monospace;
  background: #f3f4f6;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}

.score-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: #1a1a1a;
}

.score-overview {
  display: flex;
  gap: 3rem;
  align-items: center;
  flex-wrap: wrap;
}

.score-circle {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.recommendation-badge {
  padding: 0.6rem 1.5rem;
  border-radius: 25px;
  font-weight: 700;
  font-size: 1.1rem;
}

.recommendation-badge.strong-pass {
  background: #10b981;
  color: white;
}

.recommendation-badge.pass {
  background: #3b82f6;
  color: white;
}

.recommendation-badge.review {
  background: #f59e0b;
  color: white;
}

.recommendation-badge.fail {
  background: #ef4444;
  color: white;
}

.score-details {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.score-item {
  background: #f9fafb;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.score-label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.score-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1a1a1a;
}

.charts-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.chart-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h3 {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
  color: #1a1a1a;
  text-align: center;
}

.questions-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.question-card {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 1rem;
  overflow: hidden;
}

.question-header {
  padding: 1.5rem;
  background: #f9fafb;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background 0.2s;
}

.question-header:hover {
  background: #f3f4f6;
}

.question-title {
  display: flex;
  gap: 1rem;
  flex: 1;
}

.question-number {
  font-weight: bold;
  color: #667eea;
}

.question-scores {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.score-pill {
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
}

.score-pill.excellent {
  background: #10b981;
  color: white;
}

.score-pill.good {
  background: #3b82f6;
  color: white;
}

.score-pill.fair {
  background: #f59e0b;
  color: white;
}

.score-pill.poor {
  background: #ef4444;
  color: white;
}

.pass-badge {
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
}

.pass-badge.pass {
  background: #d1fae5;
  color: #065f46;
}

.pass-badge.fail {
  background: #fee2e2;
  color: #991b1b;
}

.question-details {
  padding: 1.5rem;
  background: white;
}

.individual-scores {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.score-badge {
  background: #f3f4f6;
  padding: 0.8rem 1.2rem;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.badge-label {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 0.3rem;
}

.badge-value {
  font-size: 1.2rem;
  font-weight: bold;
  color: #1a1a1a;
}

.transcript-section,
.feedback-section {
  margin-top: 1.5rem;
}

h4 {
  font-size: 1rem;
  margin-bottom: 0.8rem;
  color: #374151;
}

.transcript {
  background: #f9fafb;
  padding: 1rem;
  border-radius: 6px;
  line-height: 1.6;
  color: #374151;
}

.feedback-item {
  margin-bottom: 1rem;
  padding: 1rem;
  border-radius: 8px;
}

.feedback-item.strengths {
  background: #d1fae5;
  border-left: 4px solid #10b981;
}

.feedback-item.weaknesses {
  background: #fee2e2;
  border-left: 4px solid #ef4444;
}

.feedback-item.summary {
  background: #dbeafe;
  border-left: 4px solid #3b82f6;
}

.loading,
.error {
  text-align: center;
  padding: 3rem;
  font-size: 1.1rem;
}

.error {
  color: #ef4444;
}
</style>
