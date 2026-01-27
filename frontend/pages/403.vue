<template>
  <div
    class="min-h-screen bg-interview-bg text-interview-text-primary flex flex-col items-center justify-center p-4 relative overflow-hidden"
  >
    <!-- Background Effects -->
    <div class="fixed inset-0 z-0 bg-interview-bg">
      <div class="absolute inset-0 bg-gradient-to-b from-black/80 via-interview-bg to-black"></div>
      <div class="absolute top-1/4 -left-32 w-96 h-96 bg-red-500/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-1/4 -right-32 w-96 h-96 bg-interview-primary/5 rounded-full blur-3xl"></div>
    </div>

    <!-- Content -->
    <div
      class="relative z-10 w-full max-w-md bg-interview-surface backdrop-blur-xl p-10 rounded-2xl border border-interview-surface-border shadow-glass text-center animate-fade-in-up"
    >
      <div class="mb-6">
        <div class="w-20 h-20 mx-auto bg-red-500/20 rounded-full flex items-center justify-center mb-4">
          <ShieldExclamationIcon class="w-10 h-10 text-red-400" />
        </div>
        <h1 class="text-4xl font-bold text-interview-text-primary mb-2">403</h1>
        <h2 class="text-xl font-semibold text-interview-text-secondary mb-4">ไม่มีสิทธิ์เข้าถึง</h2>
        <p class="text-interview-text-muted text-sm">
          คุณไม่มีสิทธิ์ในการเข้าถึงหน้านี้ กรุณาติดต่อผู้ดูแลระบบหากคุณเชื่อว่านี่เป็นข้อผิดพลาด
        </p>
      </div>

      <div class="flex flex-col gap-3">
        <NuxtLink
          to="/"
          class="w-full px-6 py-3 bg-interview-primary text-interview-bg font-semibold rounded-xl hover:bg-interview-primary-hover transition-all duration-300 shadow-glow-amber"
        >
          กลับหน้าหลัก
        </NuxtLink>
        <NuxtLink
          to="/login"
          class="w-full px-6 py-3 bg-interview-surface border border-interview-surface-border text-interview-text-secondary font-semibold rounded-xl hover:bg-interview-surface-hover hover:text-interview-text-primary transition-all duration-300"
        >
          เข้าสู่ระบบด้วยบัญชีอื่น
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ShieldExclamationIcon } from '@heroicons/vue/24/solid'

definePageMeta({
  layout: 'blank'
})
</script>
