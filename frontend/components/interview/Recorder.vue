<template>
  <div class="w-full max-w-4xl bg-interview-surface backdrop-blur-xl p-6 rounded-2xl border border-interview-surface-border shadow-glass animate-fade-in-up">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold text-interview-text-primary flex items-center gap-2">
        <VideoCameraIcon class="w-7 h-7 text-interview-primary" />
        บันทึกคำตอบ (Record Answer)
      </h2>
      <div
        class="text-2xl font-mono font-bold transition-colors duration-300"
        :class="isRecording ? 'text-red-500 animate-pulse' : 'text-interview-text-primary'"
      >
        {{ formatTime(timer) }}
      </div>
    </div>

    <div
      class="relative aspect-video bg-black rounded-xl overflow-hidden mb-6 border border-interview-surface-border"
    >
      <video
        ref="videoRef"
        autoplay
        muted
        playsinline
        class="w-full h-full object-cover"
      ></video>

      <div
        v-if="!isRecording && !recordedBlob"
        class="absolute inset-0 flex items-center justify-center bg-black/60"
      >
        <p class="text-interview-text-muted">กดปุ่ม "เริ่มอัดวิดีโอ" เมื่อพร้อม</p>
      </div>

      <!-- Recording indicator -->
      <div v-if="isRecording" class="absolute top-4 left-4 flex items-center gap-2 bg-red-500/90 px-3 py-1.5 rounded-full">
        <div class="w-3 h-3 bg-white rounded-full animate-pulse"></div>
        <span class="text-sm font-medium text-white">REC</span>
      </div>
    </div>

    <div class="flex justify-center space-x-4">
      <button
        v-if="!isRecording && !recordedBlob"
        @click="$emit('start')"
        class="inline-flex items-center px-6 py-3 text-lg font-semibold text-interview-bg bg-interview-primary rounded-xl hover:bg-interview-primary-hover focus:outline-none focus:ring-2 focus:ring-interview-primary focus:ring-offset-2 focus:ring-offset-interview-bg transition-all duration-300 shadow-glow-amber hover:shadow-glow-amber-lg"
      >
        <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
          ></path>
        </svg>
        เริ่มอัดวิดีโอ
      </button>

      <button
        v-if="isRecording"
        @click="$emit('stop')"
        class="inline-flex items-center px-6 py-3 text-lg font-semibold text-white bg-red-500 rounded-xl hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 focus:ring-offset-interview-bg transition-all shadow-lg animate-pulse"
      >
        <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          ></path>
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z"
          ></path>
        </svg>
        หยุดอัด
      </button>

      <button
        v-if="recordedBlob"
        @click="$emit('submit')"
        :disabled="isSubmitting"
        class="inline-flex items-center px-6 py-3 text-lg font-semibold text-interview-bg bg-interview-primary rounded-xl hover:bg-interview-primary-hover focus:outline-none focus:ring-2 focus:ring-interview-primary focus:ring-offset-2 focus:ring-offset-interview-bg transition-all duration-300 disabled:opacity-40 disabled:cursor-not-allowed shadow-glow-amber hover:shadow-glow-amber-lg"
      >
        <svg
          v-if="!isSubmitting"
          class="w-6 h-6 mr-2"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
          ></path>
        </svg>
        <svg v-else class="animate-spin w-6 h-6 mr-2" fill="none" viewBox="0 0 24 24">
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          ></circle>
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
        ส่งคำตอบ
      </button>

      <button
        v-if="recordedBlob && !isSubmitting"
        @click="$emit('reset')"
        class="inline-flex items-center px-6 py-3 text-lg font-semibold text-interview-text-secondary border-2 border-interview-surface-border rounded-xl hover:bg-interview-surface-hover hover:text-interview-text-primary focus:outline-none focus:ring-2 focus:ring-interview-surface-border focus:ring-offset-2 focus:ring-offset-interview-bg transition-all duration-300"
      >
        อัดใหม่
      </button>
    </div>

    <div v-if="isSubmitting" class="mt-4 text-center text-interview-text-secondary animate-pulse">
      กำลังอัพโหลดและวิเคราะห์ผล...
    </div>
    <div v-if="error" class="mt-4 text-center text-red-400">
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { VideoCameraIcon } from '@heroicons/vue/24/solid'

defineProps<{
  isRecording: boolean
  isSubmitting: boolean
  recordedBlob: Blob | null
  timer: number
  formatTime: (seconds: number) => string
  error: string | null
}>()

const videoRef = ref<HTMLVideoElement | null>(null)

defineExpose({
  videoRef
})

defineEmits(['start', 'stop', 'submit', 'reset'])
</script>
