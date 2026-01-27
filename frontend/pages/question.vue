<template>
  <div
    class="min-h-screen bg-interview-bg text-interview-text-primary flex flex-col items-center justify-center p-4 relative overflow-hidden"
  >
    <!-- Background gradient effects -->
    <div class="fixed inset-0 z-0 bg-interview-bg">
      <div class="absolute inset-0 bg-gradient-to-b from-black/80 via-interview-bg to-black"></div>
      <div
        class="absolute top-1/4 -left-32 w-96 h-96 bg-interview-primary/10 rounded-full blur-3xl"
      ></div>
      <div
        class="absolute bottom-1/4 -right-32 w-96 h-96 bg-interview-accent-sky/10 rounded-full blur-3xl"
      ></div>
    </div>

    <div
      class="relative z-10 w-full max-w-2xl bg-interview-surface backdrop-blur-xl p-8 rounded-2xl border border-interview-surface-border shadow-glass text-center animate-fade-in-up"
    >
      <!-- Progress Indicator -->
      <div class="mb-6 flex flex-col items-center gap-3">
        <span
          class="bg-interview-primary/10 text-interview-primary text-xs font-medium px-3 py-1.5 rounded-full border border-interview-primary/30"
        >
          คำถามที่ {{ currentQuestionIndex + 1 }} / {{ totalQuestions }}
        </span>
        <!-- Progress Bar -->
        <div class="w-full max-w-xs h-2 bg-interview-surface-border rounded-full overflow-hidden">
          <div
            class="h-full bg-interview-primary transition-all duration-500 ease-out"
            :style="{ width: `${((currentQuestionIndex + 1) / totalQuestions) * 100}%` }"
            role="progressbar"
            :aria-valuenow="currentQuestionIndex + 1"
            :aria-valuemin="1"
            :aria-valuemax="totalQuestions"
          ></div>
        </div>
      </div>

      <h2
        v-if="currentQuestion"
        class="text-2xl md:text-3xl font-bold mb-8 leading-relaxed text-interview-text-primary"
      >
        "{{ currentQuestion }}"
      </h2>
      <div v-else class="text-2xl md:text-3xl font-bold mb-8 text-interview-text-secondary">
        <div class="flex items-center justify-center gap-2">
          <span>กำลังโหลดคำถาม</span>
          <span class="animate-pulse">•••</span>
        </div>
      </div>

      <!-- Audio notification when autoplay blocked -->
      <div 
        v-if="showAudioNotification && currentAudioPath" 
        class="mb-4 p-3 bg-interview-primary/20 border border-interview-primary/50 rounded-xl animate-fade-in-up"
      >
        <p class="text-interview-primary text-sm font-medium flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          กดปุ่มด้านล่างเพื่อฟังคำถาม
        </p>
      </div>

      <!-- Audio playback button -->
      <div v-if="currentAudioPath" class="mb-4">
        <button
          @click="handlePlayAudio"
          class="inline-flex items-center px-5 py-3 text-sm font-semibold rounded-xl transition-all duration-300 group"
          :class="showAudioNotification 
            ? 'text-interview-bg bg-interview-primary hover:bg-interview-primary-hover shadow-glow-amber animate-pulse' 
            : 'text-interview-text-secondary bg-interview-surface border border-interview-surface-border hover:border-interview-primary/50 hover:bg-interview-surface-hover'"
          aria-label="ฟังคำถาม"
        >
          <SpeakerWaveIcon 
            class="w-5 h-5 mr-2 transition-transform duration-300 group-hover:scale-110" 
            :class="{ 'animate-pulse': showAudioNotification }" 
          />
          {{ showAudioNotification ? '🔊 กดเพื่อฟังคำถาม' : 'ฟังคำถามอีกครั้ง' }}
        </button>
      </div>

      <div class="flex flex-col items-center justify-center space-y-4 py-6">
        <div class="text-interview-text-secondary text-sm">เวลาเตรียมตัว (Preparation Time)</div>
        <div
          class="text-7xl font-mono font-bold transition-colors duration-300"
          :class="
            timeLeft <= 5
              ? 'text-interview-warning animate-pulse'
              : 'text-interview-primary animate-glow-pulse'
          "
          role="timer"
          :aria-label="`เหลือเวลา ${timeLeft} วินาที`"
        >
          {{ timeLeft }}s
        </div>
        <!-- Warning message when time is running low -->
        <div
          v-if="timeLeft <= 5 && timeLeft > 0"
          class="text-interview-warning text-sm font-medium animate-pulse"
        >
          ⚠️ เวลาใกล้หมด! เตรียมตัวให้พร้อม
        </div>
      </div>

      <div class="mt-8">
        <button
          @click="goToRecord"
          class="inline-flex items-center px-8 py-4 text-lg font-semibold text-interview-bg bg-interview-primary hover:bg-interview-primary-hover rounded-xl focus:outline-none focus:ring-2 focus:ring-interview-primary focus:ring-offset-2 focus:ring-offset-interview-bg transition-all duration-300 shadow-glow-amber hover:shadow-glow-amber-lg group transform hover:-translate-y-0.5"
          aria-label="เริ่มอัดวิดีโอตอบคำถาม"
        >
          <VideoCameraIcon class="w-6 h-6 mr-2 transition-transform duration-300 group-hover:scale-110" />
          พร้อมแล้ว! เริ่มอัดวิดีโอเลย
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { SpeakerWaveIcon, VideoCameraIcon } from '@heroicons/vue/24/solid'

definePageMeta({
  layout: 'blank'
})

const {
  selectedRole,
  currentQuestionIndex,
  currentQuestion,
  currentAudioPath,
  getQuestion,
  playAudio,
  stopAudio,
  completeInterview,
  sessionId,
} = useInterview()
const router = useRouter()

const timeLeft = ref(30)
const totalQuestions = ref(5) // Default value, will be updated from API response
const showAudioNotification = ref(false) // Show notification when autoplay blocked
let timer: ReturnType<typeof setInterval>

// Handle audio play with notification dismissal
const handlePlayAudio = async () => {
  try {
    await playAudio()
    showAudioNotification.value = false
  } catch (error) {
    console.error('Error playing audio:', error)
  }
}

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
      // Update total questions from API response
      if (response.total) {
        totalQuestions.value = response.total
      }
      // currentQuestion is now automatically set by getQuestion in useInterview
      // Try to play audio automatically if available
      if (response.audio_path) {
        // Small delay to ensure UI is ready
        setTimeout(async () => {
          try {
            await playAudio()
            showAudioNotification.value = false
          } catch (error) {
            // Autoplay blocked by browser - show notification
            console.log('Autoplay blocked. User needs to click play button.')
            showAudioNotification.value = true
          }
        }, 300)
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
  stopAudio()
})

const goToRecord = () => {
  stopAudio()
  router.push('/record')
}
</script>
