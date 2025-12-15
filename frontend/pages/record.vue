<template>
  <div
    class="min-h-screen bg-minimal-bg text-minimal-text-primary flex flex-col items-center justify-center p-4"
  >
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
    />
  </div>
</template>

<script setup lang="ts">
import Recorder from '@/components/Recorder.vue'
import { useMediaRecorder } from '@/composables/useMediaRecorder'

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
    resetRecording: resetRecorder
} = useMediaRecorder()

const isSubmitting = ref(false)
const error = ref<string | null>(null)
const recorderRef = ref<any>(null)

// Sync recorder error to local error, but allow overwriting
watch(recorderError, (val) => {
    if (val) error.value = val
})

// Sync video ref when component is mounted
onMounted(() => {
    startCamera().then(() => {
         if (recorderRef.value && recorderRef.value.videoRef) {
             videoPreview.value = recorderRef.value.videoRef
             // We need to set srcObject again because the element was just mounted
             startCamera() 
         }
    })
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

    // Check if there are more questions
    if (selectedRole.value) {
      const nextIndex = currentQuestionIndex.value + 1
      const nextQ = await getQuestion(selectedRole.value.id, nextIndex)

      if (nextQ.status === 'continue') {
        // More questions available - go to next question
        router.push('/question')
      } else {
        // All questions completed - mark interview as complete
        try {
          await completeInterview()
        } catch (error) {
          console.error('Failed to complete interview:', error)
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
