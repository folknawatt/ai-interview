<template>
  <div class="min-h-screen bg-interview-bg text-interview-text-primary flex items-center justify-center p-8 relative overflow-hidden">
    <!-- Background gradient effects -->
    <div class="absolute inset-0 bg-gradient-to-br from-interview-bg via-interview-bg-secondary to-interview-bg-gradient"></div>
    <div class="absolute top-1/4 -left-32 w-96 h-96 bg-interview-success/10 rounded-full blur-3xl"></div>
    <div class="absolute bottom-1/4 -right-32 w-96 h-96 bg-interview-primary/10 rounded-full blur-3xl"></div>

    <div class="relative max-w-xl w-full text-center animate-fade-in-up">
      <!-- Success Icon -->
      <div class="mb-8">
        <div class="w-24 h-24 bg-interview-success/10 rounded-full flex items-center justify-center mx-auto mb-6 animate-float border border-interview-success/30">
          <CheckCircleIcon class="w-16 h-16 text-interview-success" />
        </div>
        <h1 class="text-3xl font-bold text-interview-text-primary mb-2">
          สัมภาษณ์เสร็จสิ้น
        </h1>
        <p class="text-lg text-interview-text-secondary">
          Interview Completed
        </p>
      </div>

      <!-- Thank You Message -->
      <div class="bg-interview-surface backdrop-blur-xl p-8 rounded-2xl border border-interview-surface-border shadow-glass mb-8">
        <p class="text-xl text-interview-text-primary mb-4">
          ขอบคุณที่เข้าร่วมการสัมภาษณ์
        </p>
        <p class="text-interview-text-secondary">
          ผลการสัมภาษณ์จะถูกส่งให้ทีม HR ดำเนินการต่อไป
        </p>
        <p class="text-interview-text-secondary mt-2">
          เราจะติดต่อกลับภายใน 3-5 วันทำการ
        </p>
      </div>

      <!-- Action Button -->
      <button
        @click="startNewInterview"
        class="px-8 py-4 bg-interview-primary hover:bg-interview-primary-hover text-interview-bg rounded-xl font-semibold transition-all duration-300 shadow-glow-amber hover:shadow-glow-amber-lg text-lg"
      >
        เริ่มสัมภาษณ์ใหม่
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { CheckCircleIcon } from '@heroicons/vue/24/solid'

const { resetInterview } = useInterview()
const router = useRouter()

const startNewInterview = () => {
  resetInterview()
  router.push('/login')
}
</script>
