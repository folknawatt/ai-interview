<template>
  <div
    class="min-h-screen bg-interview-bg text-interview-text-primary flex flex-col items-center justify-center p-4 relative overflow-hidden"
    @mousemove="handleMouseMove"
  >
    <!-- Premium Background Complexity -->
    <div class="fixed inset-0 z-0 bg-interview-bg">
      <!-- 1. Base Gradient -->
      <div class="absolute inset-0 bg-gradient-to-b from-black/80 via-interview-bg to-black"></div>
      
      <!-- 2. Noise Texture (The Human Touch) handled in layout now, but explicit here as well doesn't hurt -->
      <div class="absolute inset-0 opacity-[0.02]" :style="{ backgroundImage: 'url(\'data:image/svg+xml,%3Csvg viewBox=\'0 0 200 200\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noiseFilter\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.65\' numOctaves=\'3\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23noiseFilter)\'/%3E%3C/svg%3E\')' }"></div>

      <!-- 3. Dynamic Orbs (Positioned carefully) with Parallax -->
      <div 
        class="absolute top-[-10%] left-[-10%] w-[600px] h-[600px] bg-interview-primary/10 rounded-full blur-[120px] transition-transform duration-100 ease-out will-change-transform"
        :style="{ transform: `translate(${mouseParallax.x * 20}px, ${mouseParallax.y * 20}px)` }"
      ></div>
      <div 
        class="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-interview-primary/5 rounded-full blur-[100px] transition-transform duration-100 ease-out will-change-transform delay-75"
        :style="{ transform: `translate(${mouseParallax.x * -15}px, ${mouseParallax.y * -15}px)` }"
      ></div>
    </div>

    <!-- Login Card -->
    <div
      class="relative w-full max-w-md bg-interview-surface backdrop-blur-2xl p-10 rounded-3xl border border-white/5 shadow-glass animate-fade-in-up z-10"
      role="form"
      aria-labelledby="login-title"
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
          id="login-title"
          class="text-4xl font-black tracking-tight bg-gradient-to-r from-interview-text-primary via-white to-interview-text-secondary bg-clip-text text-transparent drop-shadow-2xl mb-2"
        >
          {{ activeTab === 'candidate' ? 'ยินดีต้อนรับ' : 'HR Portal' }}
        </h1>
        <p class="text-interview-text-secondary text-sm font-medium tracking-wide">
          {{ activeTab === 'candidate' ? 'ระบบสัมภาษณ์งานอัจฉริยะ AI Powered' : 'เข้าสู่ระบบสำหรับเจ้าหน้าที่บริหาร' }}
        </p>
      </div>

      <!-- Tab Switcher -->
      <div class="flex p-1 bg-interview-bg-secondary/50 rounded-xl mb-6 backdrop-blur-sm border border-interview-surface-border">
        <button
          @click="activeTab = 'candidate'"
          class="flex-1 py-2.5 text-sm font-medium rounded-lg transition-all duration-300"
          :class="activeTab === 'candidate' ? 'bg-interview-primary text-interview-bg shadow-glow-amber' : 'text-interview-text-secondary hover:text-interview-text-primary hover:bg-interview-surface-hover'"
        >
          ผู้สมัคร (Candidate)
        </button>
        <button
          @click="activeTab = 'hr'"
          class="flex-1 py-2.5 text-sm font-medium rounded-lg transition-all duration-300"
          :class="activeTab === 'hr' ? 'bg-interview-primary text-interview-bg shadow-glow-amber' : 'text-interview-text-secondary hover:text-interview-text-primary hover:bg-interview-surface-hover'"
        >
          เจ้าหน้าที่ (HR)
        </button>
      </div>

      <!-- Candidate Login Form -->
      <form v-if="activeTab === 'candidate'" @submit.prevent="handleSubmitCandidate" class="space-y-6" novalidate>
        <!-- Name Field -->
        <div>
          <label class="block text-left text-sm font-medium mb-2 text-interview-text-secondary">
            ชื่อ-นามสกุล ของคุณ <span class="text-interview-primary">*</span>
          </label>
          <div class="relative group">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <UserIcon class="h-5 w-5 text-interview-text-muted group-focus-within:text-interview-primary transition-colors" />
            </div>
            <input
              id="name-input"
              v-model="name"
              type="text"
              placeholder="กรอกชื่อของคุณ..."
              autofocus
              class="w-full pl-11 pr-4 py-3.5 bg-interview-bg-secondary/50 border border-interview-surface-border rounded-xl focus:outline-none focus:ring-2 focus:ring-interview-primary/50 focus:border-interview-primary/50 text-interview-text-primary placeholder-interview-text-muted transition-all backdrop-blur-sm"
              :class="showErrors && !name.trim() ? 'border-interview-warning/50 focus:ring-interview-warning/50' : ''"
              @blur="touchedFields.name = true"
            />
          </div>
          <Transition
            enter-active-class="transition-all duration-300 ease-out"
            enter-from-class="opacity-0 -translate-y-2"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition-all duration-200 ease-in"
            leave-from-class="opacity-100 translate-y-0"
            leave-to-class="opacity-0 -translate-y-2"
          >
            <p v-if="showErrors && !name.trim()" class="mt-2 text-sm text-interview-warning flex items-center gap-1.5 font-medium">
              <ExclamationTriangleIcon class="w-4 h-4" /> กรุณากรอกชื่อ-นามสกุล
            </p>
          </Transition>
        </div>

        <!-- Email Field -->
        <div>
          <label class="block text-left text-sm font-medium mb-2 text-interview-text-secondary">
            อีเมล (Email) <span class="text-interview-primary">*</span>
          </label>
          <div class="relative group">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <EnvelopeIcon class="h-5 w-5 text-interview-text-muted group-focus-within:text-interview-primary transition-colors" />
            </div>
            <input
              id="email-input"
              v-model="email"
              type="email"
              placeholder="example@email.com"
              class="w-full pl-11 pr-4 py-3.5 bg-interview-bg-secondary/50 border border-interview-surface-border rounded-xl focus:outline-none focus:ring-2 focus:ring-interview-primary/50 focus:border-interview-primary/50 text-interview-text-primary placeholder-interview-text-muted transition-all backdrop-blur-sm"
              :class="showErrors && !isValidEmail ? 'border-interview-warning/50 focus:ring-interview-warning/50' : ''"
              @blur="touchedFields.email = true"
            />
          </div>
          <Transition
            enter-active-class="transition-all duration-300 ease-out"
            enter-from-class="opacity-0 -translate-y-2"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition-all duration-200 ease-in"
            leave-from-class="opacity-100 translate-y-0"
            leave-to-class="opacity-0 -translate-y-2"
          >
            <div v-if="showErrors">
              <p v-if="!email.trim()" class="mt-2 text-sm text-interview-warning flex items-center gap-1.5 font-medium">
                <ExclamationTriangleIcon class="w-4 h-4" /> กรุณากรอกอีเมล
              </p>
              <p v-else-if="!isValidEmail" class="mt-2 text-sm text-interview-warning flex items-center gap-1.5 font-medium">
                <ExclamationTriangleIcon class="w-4 h-4" /> รูปแบบอีเมลไม่ถูกต้อง
              </p>
            </div>
          </Transition>
        </div>

        <!-- Privacy Consent -->
        <div class="flex items-start gap-3 p-4 bg-black/20 rounded-xl border border-interview-surface-border">
          <div class="flex items-center h-5 mt-0.5">
            <input
              id="privacy-consent"
              v-model="privacyConsent"
              type="checkbox"
              required
              class="w-5 h-5 text-interview-primary border-interview-surface-border rounded focus:ring-interview-primary bg-interview-surface cursor-pointer ring-offset-0"
            />
          </div>
          <div class="text-sm">
            <label for="privacy-consent" class="font-medium text-interview-text-primary cursor-pointer select-none">
              ฉันได้อ่านและยอมรับ
              <a href="/privacy" target="_blank" class="text-interview-primary hover:text-interview-primary-hover underline decoration-dashed underline-offset-4">
                นโยบายความเป็นส่วนตัว
              </a>
              <div class="text-xs text-interview-text-secondary mt-1">
                (ยินยอมให้บันทึกภาพและเสียงวิดีโอเพื่อการประเมินผลโดย AI)
              </div>
            </label>
          </div>
        </div>

        <button
          type="submit"
          :disabled="!isFormValid"
          class="w-full px-6 py-4 text-lg font-bold text-interview-bg bg-gradient-to-r from-interview-primary to-interview-primary-light rounded-xl hover:from-interview-primary-hover hover:to-interview-primary shadow-glow-amber hover:shadow-glow-amber-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed transform hover:-translate-y-0.5"
        >
          เริ่มการสัมภาษณ์
        </button>
      </form>


      <!-- HR Login Form -->
      <form v-else @submit.prevent="handleSubmitHR" class="space-y-6">
        <div>
          <label class="block text-left text-sm font-medium mb-2 text-interview-text-secondary">Username</label>
          <div class="relative group">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <UserIcon class="h-5 w-5 text-interview-text-muted group-focus-within:text-interview-primary transition-colors" />
            </div>
            <input
              v-model="hrUsername"
              type="text"
              placeholder="admin"
              class="w-full pl-11 pr-4 py-3.5 bg-interview-bg-secondary/50 border border-interview-surface-border rounded-xl focus:outline-none focus:ring-2 focus:ring-interview-primary/50 focus:border-interview-primary/50 text-interview-text-primary placeholder-interview-text-muted transition-all backdrop-blur-sm"
            />
          </div>
        </div>
        <div>
          <label class="block text-left text-sm font-medium mb-2 text-interview-text-secondary">Password</label>
          <div class="relative group">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <LockClosedIcon class="h-5 w-5 text-interview-text-muted group-focus-within:text-interview-primary transition-colors" />
            </div>
            <input
              v-model="hrPassword"
              type="password"
              placeholder="password"
              class="w-full pl-11 pr-4 py-3.5 bg-interview-bg-secondary/50 border border-interview-surface-border rounded-xl focus:outline-none focus:ring-2 focus:ring-interview-primary/50 focus:border-interview-primary/50 text-interview-text-primary placeholder-interview-text-muted transition-all backdrop-blur-sm"
            />
          </div>
        </div>

        <div v-if="hrError" class="text-sm text-interview-warning bg-interview-warning/10 p-3 rounded-lg border border-interview-warning/30 flex items-center gap-2">
          <ExclamationTriangleIcon class="w-5 h-5 flex-shrink-0" />
          {{ hrError }}
        </div>

        <button
          type="submit"
          class="w-full px-6 py-4 text-lg font-bold text-interview-bg bg-gradient-to-r from-interview-primary to-interview-primary-light rounded-xl hover:from-interview-primary-hover hover:to-interview-primary shadow-glow-amber hover:shadow-glow-amber-lg transition-all duration-300 transform hover:-translate-y-0.5"
        >
          เข้าสู่ระบบ (Login)
        </button>
        
        <div class="text-center text-xs text-interview-text-muted mt-4">
          Default: admin / password
        </div>
      </form>
    </div>

    <!-- Footer text -->
    <p class="mt-8 text-interview-text-muted text-sm animate-fade-in">
      Powered by AI Interview Platform
    </p>
  </div>
</template>

<script setup lang="ts">
import { HandRaisedIcon, UserGroupIcon, UserIcon, EnvelopeIcon, LockClosedIcon, ExclamationTriangleIcon } from '@heroicons/vue/24/solid'
import { useAuth } from '@/store/auth'
import { UserRole } from '@/types'

definePageMeta({
  layout: 'blank'
})

// Stores
const { setCandidateInfo } = useInterview()
const authStore = useAuth()
const router = useRouter()

// UI State
const activeTab = ref<'candidate' | 'hr'>('candidate')

// Candidate State
const name = ref('')
const email = ref('')
const privacyConsent = ref(false)
const touchedFields = reactive({ name: false, email: false })
const formSubmitted = ref(false)

// HR State
const hrUsername = ref('')
const hrPassword = ref('')
const hrError = ref('')
const hrLoading = ref(false)

// Mouse Parallax Logic
const mouseParallax = reactive({ x: 0, y: 0 })
let rafId: number | null = null

const handleMouseMove = (event: MouseEvent) => {
  if (rafId) return

  rafId = requestAnimationFrame(() => {
    const { clientX, clientY } = event
    const { innerWidth, innerHeight } = window
    // Normalize coordinates from -1 to 1
    mouseParallax.x = (clientX / innerWidth) * 2 - 1
    mouseParallax.y = (clientY / innerHeight) * 2 - 1
    rafId = null
  })
}

onUnmounted(() => {
  if (rafId) cancelAnimationFrame(rafId)
})

// Email validation regex
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

// Computed properties for validation
const isValidEmail = computed(() => emailRegex.test(email.value.trim()))
const isFormValid = computed(() => name.value.trim() && isValidEmail.value && privacyConsent.value)
const showErrors = computed(() => formSubmitted.value || touchedFields.name || touchedFields.email)

const handleSubmitCandidate = () => {
  formSubmitted.value = true

  if (isFormValid.value) {
    setCandidateInfo(name.value, email.value)
    router.push('/role-selection')
  }
}

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
    
    const response = await $fetch<{
      access_token: string
      token_type: string
      user: {
        id: number
        username: string
        email: string
        full_name: string
        role: string
        is_active: boolean
      }
    }>(`${apiBase}/auth/login`, {
      method: 'POST',
      body: formData,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    
    // Map backend user to frontend User type
    const user = {
      id: String(response.user.id),
      name: response.user.full_name,
      email: response.user.email,
      role: response.user.role === 'admin' ? UserRole.ADMIN : UserRole.HR,
      createdAt: new Date().toISOString()
    }
    
    authStore.signInAuth(response.access_token, response.access_token, user)
    
    // Redirect to HR Dashboard
    const redirectPath = (router.currentRoute.value.query.redirect as string) || '/hr/dashboard'
    router.push(redirectPath)
  } catch (error: any) {
    console.error('Login error:', error)
    if (error.data?.detail) {
      hrError.value = error.data.detail
    } else {
      hrError.value = 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
    }
  } finally {
    hrLoading.value = false
  }
}
</script>
