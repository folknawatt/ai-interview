<template>
  <div class="min-h-screen bg-interview-bg flex items-center justify-center p-4">
    <div class="text-center space-y-8 animate-fade-in-up">
      <!-- 404 Visualization -->
      <div class="relative">
        <h1 class="text-9xl font-bold text-interview-surface-border opacity-20 select-none">404</h1>
        <div class="absolute inset-0 flex items-center justify-center">
          <div class="text-6xl animate-bounce">🤔</div>
        </div>
      </div>

      <!-- Message -->
      <div class="space-y-4 max-w-md mx-auto">
        <h2 class="text-2xl font-bold text-interview-text-primary">ไม่พบหน้าที่คุณต้องการ</h2>
        <p class="text-interview-text-secondary">
          ขออภัย หน้าที่คุณกำลังตามหาอาจถูกย้าย ลบ หรือไม่มีอยู่จริงในระบบ
        </p>
      </div>

      <!-- Action -->
      <div>
        <button
          @click="handleError"
          class="px-8 py-3 bg-interview-primary text-interview-bg font-semibold rounded-xl hover:bg-interview-primary-hover shadow-glow-amber transition-all duration-300 transform hover:scale-105"
        >
          กลับสู่หน้าหลัก
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { NuxtError } from '#app'

const props = defineProps({
  error: Object as () => NuxtError,
})

const handleError = () => {
  clearError({ redirect: '/login' })
}
</script>
