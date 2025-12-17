<template>
  <div class="min-h-screen bg-minimal-bg flex flex-col">
    <!-- Minimal header with progress -->
    <header class="bg-minimal-card border-b border-minimal-border">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <div class="text-xl font-semibold text-minimal-text-primary">
            AI Interview
          </div>
          
          <!-- Progress indicator slot (can be overridden by pages) -->
          <div v-if="showProgress" class="flex items-center gap-2 text-sm text-minimal-text-secondary">
            <span>Question {{ currentQuestion }} of {{ totalQuestions }}</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Centered content area for interview flow -->
    <main class="flex-1 flex items-center justify-center p-4">
      <div class="w-full max-w-4xl">
        <slot />
      </div>
    </main>

    <!-- Minimal footer -->
    <footer class="py-4 text-center text-sm text-minimal-text-muted">
      <p>Stay focused. You're doing great!</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
/**
 * Candidate Interview Layout
 * Minimal distraction design focused on the interview experience
 * Centered content with optional progress indicator
 */

// Optional props for progress tracking
interface Props {
  showProgress?: boolean
  currentQuestion?: number
  totalQuestions?: number
}

withDefaults(defineProps<Props>(), {
  showProgress: false,
  currentQuestion: 1,
  totalQuestions: 1
})
</script>
