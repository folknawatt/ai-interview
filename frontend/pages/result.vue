<template>
  <div
    class="min-h-screen bg-interview-bg text-interview-text-primary flex items-center justify-center p-8 relative overflow-hidden"
    role="main"
    aria-labelledby="result-title"
  >
    <!-- Background gradient effects -->
    <div class="fixed inset-0 z-0 bg-interview-bg">
      <div class="absolute inset-0 bg-gradient-to-b from-black/80 via-interview-bg to-black" aria-hidden="true"></div>
      <div
        class="absolute top-1/4 -left-32 w-96 h-96 bg-interview-success/10 rounded-full blur-3xl"
        aria-hidden="true"
      ></div>
      <div
        class="absolute bottom-1/4 -right-32 w-96 h-96 bg-interview-primary/10 rounded-full blur-3xl"
        aria-hidden="true"
      ></div>
    </div>

    <div class="relative z-10 max-w-xl w-full text-center animate-fade-in-up">
      <!-- Success Icon -->
      <div class="mb-8" role="status" aria-live="polite">
        <div
          class="w-24 h-24 bg-interview-success/10 rounded-full flex items-center justify-center mx-auto mb-6 animate-float border border-interview-success/30"
        >
          <CheckCircleIcon class="w-16 h-16 text-interview-success" aria-hidden="true" />
        </div>
        <h1 id="result-title" class="text-3xl font-bold text-interview-text-primary mb-2">
          {{ $t('result.title') }}
        </h1>
        <p class="text-lg text-interview-text-secondary">Interview Completed</p>
      </div>

      <!-- Thank You Message -->
      <div
        class="bg-interview-surface backdrop-blur-xl p-8 rounded-2xl border border-interview-surface-border shadow-glass mb-8"
        role="region"
        aria-label="ข้อความขอบคุณ"
      >
        <p class="text-xl text-interview-text-primary mb-4">{{ $t('result.thankYou') }}</p>
        <p class="text-interview-text-secondary">{{ $t('result.message') }}</p>
      <p class="text-interview-text-secondary mt-2">{{ $t('result.followUp') }}</p>
      </div>

      <!-- Action Button -->
      <div>
        <button
          @click="handleFinish"
          class="px-8 py-3 bg-interview-primary text-interview-bg font-semibold rounded-xl hover:bg-interview-primary-hover shadow-glow-amber transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-interview-primary focus:ring-offset-2 focus:ring-offset-interview-bg"
          aria-label="กลับสู่หน้าหลัก"
        >
          {{ $t('result.backToHome') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { CheckCircleIcon } from '@heroicons/vue/24/solid'

definePageMeta({
  layout: 'blank'
})

const { resetInterview } = useInterview()
const router = useRouter()

const handleFinish = () => {
  resetInterview()
  router.push('/login')
}
</script>
