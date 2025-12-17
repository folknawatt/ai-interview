<template>
  <div class="spinner-container" :class="sizeClass">
    <div class="spinner" :style="spinnerStyle"></div>
    <p v-if="message" class="spinner-message">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  size?: 'sm' | 'md' | 'lg'
  color?: string
  message?: string
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  color: '#334155' // minimal-focus color
})

const sizeClass = computed(() => {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  }
  return sizes[props.size]
})

const spinnerStyle = computed(() => ({
  borderColor: props.color,
  borderRightColor: 'transparent'
}))
</script>

<style scoped>
/* stylelint-disable-next-line */
.spinner-container {
  @apply flex flex-col items-center justify-center gap-3;
}

.spinner {
  @apply border-4 border-solid rounded-full animate-spin;
  width: inherit;
  height: inherit;
}

.spinner-message {
  @apply text-sm text-minimal-text-secondary text-center;
}
</style>
