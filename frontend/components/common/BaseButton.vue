<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="buttonClasses"
    @click="handleClick"
  >
    <span v-if="loading" class="loading-spinner"></span>
    <slot v-else />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  disabled?: boolean
  type?: 'button' | 'submit' | 'reset'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  loading: false,
  disabled: false,
  type: 'button'
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const buttonClasses = computed(() => {
  const base = 'inline-flex items-center justify-center font-medium rounded-lg transition-all focus:outline-none focus:ring-2 focus:ring-offset-2'
  
  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  }
  
  const variants = {
    primary: 'bg-minimal-focus text-white hover:bg-opacity-90 focus:ring-minimal-focus disabled:bg-minimal-border disabled:text-minimal-text-muted',
    secondary: 'bg-minimal-border text-minimal-text-primary hover:bg-minimal-text-muted hover:bg-opacity-10 focus:ring-minimal-border',
    danger: 'bg-minimal-warning text-white hover:bg-opacity-90 focus:ring-minimal-warning disabled:bg-minimal-border disabled:text-minimal-text-muted',
    ghost: 'bg-transparent text-minimal-text-primary hover:bg-minimal-border focus:ring-minimal-border'
  }
  
  const disabledClass = props.disabled || props.loading ? 'cursor-not-allowed opacity-60' : 'cursor-pointer'
  
  return `${base} ${sizes[props.size]} ${variants[props.variant]} ${disabledClass}`
})

const handleClick = (event: MouseEvent) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

<style scoped>
.loading-spinner {
  display: inline-block;
  width: 1em;
  height: 1em;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
