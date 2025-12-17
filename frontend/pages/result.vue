<template>
  <div class="min-h-screen bg-minimal-bg text-minimal-text-primary p-8">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold mb-6 text-center flex items-center justify-center gap-3">
        <ChartBarIcon class="w-8 h-8 text-minimal-info" />
        ผลการวิเคราะห์ (Analysis Result)
      </h1>

      <div v-if="loading" class="text-center py-12">
        <div
          class="animate-spin rounded-full h-12 w-12 border-b-2 border-minimal-info mx-auto mb-4"
        ></div>
        <p class="text-minimal-text-secondary">กำลังประมวลผลคะแนน...</p>
      </div>

      <div
        v-else-if="error"
        class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative"
        role="alert"
      >
        <strong class="font-bold">Error: </strong>
        <span class="block sm:inline">{{ error }}</span>
      </div>

      <div v-else-if="!result" class="text-center py-12 text-gray-500">ไม่พบข้อมูลผลลัพธ์</div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Scores -->
        <div class="bg-minimal-card p-6 rounded-lg shadow-sm border border-minimal-border">
          <h2 class="text-xl font-semibold mb-4">คะแนนประเมิน (Scores)</h2>
          <div class="grid grid-cols-2 gap-4">
            <div
              class="bg-sky-50 p-4 rounded border border-sky-200 text-center flex flex-col items-center"
            >
              <div class="text-sm text-minimal-text-secondary mb-2">Communication</div>
              <ScoreCard :score="Number(result.scores.communication)" :size="80" />
            </div>
            <div
              class="bg-sky-50 p-4 rounded border border-sky-200 text-center flex flex-col items-center"
            >
              <div class="text-sm text-minimal-text-secondary mb-2">Relevance</div>
              <ScoreCard :score="Number(result.scores.relevance)" :size="80" />
            </div>
            <div
              class="bg-sky-50 p-4 rounded border border-sky-200 text-center flex flex-col items-center"
            >
              <div class="text-sm text-minimal-text-secondary mb-2">Logical Thinking</div>
              <ScoreCard :score="Number(result.scores.logical_thinking)" :size="80" />
            </div>
            <div
              class="bg-sky-50 p-4 rounded border border-sky-200 text-center flex flex-col items-center"
            >
              <div class="text-sm text-minimal-text-secondary mb-2">Average Score</div>
              <ScoreCard :score="Number(result.scores.total)" :maxScore="10" :size="80" />
            </div>
          </div>
        </div>

        <!-- Pass/Fail -->
        <div
          class="bg-minimal-card p-6 rounded-lg shadow-sm border border-minimal-border flex flex-col items-center justify-center"
        >
          <h2 class="text-xl font-semibold mb-4">ผลสรุป (Conclusion)</h2>
          <div v-if="result.pass_prediction" class="text-center">
            <div class="flex justify-center mb-2">
              <CheckCircleIcon class="w-16 h-16 text-minimal-success" />
            </div>
            <div class="text-2xl font-bold text-minimal-success">ผ่าน (PASS)</div>
          </div>
          <div v-else class="text-center">
            <div class="flex justify-center mb-2">
              <XCircleIcon class="w-16 h-16 text-minimal-warning" />
            </div>
            <div class="text-2xl font-bold text-minimal-warning">ไม่ผ่าน (FAIL)</div>
          </div>
        </div>

        <!-- Feedback -->
        <FeedbackSection
          :strengths="result.feedback.strengths"
          :weaknesses="result.feedback.weaknesses"
          :summary="result.feedback.summary"
        />
      </div>

      <!-- Action Buttons -->
      <div class="mt-8 text-center space-x-4">
        <button
          @click="startNewInterview"
          class="px-6 py-3 bg-minimal-info hover:bg-sky-600 text-white rounded-lg font-semibold transition-all shadow-sm"
        >
          เริ่มสัมภาษณ์ใหม่
        </button>
        <NuxtLink
          to="/hr/dashboard"
          class="inline-block px-6 py-3 bg-minimal-text-secondary hover:bg-minimal-text-primary text-white rounded-lg font-semibold transition-all shadow-sm"
        >
          HR Dashboard
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ChartBarIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/vue/24/solid'
import ScoreCard from '../components/charts/ScoreCard.vue'
import FeedbackSection from '../components/interview/FeedbackSection.vue'

const { sessionId, getSummary, resetInterview } = useInterview()
const router = useRouter()

// State for aggregated results
const loading = ref(true)
const error = ref('')
const aggregatedScore = ref<any>(null)
const questionResults = ref<any[]>([])

// Fetch aggregated scores on mount
onMounted(async () => {
  if (!sessionId.value) {
    // No session, redirect to login
    router.push('/login')
    return
  }

  try {
    loading.value = true
    const summary = await getSummary()

    if (summary.aggregated_score) {
      aggregatedScore.value = summary.aggregated_score
      questionResults.value = summary.details || []
    } else {
      error.value = 'ยังไม่มีผลคะแนนรวม กรุณารอสักครู่'
    }
  } catch (err: any) {
    console.error('Error fetching summary:', err)
    error.value = 'ไม่สามารถโหลดผลคะแนนได้'
  } finally {
    loading.value = false
  }
})

// Computed result for template (transform aggregated score to match old format)
const result = computed(() => {
  if (!aggregatedScore.value) return null

  const agg = aggregatedScore.value
  const isPassed =
    agg.overall_recommendation === 'Strong Pass' || agg.overall_recommendation === 'Pass'

  // Helper to extract non-empty feedback items
  const extractFeedback = (key: string) => {
    return questionResults.value
      .map(q => q.evaluation?.feedback?.[key])
      .filter(item => item && item.trim() !== '' && item !== 'None')
  }

  return {
    scores: {
      communication: agg.communication_avg.toFixed(1),
      relevance: agg.relevance_avg.toFixed(1),
      logical_thinking: agg.logical_thinking_avg.toFixed(1),
      total: agg.average_score.toFixed(1),
    },
    pass_prediction: isPassed,
    feedback: {
      strengths: extractFeedback('strengths'),

      summary: `ผลการประเมินโดยรวม: ${agg.overall_recommendation} (คะแนนเฉลี่ย ${agg.average_score.toFixed(1)}/10)`,
      // Merge reasoning into weaknesses
      weaknesses: [
        ...extractFeedback('weaknesses'),
        ...extractFeedback('reasoning').map(r => `(เพิ่ม) การลำดับความคิด: ${r}`),
      ],
      reasonings: [], // Clear this so it doesn't show up elsewhere if verified
    },
  }
})

const startNewInterview = () => {
  resetInterview()
  router.push('/login')
}
</script>
