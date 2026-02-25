<template>
  <div
    class="min-h-screen bg-interview-bg text-interview-text-primary flex flex-col items-center justify-center p-4 relative overflow-hidden"
  >
    <!-- Background gradient effects -->
    <div class="fixed inset-0 z-0 bg-interview-bg">
      <div class="absolute inset-0 bg-gradient-to-b from-black/80 via-interview-bg to-black"></div>
      <div class="absolute top-1/4 -left-32 w-96 h-96 bg-red-500/10 rounded-full blur-3xl"></div>
      <div
        class="absolute bottom-1/4 -right-32 w-96 h-96 bg-interview-primary/10 rounded-full blur-3xl"
      ></div>
    </div>

    <Recorder
      ref="recorderRef"
      :is-recording="isRecording"
      :is-submitting="isSubmitting"
      :recorded-blob="recordedBlob"
      :timer="timer"
      :format-time="formatTime"
      :error="error"
      @start="startRecording"
      @stop="stopRecording"
      @submit="submitRecording"
      @reset="resetRecording"
      class="relative z-10"
    />
  </div>
</template>

<script setup lang="ts">
import Recorder from '../components/interview/Recorder.vue'
import { useMediaRecorder } from '../composables/useMediaRecorder'

definePageMeta({
  layout: 'blank',
})

const {
  currentQuestion,
  selectedRole,
  currentQuestionIndex,
  uploadAnswer,
  setAnalysisResult,
  getQuestion,
  completeInterview,
} = useInterview()
const router = useRouter()

// Use the composable for recording logic
const {
  videoPreview,
  recordedBlob,
  isRecording,
  timer,
  error: recorderError,
  formatTime,
  startCamera,
  stopCamera,
  startRecording,
  stopRecording,
  resetRecording: resetRecorder,
} = useMediaRecorder()

const isSubmitting = ref(false)
const error = ref<string | null>(null)
const recorderRef = ref<any>(null)

// Sync recorder error to local error, but allow overwriting
watch(recorderError, val => {
  if (val) error.value = val
})

// Sync video ref when component is mounted, then start camera once
onMounted(() => {
  if (recorderRef.value?.videoRef) {
    videoPreview.value = recorderRef.value.videoRef
  }
  startCamera()
})

const resetRecording = () => {
  resetRecorder()
  error.value = null
}

const submitRecording = async () => {
  if (!recordedBlob.value || !currentQuestion.value) return

  isSubmitting.value = true
  error.value = null

  try {
    // Upload video and get evaluation from API
    const result = await uploadAnswer(recordedBlob.value, currentQuestion.value)

    // Set analysis result in state for result page
    setAnalysisResult(result)

    // Check if there are more questions (skip TTS to avoid playing audio before navigation)
    if (selectedRole.value) {
      const nextIndex = currentQuestionIndex.value + 1
      const nextQ = await getQuestion(selectedRole.value.id, nextIndex, true) // skipTts = true

      if (nextQ.status === 'continue') {
        // More questions available - go to next question
        router.push('/question')
      } else {
        // All questions completed - mark interview as complete
        try {
          await completeInterview()
        } catch (completionError) {
          console.error('Failed to complete interview:', completionError)
          // Proceed to result page anyway
        }
        router.push('/result')
      }
    } else {
      // Fallback - go to result page
      router.push('/result')
    }
  } catch (err: any) {
    error.value = err.message || 'Failed to submit recording'
    isSubmitting.value = false
  }
}

onUnmounted(() => {
  stopCamera()
})
</script>
