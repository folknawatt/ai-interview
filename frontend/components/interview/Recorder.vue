<template>
  <div class="w-full max-w-4xl bg-minimal-card p-6 rounded-lg shadow-sm border border-minimal-border">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold text-minimal-text-primary flex items-center gap-2">
        <VideoCameraIcon class="w-7 h-7 text-minimal-info" />
        บันทึกคำตอบ (Record Answer)
      </h2>
      <div
        class="text-2xl font-mono font-bold transition-colors"
        :class="isRecording ? 'text-minimal-warning' : 'text-minimal-text-primary'"
      >
        {{ formatTime(timer) }}
      </div>
    </div>

    <div
      class="relative aspect-video bg-black rounded-lg overflow-hidden mb-6 border border-minimal-border"
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
        class="absolute inset-0 flex items-center justify-center bg-black/50"
      >
        <p class="text-minimal-text-muted">กดปุ่ม "เริ่มอัดวิดีโอ" เมื่อพร้อม</p>
      </div>
    </div>

    <div class="flex justify-center space-x-4">
      <button
        v-if="!isRecording && !recordedBlob"
        @click="$emit('start')"
        class="inline-flex items-center px-6 py-3 text-lg font-semibold text-white bg-minimal-focus rounded-lg hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-minimal-focus focus:ring-offset-2 transition-all shadow-sm"
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
        class="inline-flex items-center px-6 py-3 text-lg font-semibold text-white bg-minimal-warning rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-minimal-warning focus:ring-offset-2 transition-all shadow-sm animate-pulse"
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
        class="inline-flex items-center px-6 py-3 text-lg font-semibold text-white bg-minimal-info rounded-lg hover:bg-sky-600 focus:outline-none focus:ring-2 focus:ring-minimal-info focus:ring-offset-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
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
        class="inline-flex items-center px-6 py-3 text-lg font-semibold text-minimal-text-secondary border-2 border-minimal-border rounded-lg hover:bg-minimal-border hover:text-minimal-text-primary focus:outline-none focus:ring-2 focus:ring-minimal-border focus:ring-offset-2 transition-all"
      >
        อัดใหม่
      </button>
    </div>

    <div v-if="isSubmitting" class="mt-4 text-center text-minimal-text-secondary animate-pulse">
      กำลังอัพโหลดและวิเคราะห์ผล...
    </div>
    <div v-if="error" class="mt-4 text-center text-minimal-warning">
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
