<template>
  <div class="min-h-screen bg-minimal-bg text-minimal-text-primary p-8">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold mb-6 text-center flex items-center justify-center gap-3">
        <ChartBarIcon class="w-8 h-8 text-minimal-info" />
        ผลการวิเคราะห์ (Analysis Result)
      </h1>

      <div v-if="result" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Scores -->
        <div class="bg-minimal-card p-6 rounded-lg shadow-sm border border-minimal-border">
          <h2 class="text-xl font-semibold mb-4">คะแนนประเมิน (Scores)</h2>
          <div class="grid grid-cols-2 gap-4">
            <div class="bg-sky-50 p-4 rounded border border-sky-200 text-center">
              <div class="text-sm text-minimal-text-secondary">Communication</div>
              <div class="text-2xl font-bold text-minimal-info">
                {{ result.scores.communication }}/10
              </div>
            </div>
            <div class="bg-sky-50 p-4 rounded border border-sky-200 text-center">
              <div class="text-sm text-minimal-text-secondary">Relevance</div>
              <div class="text-2xl font-bold text-minimal-info">
                {{ result.scores.relevance }}/10
              </div>
            </div>
            <div class="bg-sky-50 p-4 rounded border border-sky-200 text-center">
              <div class="text-sm text-minimal-text-secondary">Quality</div>
              <div class="text-2xl font-bold text-minimal-info">
                {{ result.scores.quality }}/10
              </div>
            </div>
            <div class="bg-emerald-50 p-4 rounded border-2 border-minimal-success text-center">
              <div class="text-sm text-minimal-text-secondary">Total Score</div>
              <div class="text-3xl font-bold text-minimal-success">
                {{ result.scores.total }}/30
              </div>
            </div>
          </div>
        </div>

        <!-- Pass/Fail -->
        <div class="bg-minimal-card p-6 rounded-lg shadow-sm border border-minimal-border flex flex-col items-center justify-center">
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
        <div class="bg-minimal-card p-6 rounded-lg shadow-sm border border-minimal-border md:col-span-2">
          <h2 class="text-xl font-semibold mb-4">คำติชม (Feedback)</h2>
          <div class="space-y-4">
            <div>
              <h3 class="text-sm font-medium text-minimal-success mb-1 flex items-center gap-1">
                <SparklesIcon class="w-4 h-4" />
                จุดแข็ง
              </h3>
              <p class="text-minimal-text-secondary">{{ result.feedback.strengths }}</p>
            </div>
            <div>
              <h3 class="text-sm font-medium text-amber-500 mb-1 flex items-center gap-1">
                <ExclamationTriangleIcon class="w-4 h-4" />
                จุดที่ควรพัฒนา
              </h3>
              <p class="text-minimal-text-secondary">{{ result.feedback.weaknesses }}</p>
            </div>
            <div>
              <h3 class="text-sm font-medium text-minimal-info mb-1 flex items-center gap-1">
                <DocumentTextIcon class="w-4 h-4" />
                สรุป
              </h3>
              <p class="text-minimal-text-secondary">{{ result.feedback.summary }}</p>
            </div>
          </div>
        </div>
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
import {
  ChartBarIcon,
  CheckCircleIcon,
  XCircleIcon,
  SparklesIcon,
  ExclamationTriangleIcon,
  DocumentTextIcon
} from '@heroicons/vue/24/solid';

const { sessionId, getSummary, resetInterview } = useInterview();
const router = useRouter();

// State for aggregated results
const loading = ref(true);
const error = ref('');
const aggregatedScore = ref<any>(null);

// Fetch aggregated scores on mount
onMounted(async () => {
  if (!sessionId.value) {
    // No session, redirect to login
    router.push('/login');
    return;
  }

  try {
    loading.value = true;
    const summary = await getSummary();
    
    if (summary.aggregated_score) {
      aggregatedScore.value = summary.aggregated_score;
    } else {
      error.value = 'ยังไม่มีผลคะแนนรวม กรุณารอสักครู่';
    }
  } catch (err: any) {
    console.error('Error fetching summary:', err);
    error.value = 'ไม่สามารถโหลดผลคะแนนได้';
  } finally {
    loading.value = false;
  }
});

// Computed result for template (transform aggregated score to match old format)
const result = computed(() => {
  if (!aggregatedScore.value) return null;
  
  const agg = aggregatedScore.value;
  const isPassed = agg.overall_recommendation === 'Strong Pass' || agg.overall_recommendation === 'Pass';
  
  return {
    scores: {
      communication: agg.communication_avg.toFixed(1),
      relevance: agg.relevance_avg.toFixed(1),
      quality: agg.quality_avg.toFixed(1),
      total: agg.total_score.toFixed(1)
    },
    pass_prediction: isPassed,
    feedback: {
      strengths: `คุณตอบคำถามได้ ${agg.questions_answered} จาก ${agg.total_questions} ข้อ`,
      weaknesses: `อัตราผ่านต่อคำถาม: ${agg.pass_rate.toFixed(1)}%`,
      summary: `ผลการประเมินโดยรวม: ${agg.overall_recommendation} (คะแนนเฉลี่ย ${agg.total_score.toFixed(1)}/10)`
    }
  };
});

const startNewInterview = () => {
  resetInterview();
  router.push('/login');
};
</script>
