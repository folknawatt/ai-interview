<template>
  <div
    class="w-full max-w-4xl bg-interview-surface backdrop-blur-xl p-6 rounded-2xl border border-interview-surface-border shadow-glass animate-fade-in-up"
  >
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
      <video ref="videoRef" autoplay muted playsinline class="w-full h-full object-cover"></video>

      <div
        v-if="!isRecording && !recordedBlob"
        class="absolute inset-0 flex flex-col items-center justify-center bg-black/60"
      >
        <div v-if="countdown > 0" class="text-6xl font-bold font-mono text-white animate-pulse mb-4">
          {{ countdown }}
        </div>
        <p class="text-interview-text-muted">วิดีโอจะเริ่มบันทึกอัตโนมัติ</p>
      </div>

      <!-- Recording indicator -->
      <div
        v-if="isRecording"
        class="absolute top-4 left-4 flex items-center gap-2 bg-red-500/90 px-3 py-1.5 rounded-full"
      >
        <div class="w-3 h-3 bg-white rounded-full animate-pulse"></div>
        <span class="text-sm font-medium text-white">REC</span>
      </div>
    </div>

    <div class="flex justify-center space-x-4">
      <button
        v-if="!isRecording && !recordedBlob"
        @click="startNow"
        class="inline-flex items-center px-6 py-3 text-lg font-semibold text-interview-bg bg-interview-primary rounded-xl hover:bg-interview-primary-hover focus:outline-none focus:ring-2 focus:ring-interview-primary focus:ring-offset-2 focus:ring-offset-interview-bg transition-all duration-300 shadow-glow-amber hover:shadow-glow-amber-lg group"
      >
        <VideoCameraIcon
          class="w-6 h-6 mr-2 transition-transform duration-300 group-hover:scale-110"
        />
        เริ่มอัดเดี๋ยวนี้
      </button>

      <button
        v-if="isRecording"
        @click="$emit('stop')"
        class="inline-flex items-center px-6 py-3 text-lg font-semibold text-white bg-interview-warning rounded-xl hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-interview-warning focus:ring-offset-2 focus:ring-offset-interview-bg transition-all shadow-lg animate-pulse"
      >
        <StopIcon class="w-6 h-6 mr-2 animate-pulse" />
        หยุดอัด
      </button>

      <button
        v-if="recordedBlob"
        @click="$emit('submit')"
        :disabled="isSubmitting"
        class="inline-flex items-center px-6 py-3 text-lg font-semibold text-interview-bg bg-interview-primary rounded-xl hover:bg-interview-primary-hover focus:outline-none focus:ring-2 focus:ring-interview-primary focus:ring-offset-2 focus:ring-offset-interview-bg transition-all duration-300 disabled:opacity-40 disabled:cursor-not-allowed shadow-glow-amber hover:shadow-glow-amber-lg group"
      >
        <PaperAirplaneIcon
          v-if="!isSubmitting"
          class="w-6 h-6 mr-2 -rotate-45 transition-transform duration-300 group-hover:translate-x-1 group-hover:-translate-y-1"
        />
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
        {{ isSubmitting ? 'กำลังส่ง...' : 'ส่งคำตอบ' }}
      </button>

      <button
        v-if="recordedBlob && !isSubmitting"
        @click="$emit('reset')"
        class="inline-flex items-center px-6 py-3 text-lg font-semibold text-interview-text-secondary border-2 border-interview-surface-border rounded-xl hover:bg-interview-surface-hover hover:text-interview-text-primary focus:outline-none focus:ring-2 focus:ring-interview-surface-border focus:ring-offset-2 focus:ring-offset-interview-bg transition-all duration-300 group"
      >
        <ArrowPathIcon
          class="w-5 h-5 mr-2 transition-transform duration-500 group-hover:rotate-180"
        />
        อัดใหม่
      </button>
    </div>

    <div v-if="isSubmitting" class="mt-4 text-center text-interview-text-secondary animate-pulse">
      กำลังอัพโหลดและวิเคราะห์ผล...
    </div>
    <div v-if="error" class="mt-4 text-center text-interview-warning">
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import {
  VideoCameraIcon,
  StopIcon,
  PaperAirplaneIcon,
  ArrowPathIcon,
} from '@heroicons/vue/24/solid'

const props = defineProps<{
  isRecording: boolean
  isSubmitting: boolean
  recordedBlob: Blob | null
  timer: number
  formatTime: (seconds: number) => string
  error: string | null
}>()

const videoRef = ref<HTMLVideoElement | null>(null)

defineExpose({
  videoRef,
})

const emit = defineEmits(['start', 'stop', 'submit', 'reset'])

// Auto-start countdown logic
const countdown = ref(5)
let countdownInterval: ReturnType<typeof setInterval> | null = null

const startCountdown = () => {
  countdown.value = 5
  if (countdownInterval) clearInterval(countdownInterval)
  
  countdownInterval = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearCountdown()
      emit('start')
    }
  }, 1000)
}

const clearCountdown = () => {
  if (countdownInterval) {
    clearInterval(countdownInterval)
    countdownInterval = null
  }
}

const startNow = () => {
  clearCountdown()
  emit('start')
}

onMounted(() => {
  if (!props.isRecording && !props.recordedBlob) {
    startCountdown()
  }
})

watch(() => [props.isRecording, props.recordedBlob], ([rec, blob]) => {
  if (!rec && !blob) {
    startCountdown()
  } else {
    clearCountdown()
  }
})

onUnmounted(() => {
  clearCountdown()
})
</script>
