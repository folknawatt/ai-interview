<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="modelValue" class="modal-overlay" @click="onOverlayClick">
        <div class="modal-container" :class="sizeClass" @click.stop>
          <!-- Header -->
          <div v-if="title || $slots.header" class="modal-header">
            <slot name="header">
              <h3 class="modal-title">{{ title }}</h3>
            </slot>
            <button
              v-if="closable"
              class="modal-close"
              @click="close"
              aria-label="Close modal"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Body -->
          <div class="modal-body">
            <slot />
          </div>

          <!-- Footer -->
          <div v-if="$slots.footer" class="modal-footer">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, watch, onMounted, onUnmounted } from 'vue'

interface Props {
  modelValue: boolean
  title?: string
  size?: 'sm' | 'md' | 'lg' | 'xl'
  closable?: boolean
  closeOnOverlay?: boolean
  closeOnEscape?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  closable: true,
  closeOnOverlay: true,
  closeOnEscape: true
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  close: []
}>()

const sizeClass = computed(() => {
  const sizes = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl'
  }
  return sizes[props.size]
})

const close = () => {
  emit('update:modelValue', false)
  emit('close')
}

const onOverlayClick = () => {
  if (props.closeOnOverlay) {
    close()
  }
}

const handleEscape = (event: KeyboardEvent) => {
  if (event.key === 'Escape' && props.closeOnEscape && props.modelValue) {
    close()
  }
}

// Lock body scroll when modal is open
watch(() => props.modelValue, (isOpen) => {
  if (isOpen) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

onMounted(() => {
  document.addEventListener('keydown', handleEscape)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape)
  document.body.style.overflow = ''
})
</script>

<style lang="postcss" scoped>
/* stylelint-disable-next-line */
.modal-overlay {
  @apply fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4;
}

.modal-container {
  @apply bg-white rounded-lg shadow-xl w-full max-h-[90vh] flex flex-col;
}

.modal-header {
  @apply flex items-center justify-between p-6 border-b border-slate-200;
}

.modal-title {
  @apply text-xl font-semibold text-slate-800;
}

.modal-close {
  @apply text-slate-500 hover:text-slate-800 transition-colors;
}

.modal-body {
  @apply p-6 overflow-y-auto flex-1;
}

.modal-footer {
  @apply p-6 border-t border-slate-200 flex gap-3 justify-end;
}

/* Transitions */
.modal-enter-active,
.modal-leave-active {
  @apply transition ease-out duration-300;
}

.modal-enter-from,
.modal-leave-to {
  @apply opacity-0;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  @apply transition-transform ease-out duration-300;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  @apply scale-95;
}
</style>
