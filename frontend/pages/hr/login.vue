<template>
  <div
    class="min-h-screen bg-interview-bg text-interview-text-primary flex flex-col items-center justify-center p-4 relative overflow-hidden"
  >
    <!-- Background Elements -->
    <div class="fixed inset-0 z-0 bg-interview-bg">
      <div class="absolute inset-0 bg-gradient-to-b from-black/80 via-interview-bg to-black"></div>
      <div
        class="absolute inset-0 opacity-[0.02]"
        :style="{
          backgroundImage:
            'url(\'data:image/svg+xml,%3Csvg viewBox=\'0 0 200 200\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noiseFilter\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.65\' numOctaves=\'3\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23noiseFilter)\'/%3E%3C/svg%3E\')',
        }"
      ></div>
    </div>

    <!-- Login Card -->
    <div
      class="relative w-full max-w-md bg-interview-surface backdrop-blur-2xl p-10 rounded-3xl border border-white/5 shadow-glass animate-fade-in-up z-10"
    >
      <!-- Header Section -->
      <div class="text-center mb-10">
        <div class="flex justify-center mb-6">
          <img
            src="/logo_chono.png"
            alt="ChonoHire Logo"
            class="h-24 w-auto object-contain drop-shadow-xl transition-transform duration-500 hover:scale-105"
          />
        </div>
        <h1
          class="text-4xl font-black tracking-tight bg-gradient-to-r from-interview-text-primary via-white to-interview-text-secondary bg-clip-text text-transparent drop-shadow-2xl mb-2"
        >
          HR Portal
        </h1>
        <p class="text-interview-text-secondary text-sm font-medium tracking-wide">
          {{ $t('hr.login.title') }}
        </p>
      </div>

      <!-- HR Login Form -->
      <form @submit.prevent="handleSubmitHR" class="space-y-6">
        <div>
          <label class="block text-left text-sm font-medium mb-2 text-interview-text-secondary"
            >Username</label
          >
          <div class="relative group">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <UserIcon
                class="h-5 w-5 text-interview-text-muted group-focus-within:text-interview-primary transition-colors"
              />
            </div>
            <input
              v-model="hrUsername"
              type="text"
              placeholder="admin"
              class="w-full pl-11 pr-4 py-3.5 bg-interview-bg-secondary/50 border border-interview-surface-border rounded-xl focus:outline-none focus:ring-2 focus:ring-interview-primary/50 focus:border-interview-primary/50 text-interview-text-primary placeholder-interview-text-muted transition-all backdrop-blur-sm"
              autofocus
            />
          </div>
        </div>
        <div>
          <label class="block text-left text-sm font-medium mb-2 text-interview-text-secondary"
            >Password</label
          >
          <div class="relative group">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <LockClosedIcon
                class="h-5 w-5 text-interview-text-muted group-focus-within:text-interview-primary transition-colors"
              />
            </div>
            <input
              v-model="hrPassword"
              type="password"
              placeholder="password"
              class="w-full pl-11 pr-4 py-3.5 bg-interview-bg-secondary/50 border border-interview-surface-border rounded-xl focus:outline-none focus:ring-2 focus:ring-interview-primary/50 focus:border-interview-primary/50 text-interview-text-primary placeholder-interview-text-muted transition-all backdrop-blur-sm"
            />
          </div>
        </div>

        <div
          v-if="hrError"
          class="text-sm text-interview-warning bg-interview-warning/10 p-3 rounded-lg border border-interview-warning/30 flex items-center gap-2"
        >
          <ExclamationTriangleIcon class="w-5 h-5 flex-shrink-0" />
          {{ hrError }}
        </div>

        <button
          type="submit"
          :disabled="hrLoading"
          class="w-full px-6 py-4 text-lg font-bold text-interview-bg bg-gradient-to-r from-interview-primary to-interview-primary-light rounded-xl hover:from-interview-primary-hover hover:to-interview-primary shadow-glow-amber hover:shadow-glow-amber-lg transition-all duration-300 transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="hrLoading">{{ $t('hr.login.loggingIn') }}</span>
          <span v-else>{{ $t('hr.login.loginButton') }}</span>
        </button>

        <div class="text-center text-xs text-interview-text-muted mt-4">Default: admin / admin</div>
      </form>
    </div>

    <!-- Footer text -->
    <p class="mt-8 text-interview-text-muted text-sm animate-fade-in">
      Powered by AI Interview Platform
    </p>
  </div>
</template>

<script setup lang="ts">
import { UserIcon, LockClosedIcon, ExclamationTriangleIcon } from '@heroicons/vue/24/solid'
import { useAuth } from '@/store/auth'

definePageMeta({
  layout: 'blank',
})

const authStore = useAuth()
const router = useRouter()

// HR State
const hrUsername = ref('')
const hrPassword = ref('')
const hrError = ref('')
const hrLoading = ref(false)

const handleSubmitHR = async () => {
  hrError.value = ''
  hrLoading.value = true

  try {
    // Create form data for OAuth2 password flow
    const formData = new URLSearchParams()
    formData.append('username', hrUsername.value)
    formData.append('password', hrPassword.value)

    const config = useRuntimeConfig()
    const apiBase = config.public.apiBaseUrl || 'http://localhost:8000'

    await $fetch(`${apiBase}/auth/login`, {
      method: 'POST',
      body: formData,
      credentials: 'include', // Required for receiving Set-Cookie
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })

    // Cookie is set automatically by backend
    // Fetch user profile to update store state
    await authStore.fetchUser()

    // Redirect to HR Dashboard
    const redirectPath = (router.currentRoute.value.query.redirect as string) || '/hr/dashboard'
    await navigateTo(redirectPath, { replace: true })
  } catch (error: any) {
    console.error('Login error:', error)
    if (error.data?.detail) {
      hrError.value = error.data.detail
    } else {
      hrError.value = $t('hr.login.errorInvalidCredentials')
    }
  } finally {
    hrLoading.value = false
  }
}
</script>
