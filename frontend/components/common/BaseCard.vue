<template>
  <div :class="cardClasses" @click="handleClick">
    <div v-if="title || $slots.header" class="card-header">
      <slot name="header">
        <h3 class="card-title">{{ title }}</h3>
      </slot>
    </div>
    
    <div class="card-body" :class="bodyPaddingClass">
      <slot />
    </div>
    
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  title?: string
  padding?: 'none' | 'sm' | 'md' | 'lg'
  hoverable?: boolean
  clickable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  padding: 'md',
  hoverable: false,
  clickable: false
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const cardClasses = computed(() => {
  const base = 'bg-minimal-card border border-minimal-border rounded-lg'
  const hover = props.hoverable ? 'hover:shadow-md transition-shadow' : ''
  const cursor = props.clickable ? 'cursor-pointer' : ''
  return `${base} ${hover} ${cursor}`
})

const bodyPaddingClass = computed(() => {
  const paddings = {
    none: 'p-0',
    sm: 'p-3',
    md: 'p-6',
    lg: 'p-8'
  }
  return paddings[props.padding]
})

const handleClick = (event: MouseEvent) => {
  if (props.clickable) {
    emit('click', event)
  }
}
</script>

<style scoped>
.card-header {
  @apply px-6 py-4 border-b border-minimal-border;
}

.card-title {
  @apply text-lg font-semibold text-minimal-text-primary;
}

.card-body {
  @apply text-minimal-text-secondary;
}

.card-footer {
  @apply px-6 py-4 border-t border-minimal-border;
}
</style>
