<template>
  <div class="min-h-screen bg-minimal-bg text-minimal-text-primary flex items-center justify-center p-8">
    <div class="max-w-xl w-full text-center">
      <!-- Success Icon -->
      <div class="mb-8">
        <div class="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <CheckCircleIcon class="w-16 h-16 text-green-500" />
        </div>
        <h1 class="text-3xl font-bold text-minimal-text-primary mb-2">
          สัมภาษณ์เสร็จสิ้น
        </h1>
        <p class="text-lg text-minimal-text-secondary">
          Interview Completed
        </p>
      </div>

      <!-- Thank You Message -->
      <div class="bg-minimal-card p-8 rounded-xl shadow-sm border border-minimal-border mb-8">
        <p class="text-xl text-minimal-text-primary mb-4">
          ขอบคุณที่เข้าร่วมการสัมภาษณ์
        </p>
        <p class="text-minimal-text-secondary">
          ผลการสัมภาษณ์จะถูกส่งให้ทีม HR ดำเนินการต่อไป
        </p>
        <p class="text-minimal-text-secondary mt-2">
          เราจะติดต่อกลับภายใน 3-5 วันทำการ
        </p>
      </div>

      <!-- Action Button -->
      <button
        @click="startNewInterview"
        class="px-8 py-4 bg-minimal-info hover:bg-sky-600 text-white rounded-lg font-semibold transition-all shadow-sm text-lg"
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
