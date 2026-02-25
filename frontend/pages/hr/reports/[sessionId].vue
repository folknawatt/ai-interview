<template>
  <div class="text-interview-text-primary p-8">
    <!-- Header Actions (Always Visible) -->
    <div class="max-w-6xl mx-auto flex justify-between items-center mb-8">
      <button
        @click="navigateTo('/hr/reports')"
        class="inline-flex items-center gap-2 px-4 py-2 text-interview-text-secondary hover:text-interview-text-primary hover:bg-interview-surface rounded-xl transition-all duration-300 group z-10"
      >
        <ArrowLeftIcon class="w-4 h-4 transition-transform group-hover:-translate-x-1" />
        Back to Reports
      </button>

      <button
        v-if="report"
        @click="handleDownloadPDF"
        class="flex items-center gap-2 px-4 py-2 bg-interview-primary hover:bg-interview-primary-hover text-interview-bg rounded-xl transition-all duration-300 font-semibold shadow-glow-amber hover:shadow-glow-amber-lg group z-10"
      >
        <ArrowDownTrayIcon class="w-5 h-5 transition-transform group-hover:-translate-y-1" />
        Download PDF
      </button>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-interview-primary border-t-transparent mx-auto mb-4"></div>
      <p class="text-interview-text-secondary">Loading report...</p>
    </div>

    <div
      v-else-if="error"
      class="max-w-4xl mx-auto bg-interview-warning/10 border border-interview-warning/30 text-interview-warning px-6 py-4 rounded-xl flex items-center gap-2"
    >
      <ExclamationTriangleIcon class="w-6 h-6 flex-shrink-0" />
      {{ error }}
    </div>

    <div v-else-if="report" class="max-w-6xl mx-auto">

      <!-- Candidate Info -->
      <div class="report-card bg-interview-surface backdrop-blur-xl p-6 rounded-2xl border border-interview-surface-border mb-6" style="--delay: 0ms">
        <h1 class="text-2xl font-bold mb-4 text-interview-text-primary">
          {{ report.candidate.name }}
        </h1>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="flex flex-col">
            <span class="text-xs font-semibold uppercase text-interview-text-muted">Email</span>
            <span class="font-medium text-interview-text-primary">{{ report.candidate.email || 'N/A' }}</span>
          </div>
          <div class="flex flex-col">
            <span class="text-xs font-semibold uppercase text-interview-text-muted">Role</span>
            <span class="font-medium text-interview-text-primary">{{ report.candidate.role_id }}</span>
          </div>
          <div class="flex flex-col">
            <span class="text-xs font-semibold uppercase text-interview-text-muted">Interview Date</span>
            <span class="font-medium text-interview-text-primary">{{ formatDate(report.candidate.interview_date) }}</span>
          </div>
        </div>
      </div>

      <!-- Score Overview -->
      <div
        v-if="report.aggregated_score"
        class="report-card bg-interview-surface backdrop-blur-xl p-6 rounded-2xl border border-interview-surface-border mb-6"
        style="--delay: 80ms"
      >
        <h2 class="text-xl font-semibold mb-6 text-interview-text-primary">Score Overview</h2>
        <div class="flex flex-col md:flex-row gap-8 items-center">
          <div class="flex flex-col items-center gap-4">
            <ScoreCard :score="report.aggregated_score.average_score" :size="200" />
            <div
              class="px-6 py-2 rounded-full font-bold text-lg"
              :class="getRecommendationClass(report.aggregated_score.overall_recommendation)"
            >
              {{ report.aggregated_score.overall_recommendation }}
            </div>
          </div>
          <div class="flex-1 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 w-full">
            <div class="bg-interview-bg-secondary p-4 rounded-xl border-l-4 border-interview-accent-sky">
              <div class="text-sm text-interview-text-muted mb-1">Communication</div>
              <div class="text-2xl font-bold text-interview-text-primary">
                {{ report.aggregated_score.communication_avg }} / 5
              </div>
            </div>
            <div class="bg-interview-bg-secondary p-4 rounded-xl border-l-4 border-interview-accent-teal">
              <div class="text-sm text-interview-text-muted mb-1">Relevance</div>
              <div class="text-2xl font-bold text-interview-text-primary">
                {{ report.aggregated_score.relevance_avg }} / 5
              </div>
            </div>
            <div class="bg-interview-bg-secondary p-4 rounded-xl border-l-4 border-interview-accent-olive">
              <div class="text-sm text-interview-text-muted mb-1">Logical Thinking</div>
              <div class="text-2xl font-bold text-interview-text-primary">
                {{ report.aggregated_score.logical_thinking_avg }} / 5
              </div>
            </div>
            <div class="bg-interview-bg-secondary p-4 rounded-xl border-l-4 border-interview-primary">
              <div class="text-sm text-interview-text-muted mb-1">Pass Rate</div>
              <div class="text-2xl font-bold text-interview-text-primary">
                {{ report.aggregated_score.pass_rate }}%
              </div>
            </div>
            <div class="bg-interview-bg-secondary p-4 rounded-xl border-l-4 border-interview-accent-rose">
              <div class="text-sm text-interview-text-muted mb-1">Questions Answered</div>
              <div class="text-2xl font-bold text-interview-text-primary">
                {{ report.aggregated_score.questions_answered }} /
                {{ report.aggregated_score.total_questions }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="report-card bg-interview-surface backdrop-blur-xl p-6 rounded-2xl border border-interview-surface-border" style="--delay: 160ms">
          <h3 class="text-lg font-semibold mb-4 text-center text-interview-text-primary">Skills Breakdown</h3>
          <ScoreRadarChart
            v-if="report.aggregated_score"
            :communication-avg="report.aggregated_score.communication_avg"
            :relevance-avg="report.aggregated_score.relevance_avg"
            :logical-thinking-avg="report.aggregated_score.logical_thinking_avg"
          />
        </div>
        <div class="report-card bg-interview-surface backdrop-blur-xl p-6 rounded-2xl border border-interview-surface-border" style="--delay: 240ms">
          <h3 class="text-lg font-semibold mb-4 text-center text-interview-text-primary">Question Scores</h3>
          <ScoreBarChart :questions="report.questions" />
        </div>
      </div>

      <!-- Question Details -->
      <div class="report-card bg-interview-surface backdrop-blur-xl p-6 rounded-2xl border border-interview-surface-border" style="--delay: 320ms">
        <h2 class="text-xl font-semibold mb-6 text-interview-text-primary">
          Question-by-Question Analysis
        </h2>
        <div
          v-for="(question, idx) in report.questions"
          :key="question.id"
          class="border border-interview-surface-border rounded-xl mb-4 overflow-hidden"
        >
          <div
            class="p-4 bg-interview-surface cursor-pointer flex justify-between items-center hover:bg-interview-surface-hover transition-colors"
            @click="toggleQuestion(idx)"
          >
            <div class="flex gap-4 flex-1 items-center">
              <span class="font-bold text-interview-primary">Q{{ idx + 1 }}</span>
              <span class="text-interview-text-primary font-medium">{{ question.question }}</span>
            </div>
            <div class="flex gap-4 items-center">
              <span
                class="px-3 py-1 rounded-full text-sm font-semibold"
                :class="getScoreClass(question.average_score)"
              >
                {{ question.average_score }}/5
              </span>
              <span
                class="px-3 py-1 rounded-full text-sm font-semibold"
                :class="
                  question.pass_prediction
                    ? 'bg-interview-success/20 text-interview-success'
                    : 'bg-interview-warning/20 text-interview-warning'
                "
              >
                {{ question.pass_prediction ? '✓ Pass' : '✗ Fail' }}
              </span>
              <button
                class="p-2 rounded-full hover:bg-interview-surface-border transition-colors text-interview-text-muted hover:text-white"
              >
                <ChevronDownIcon
                  class="w-5 h-5 transition-transform duration-300"
                  :class="{ 'rotate-180': expandedQuestions[idx] }"
                />
              </button>
            </div>
          </div>

          <Transition
            enter-active-class="transition-all duration-300"
            enter-from-class="opacity-0 max-h-0"
            enter-to-class="opacity-100 max-h-screen"
            leave-active-class="transition-all duration-300"
            leave-from-class="opacity-100 max-h-screen"
            leave-to-class="opacity-0 max-h-0"
          >
            <div v-if="expandedQuestions[idx]" class="p-6 bg-interview-bg-secondary border-t border-interview-surface-border">
              <!-- Video Answer -->
              <div v-if="question.video_url" class="mb-6">
                <h4 class="text-sm font-bold text-interview-primary mb-2 flex items-center gap-2">
                  <VideoCameraIcon class="w-4 h-4" />
                  Video Answer:
                </h4>
                <div class="relative w-full max-w-2xl rounded-xl overflow-hidden border border-interview-surface-border bg-black">
                  <video 
                    controls 
                    class="w-full h-auto aspect-video"
                    :src="getVideoUrl(question.video_url)"
                  >
                    Your browser does not support the video tag.
                  </video>
                </div>
              </div>

              <!-- Individual Scores -->
              <div v-if="question.transcript" class="flex flex-wrap gap-4 mb-6">
                <div class="bg-interview-surface px-4 py-3 rounded-xl text-center border border-interview-surface-border">
                  <span class="text-xs text-interview-text-secondary block mb-1">Communication</span>
                  <span class="font-bold text-interview-primary">{{ question.communication_score }}/5</span>
                </div>
                <div class="bg-interview-surface px-4 py-3 rounded-xl text-center border border-interview-surface-border">
                  <span class="text-xs text-interview-text-secondary block mb-1">Relevance</span>
                  <span class="font-bold text-interview-primary">{{ question.relevance_score }}/5</span>
                </div>
                <div class="bg-interview-surface px-4 py-3 rounded-xl text-center border border-interview-surface-border">
                  <span class="text-xs text-interview-text-secondary block mb-1">Logical Thinking</span>
                  <span class="font-bold text-interview-primary">{{ question.logical_thinking_score }}/5</span>
                </div>
              </div>

              <!-- Transcript -->
              <div v-if="question.transcript" class="mb-6">
                <h4 class="text-sm font-bold text-interview-primary mb-2">Candidate's Answer:</h4>
                <p class="bg-interview-surface p-4 rounded-xl text-interview-text-primary leading-relaxed border border-interview-surface-border">
                  {{ question.transcript }}
                </p>
              </div>
              <div v-else class="mb-6">
                <div class="bg-interview-surface/50 p-6 rounded-xl border border-interview-surface-border text-center">
                  <p class="text-interview-text-muted italic flex items-center justify-center gap-2">
                    <ExclamationTriangleIcon class="w-5 h-5 opacity-70" />
                    ผู้สมัครไม่ได้ตอบคำถามข้อนี้ หรือข้ามการตอบคำถาม (No answer provided)
                  </p>
                </div>
              </div>

              <!-- Feedback -->
              <div v-if="question.feedback" class="space-y-4">
                <div
                  v-if="question.feedback.strengths"
                  class="p-4 bg-interview-success/10 border-l-4 border-interview-success rounded-r-xl"
                >
                  <h4 class="flex items-center gap-2 font-bold text-interview-success mb-1">
                    <FireIcon class="w-4 h-4" />
                    Strengths:
                  </h4>
                  <p class="text-interview-text-primary">{{ question.feedback.strengths }}</p>
                </div>

                <div
                  v-if="question.feedback.weaknesses"
                  class="p-4 bg-interview-warning/10 border-l-4 border-interview-warning rounded-r-xl"
                >
                  <h4 class="flex items-center gap-2 font-bold text-interview-warning mb-1">
                    <ExclamationTriangleIcon class="w-4 h-4" />
                    Areas for Improvement:
                  </h4>
                  <p class="text-interview-text-primary">{{ question.feedback.weaknesses }}</p>
                </div>

                <div
                  v-if="question.feedback.summary"
                  class="p-4 bg-interview-accent-sky/10 border-l-4 border-interview-accent-sky rounded-r-xl"
                >
                  <h4 class="flex items-center gap-2 font-bold text-interview-accent-sky mb-1">
                    <DocumentTextIcon class="w-4 h-4" />
                    Summary:
                  </h4>
                  <p class="text-interview-text-primary">{{ question.feedback.summary }}</p>
                </div>

                <div
                  v-if="question.feedback.reasoning"
                  class="p-4 bg-interview-primary/10 border-l-4 border-interview-primary rounded-r-xl"
                >
                  <h4 class="flex items-center gap-2 font-bold text-interview-primary mb-1">
                    <MicrophoneIcon class="w-4 h-4" />
                    เหตุผลการให้คะแนน (Reasoning):
                  </h4>
                  <p class="text-interview-text-primary">{{ question.feedback.reasoning }}</p>
                </div>
              </div>
            </div>
          </Transition>
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
  DocumentTextIcon,
  ArrowLeftIcon,
  ChevronDownIcon,
  VideoCameraIcon,
  MicrophoneIcon
} from '@heroicons/vue/24/solid'
import ScoreCard from '../../../components/charts/ScoreCard.vue'
import ScoreRadarChart from '../../../components/charts/ScoreRadarChart.vue'
import ScoreBarChart from '../../../components/charts/ScoreBarChart.vue'

definePageMeta({
  layout: 'hr',
  middleware: ['hr']
})

const route = useRoute()
const router = useRouter()
const { getReportDetails, downloadPDF } = useReports()

interface Question {
  id: number;
  question: string;
  pass_prediction: boolean;
  average_score: number;
  communication_score: number;
  relevance_score: number;
  logical_thinking_score: number;
  transcript: string;
  video_url?: string;
  feedback?: {
    strengths?: string;
    weaknesses?: string;
    summary?: string;
    reasoning?: string;
  };
}

interface AggregatedScore {
  average_score: number;
  communication_avg: number;
  relevance_avg: number;
  logical_thinking_avg: number;
  pass_rate: number;
  questions_answered: number;
  total_questions: number;
  overall_recommendation: string;
}

interface Candidate {
  id: string;
  name: string;
  email: string;
  role_id: string;
  interview_date: string;
}

interface Report {
  session_id: string;
  candidate: Candidate;
  aggregated_score: AggregatedScore;
  questions: Question[];
}

const sessionId = computed(() => route.params.sessionId as string)
const report = ref<Report | null>(null)
const loading = ref(true)
const error = ref('')
const expandedQuestions = ref<Record<number, boolean>>({})

onMounted(async () => {
  await loadReport()
})

const loadReport = async () => {
  try {
    loading.value = true
    error.value = ''
    report.value = await getReportDetails(sessionId.value) as unknown as Report
  } catch (err: any) {
    error.value = err.message || 'Failed to load report'
  } finally {
    loading.value = false
  }
}

const toggleQuestion = (idx: number) => {
  expandedQuestions.value[idx] = !expandedQuestions.value[idx]
}

const handleDownloadPDF = async () => {
  try {
    await downloadPDF(sessionId.value)
  } catch (err: any) {
    alert('Failed to download PDF: ' + err.message)
  }
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
}

const getScoreClass = (score: number) => {
  if (score >= 4) return 'bg-interview-success/20 text-interview-success'
  if (score >= 3) return 'bg-interview-accent-sky/20 text-interview-accent-sky'
  if (score >= 2) return 'bg-interview-primary/20 text-interview-primary'
  return 'bg-interview-warning/20 text-interview-warning'
}

const getRecommendationClass = (rec: string) => {
  if (rec === 'Strong Pass') return 'bg-interview-success text-white shadow-glow-green'
  if (rec === 'Pass') return 'bg-interview-accent-sky text-white shadow-glow-blue'
  if (rec === 'Review') return 'bg-interview-primary text-interview-bg shadow-glow-amber'
  return 'bg-interview-warning text-white shadow-glow-red'
}

const getVideoUrl = (path: string) => {
  if (!path) return ''
  // If absolute URL, return as is
  if (path.startsWith('http')) return path
  
  const config = useRuntimeConfig()
  const baseURL = (config.public.apiBaseUrl as string) || 'http://localhost:8000'
  
  // Ensure we don't double slash if base ends with / and path starts with /
  const cleanBase = baseURL.replace(/\/$/, '')
  const cleanPath = path.startsWith('/') ? path : `/${path}`
  
  return `${cleanBase}${cleanPath}`
}
</script>

<style scoped>
.report-card {
  animation: report-fade-in 0.4s cubic-bezier(0.16, 1, 0.3, 1) backwards;
  animation-delay: var(--delay, 0ms);
}

@keyframes report-fade-in {
  from {
    opacity: 0;
    transform: translate3d(0, 20px, 0);
  }
  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
}
</style>
