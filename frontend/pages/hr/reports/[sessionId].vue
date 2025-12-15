<template>
  <div class="min-h-screen bg-minimal-bg text-minimal-text-primary p-8">
    <div v-if="loading" class="text-center py-12">
      <div
        class="animate-spin rounded-full h-12 w-12 border-b-2 border-minimal-info mx-auto mb-4"
      ></div>
      <p class="text-minimal-text-secondary">Loading report...</p>
    </div>
    <div
      v-else-if="error"
      class="max-w-4xl mx-auto bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative"
    >
      {{ error }}
    </div>
    <div v-else-if="report" class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <button
          @click="router.back()"
          class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-semibold"
        >
          ← Back to Reports
        </button>
        <button
          @click="handleDownloadPDF"
          class="flex items-center gap-2 px-4 py-2 bg-minimal-info text-white rounded-lg hover:bg-sky-600 transition-colors font-semibold"
        >
          <ArrowDownTrayIcon class="w-5 h-5" />
          Download PDF
        </button>
      </div>

      <!-- Candidate Info -->
      <div
        class="bg-minimal-card p-6 rounded-lg shadow-sm border border-minimal-border mb-6"
      >
        <h1 class="text-2xl font-bold mb-4 text-minimal-text-primary">
          {{ report.candidate.name }}
        </h1>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="flex flex-col">
            <span class="text-xs font-semibold uppercase text-minimal-text-secondary"
              >Email</span
            >
            <span class="font-medium">{{ report.candidate.email || 'N/A' }}</span>
          </div>
          <div class="flex flex-col">
            <span class="text-xs font-semibold uppercase text-minimal-text-secondary"
              >Role</span
            >
            <span class="font-medium">{{ report.candidate.role_id }}</span>
          </div>
          <div class="flex flex-col">
            <span class="text-xs font-semibold uppercase text-minimal-text-secondary"
              >Interview Date</span
            >
            <span class="font-medium">{{ formatDate(report.candidate.interview_date) }}</span>
          </div>
          <div class="flex flex-col">
            <span class="text-xs font-semibold uppercase text-minimal-text-secondary"
              >Session ID</span
            >
            <span class="font-mono text-sm bg-gray-100 px-2 py-1 rounded max-w-max">{{
              report.candidate.session_id
            }}</span>
          </div>
        </div>
      </div>

      <!-- Score Overview -->
      <div v-if="report.aggregated_score" class="bg-minimal-card p-6 rounded-lg shadow-sm border border-minimal-border mb-6">
        <h2 class="text-xl font-semibold mb-6 text-minimal-text-primary">
          Score Overview
        </h2>
        <div class="flex flex-col md:flex-row gap-8 items-center">
          <div class="flex flex-col items-center gap-4">
            <ScoreCard :score="report.aggregated_score.total_score" :size="200" />
            <div
              class="px-6 py-2 rounded-full font-bold text-lg text-white"
              :class="getRecommendationClass(report.aggregated_score.overall_recommendation)"
            >
              {{ report.aggregated_score.overall_recommendation }}
            </div>
          </div>
          <div class="flex-1 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 w-full">
            <div class="bg-sky-50 p-4 rounded-lg border-l-4 border-minimal-info">
              <div class="text-sm text-gray-600 mb-1">Communication</div>
              <div class="text-2xl font-bold text-gray-900">
                {{ report.aggregated_score.communication_avg }} / 10
              </div>
            </div>
            <div class="bg-sky-50 p-4 rounded-lg border-l-4 border-minimal-info">
              <div class="text-sm text-gray-600 mb-1">Relevance</div>
              <div class="text-2xl font-bold text-gray-900">
                {{ report.aggregated_score.relevance_avg }} / 10
              </div>
            </div>
            <div class="bg-sky-50 p-4 rounded-lg border-l-4 border-minimal-info">
              <div class="text-sm text-gray-600 mb-1">Logical Thinking</div>
              <div class="text-2xl font-bold text-gray-900">
                {{ report.aggregated_score.logical_thinking_avg }} / 10
              </div>
            </div>
            <div class="bg-sky-50 p-4 rounded-lg border-l-4 border-minimal-info">
              <div class="text-sm text-gray-600 mb-1">Pass Rate</div>
              <div class="text-2xl font-bold text-gray-900">
                {{ report.aggregated_score.pass_rate }}%
              </div>
            </div>
             <div class="bg-sky-50 p-4 rounded-lg border-l-4 border-minimal-info">
              <div class="text-sm text-gray-600 mb-1">Questions Answered</div>
              <div class="text-2xl font-bold text-gray-900">
                 {{ report.aggregated_score.questions_answered }} /
                {{ report.aggregated_score.total_questions }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="bg-minimal-card p-6 rounded-lg shadow-sm border border-minimal-border">
          <h3 class="text-lg font-semibold mb-4 text-center">Skills Breakdown</h3>
          <ScoreRadarChart
            v-if="report.aggregated_score"
            :communication-avg="report.aggregated_score.communication_avg"
            :relevance-avg="report.aggregated_score.relevance_avg"
            :logical-thinking-avg="report.aggregated_score.logical_thinking_avg"
          />
        </div>
        <div class="bg-minimal-card p-6 rounded-lg shadow-sm border border-minimal-border">
          <h3 class="text-lg font-semibold mb-4 text-center">Question Scores</h3>
          <ScoreBarChart :questions="report.questions" />
        </div>
      </div>

      <!-- Question Details -->
      <div class="bg-minimal-card p-6 rounded-lg shadow-sm border border-minimal-border">
        <h2 class="text-xl font-semibold mb-6 text-minimal-text-primary">
          Question-by-Question Analysis
        </h2>
        <div
          v-for="(question, idx) in report.questions"
          :key="question.id"
          class="border border-gray-200 rounded-lg mb-4 overflow-hidden"
        >
          <div
            class="p-4 bg-gray-50 cursor-pointer flex justify-between items-center hover:bg-gray-100 transition-colors"
            @click="toggleQuestion(idx)"
          >
            <div class="flex gap-4 flex-1 items-center">
              <span class="font-bold text-minimal-info">Q{{ idx + 1 }}</span>
              <span class="text-gray-800 font-medium">{{ question.question }}</span>
            </div>
            <div class="flex gap-4 items-center">
              <span class="px-3 py-1 rounded-full text-sm font-semibold" :class="getScoreClass(question.total_score)">
                {{ question.total_score }}/10
              </span>
              <span
                class="px-3 py-1 rounded-full text-sm font-semibold"
                :class="question.pass_prediction ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
              >
                {{ question.pass_prediction ? '✓ Pass' : '✗ Fail' }}
              </span>
              <span class="text-gray-400">{{ expandedQuestions[idx] ? '▲' : '▼' }}</span>
            </div>
          </div>

          <div v-if="expandedQuestions[idx]" class="p-6 bg-white border-t border-gray-200">
            <!-- Individual Scores -->
            <div class="flex flex-wrap gap-4 mb-6">
              <div class="bg-gray-50 px-4 py-2 rounded-lg text-center">
                <span class="text-xs text-gray-500 block mb-1">Communication</span>
                <span class="font-bold text-gray-900">{{ question.communication_score }}/10</span>
              </div>
              <div class="bg-gray-50 px-4 py-2 rounded-lg text-center">
                <span class="text-xs text-gray-500 block mb-1">Relevance</span>
                <span class="font-bold text-gray-900">{{ question.relevance_score }}/10</span>
              </div>
              <div class="bg-gray-50 px-4 py-2 rounded-lg text-center">
                <span class="text-xs text-gray-500 block mb-1">Logical Thinking</span>
                <span class="font-bold text-gray-900">{{ question.logical_thinking_score || question.quality_score }}/10</span>
              </div>
            </div>

            <!-- Transcript -->
            <div v-if="question.transcript" class="mb-6">
              <h4 class="text-sm font-bold text-gray-700 mb-2">Candidate's Answer:</h4>
              <p class="bg-gray-50 p-4 rounded-lg text-gray-700 leading-relaxed">
                {{ question.transcript }}
              </p>
            </div>

            <!-- Feedback -->
            <div v-if="question.feedback" class="space-y-4">
              <div v-if="question.feedback.strengths" class="p-4 bg-green-50 border-l-4 border-green-500 rounded-r-lg">
                <h4 class="flex items-center gap-2 font-bold text-green-800 mb-1">
                  <FireIcon class="w-4 h-4" />
                  Strengths:
                </h4>
                <p class="text-green-900">{{ question.feedback.strengths }}</p>
              </div>
              
              <div v-if="question.feedback.weaknesses" class="p-4 bg-red-50 border-l-4 border-red-500 rounded-r-lg">
                <h4 class="flex items-center gap-2 font-bold text-red-800 mb-1">
                   <ExclamationTriangleIcon class="w-4 h-4" />
                  Areas for Improvement:
                </h4>
                <p class="text-red-900">{{ question.feedback.weaknesses }}</p>
              </div>

               <div v-if="question.feedback.summary" class="p-4 bg-blue-50 border-l-4 border-blue-500 rounded-r-lg">
                <h4 class="flex items-center gap-2 font-bold text-blue-800 mb-1">
                  <DocumentTextIcon class="w-4 h-4" />
                  Summary:
                </h4>
                <p class="text-blue-900">{{ question.feedback.summary }}</p>
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
import ScoreCard from '@/components/ScoreCard.vue';
import ScoreRadarChart from '@/components/ScoreRadarChart.vue';
import ScoreBarChart from '@/components/ScoreBarChart.vue';

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
  if (score >= 8) return 'bg-green-500 text-white';
  if (score >= 6) return 'bg-blue-500 text-white';
  if (score >= 4) return 'bg-amber-500 text-white';
  return 'bg-red-500 text-white';
};

const getRecommendationClass = (rec: string) => {
  if (rec === 'Strong Pass') return 'bg-green-500';
  if (rec === 'Pass') return 'bg-blue-500';
  if (rec === 'Review') return 'bg-amber-500';
  return 'bg-red-500';
};
</script>
