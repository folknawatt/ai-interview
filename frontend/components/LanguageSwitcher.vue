<template>
  <div class="relative inline-block text-left">
    <button
      @click="toggleDropdown"
      type="button"
      class="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-interview-text-secondary bg-interview-surface/50 backdrop-blur-sm border border-interview-surface-border rounded-lg hover:bg-interview-surface hover:border-interview-primary/30 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-interview-primary/50"
      aria-haspopup="true"
      :aria-expanded="isOpen"
    >
      <LanguageIcon class="w-5 h-5" />
      <span class="hidden sm:inline">{{ currentLocaleName }}</span>
      <ChevronDownIcon 
        class="w-4 h-4 transition-transform duration-200" 
        :class="{ 'rotate-180': isOpen }"
      />
    </button>

    <!-- Dropdown Menu -->
    <Transition
      enter-active-class="transition ease-out duration-100"
      enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100"
      leave-active-class="transition ease-in duration-75"
      leave-from-class="transform opacity-100 scale-100"
      leave-to-class="transform opacity-0 scale-95"
    >
      <div
        v-if="isOpen"
        class="absolute right-0 mt-2 w-48 origin-top-right rounded-lg bg-interview-surface backdrop-blur-xl border border-interview-surface-border shadow-glass z-50"
        role="menu"
        aria-orientation="vertical"
      >
        <div class="py-1">
          <button
            v-for="locale in availableLocales"
            :key="locale.code"
            @click="switchLanguage(locale.code)"
            class="group flex w-full items-center px-4 py-2 text-sm transition-colors duration-150"
            :class="[
              locale.code === currentLocale
                ? 'bg-interview-primary/10 text-interview-primary font-medium'
                : 'text-interview-text-secondary hover:bg-interview-surface-hover hover:text-interview-text-primary'
            ]"
            role="menuitem"
          >
            <CheckIcon 
              v-if="locale.code === currentLocale"
              class="w-4 h-4 mr-2"
            />
            <span :class="{ 'ml-6': locale.code !== currentLocale }">
              {{ locale.name }}
            </span>
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { LanguageIcon, ChevronDownIcon, CheckIcon } from '@heroicons/vue/24/outline'

interface Locale {
  code: string
  name: string
  file?: string
}

const { locale, locales } = useI18n()
const isOpen = ref(false)

const availableLocales = computed(() => locales.value as Locale[])
const currentLocale = computed(() => locale.value)
const currentLocaleName = computed(() => {
  const current = availableLocales.value.find((l: Locale) => l.code === currentLocale.value)
  return current?.name || 'Language'
})

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const switchLanguage = (code: string) => {
  locale.value = code as 'th' | 'en'
  isOpen.value = false
}

// Close dropdown when clicking outside
onMounted(() => {
  const handleClickOutside = (event: MouseEvent) => {
    const target = event.target as HTMLElement
    if (!target.closest('.relative')) {
      isOpen.value = false
    }
  }
  document.addEventListener('click', handleClickOutside)
  onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
  })
})
</script>
