<template>
  <div
    class="min-h-screen bg-interview-bg text-interview-text-primary flex flex-col items-center justify-center p-4 relative overflow-hidden"
  >
    <!-- Background gradient effects -->
    <div class="absolute inset-0 bg-gradient-to-br from-interview-bg via-interview-bg-secondary to-interview-bg-gradient"></div>
    <div class="absolute top-1/4 -left-32 w-96 h-96 bg-interview-primary/10 rounded-full blur-3xl"></div>
    <div class="absolute bottom-1/4 -right-32 w-96 h-96 bg-interview-accent-sky/10 rounded-full blur-3xl"></div>

    <div
      class="relative w-full max-w-2xl bg-interview-surface backdrop-blur-xl p-8 rounded-2xl border border-interview-surface-border shadow-glass text-center animate-fade-in-up"
    >
      <div class="mb-6">
        <span
          class="bg-interview-primary/10 text-interview-primary text-xs font-medium px-3 py-1.5 rounded-full border border-interview-primary/30"
        >
          คำถามสัมภาษณ์
        </span>
      </div>

      <h2 v-if="currentQuestion" class="text-2xl md:text-3xl font-bold mb-8 leading-relaxed text-interview-text-primary">"{{ currentQuestion }}"</h2>
      <div v-else class="text-2xl md:text-3xl font-bold mb-8 text-interview-text-secondary">
        <div class="flex items-center justify-center gap-2">
          <span>กำลังโหลดคำถาม</span>
          <span class="animate-pulse">•••</span>
        </div>
      </div>

      <!-- Audio playback button -->
      <div v-if="currentAudioPath" class="mb-4">
        <button
          @click="playAudio"
          class="inline-flex items-center px-4 py-2.5 text-sm font-medium text-interview-text-secondary bg-interview-surface border border-interview-surface-border hover:border-interview-primary/50 hover:bg-interview-surface-hover rounded-xl focus:outline-none focus:ring-2 focus:ring-interview-primary transition-all duration-300"
          title="Play audio"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"></path>
          </svg>
          ฟังคำถามอีกครั้ง
        </button>
      </div>

      <div class="flex flex-col items-center justify-center space-y-4 py-6">
        <div class="text-interview-text-secondary text-sm">เวลาเตรียมตัว (Preparation Time)</div>
        <div class="text-7xl font-mono font-bold text-interview-primary animate-glow-pulse">{{ timeLeft }}s</div>
      </div>

      <div class="mt-8">
        <button
          @click="goToRecord"
          class="inline-flex items-center px-8 py-4 text-lg font-semibold text-interview-bg bg-interview-primary hover:bg-interview-primary-hover rounded-xl focus:outline-none focus:ring-2 focus:ring-interview-primary focus:ring-offset-2 focus:ring-offset-interview-bg transition-all duration-300 shadow-glow-amber hover:shadow-glow-amber-lg"
        >
          <svg
            class="w-6 h-6 mr-2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
            ></path>
          </svg>
          พร้อมแล้ว! เริ่มอัดวิดีโอเลย
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { selectedRole, currentQuestionIndex, currentQuestion, currentAudioPath, getQuestion, playAudio, completeInterview, sessionId } = useInterview()
const router = useRouter()

const timeLeft = ref(30)
let timer: ReturnType<typeof setInterval>

onMounted(async () => {
  // Check if role is selected
  if (!selectedRole.value) {
    router.push('/role-selection')
    return
  }

  // Fetch question from API
  try {
    const response = await getQuestion(selectedRole.value.id, currentQuestionIndex.value)

    if (response.status === 'continue' && response.question) {
      // currentQuestion is now automatically set by getQuestion in useInterview
      // Try to play audio automatically if available
      if (response.audio_path) {
        // Small delay to ensure UI is ready
        setTimeout(async () => {
          try {
            await playAudio()
          } catch (error) {
            // Autoplay blocked by browser - show notification
            console.log('Autoplay blocked. User needs to click play button.')
          }
        }, 100)
      }
    } else if (response.status === 'finished') {
      // All questions completed - mark interview as complete
      try {
        await completeInterview()
        console.log('Interview marked as complete')
      } catch (error) {
        console.error('Failed to complete interview:', error)
        // Still redirect to result page even if completion fails
      }
      router.push('/result')
      return
    }
  } catch (error) {
    console.error('Error fetching question:', error)
    currentQuestion.value = 'Error loading question. Please try again.'
  }

  // Start countdown timer
  timer = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
    } else {
      goToRecord()
    }
  }, 1000)
})

onUnmounted(() => {
  clearInterval(timer)
})

const goToRecord = () => {
  router.push('/record')
}
</script>
