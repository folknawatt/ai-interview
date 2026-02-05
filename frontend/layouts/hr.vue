<template>
  <div class="min-h-screen bg-interview-bg flex relative">
    <!-- 2026 Trend: Cinematic Grain Overlay -->
    <!-- 2026 Trend: Cinematic Grain Overlay - Optimized -->
    <div class="fixed inset-0 z-50 pointer-events-none opacity-[0.02]" :style="{ backgroundImage: 'url(\'data:image/svg+xml,%3Csvg viewBox=\'0 0 200 200\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noiseFilter\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.8\' numOctaves=\'1\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23noiseFilter)\'/%3E%3C/svg%3E\')' }"></div>
    
    <!-- 2026 Trend: Vignette Focus -->
    <div class="fixed inset-0 z-40 pointer-events-none bg-radial-vignette opacity-30"></div>

    <!-- Base Background (Fixed) -->
    <div class="fixed inset-0 z-0 bg-interview-bg">
      <div class="absolute inset-0 bg-gradient-to-b from-black/80 via-interview-bg to-black"></div>
    </div>

    <!-- Sidebar Navigation (Desktop) -->
    <aside class="hidden md:block w-64 bg-interview-bg-secondary/80 backdrop-blur-xl border-r border-interview-surface-border flex-shrink-0 z-50">
      <div class="p-6">
      <div class="mb-10 flex items-center justify-center">
        <img 
          src="/logo_chono.png" 
          alt="ChonoHire Logo" 
          class="w-full h-auto object-contain drop-shadow-lg max-w-[160px]"
        />
      </div>
        
        <nav class="space-y-2">
          <NuxtLink
            to="/hr/dashboard"
            class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 group"
            :class="isActiveRoute('/hr/dashboard') 
              ? 'bg-interview-primary text-interview-bg shadow-glow-amber' 
              : 'text-interview-text-secondary hover:bg-interview-surface hover:text-interview-text-primary'"
          >
            <HomeIcon class="w-5 h-5 transition-transform group-hover:scale-110" />
            Dashboard
          </NuxtLink>
          
          <NuxtLink
            to="/hr/roles"
            class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 group"
            :class="isActiveRoute('/hr/roles') 
              ? 'bg-interview-primary text-interview-bg shadow-glow-amber' 
              : 'text-interview-text-secondary hover:bg-interview-surface hover:text-interview-text-primary'"
          >
            <UserGroupIcon class="w-5 h-5 transition-transform group-hover:scale-110" />
            Roles & Questions
          </NuxtLink>
          
          <NuxtLink
            to="/hr/generate"
            class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 group"
            :class="isActiveRoute('/hr/generate') 
              ? 'bg-interview-primary text-interview-bg shadow-glow-amber' 
              : 'text-interview-text-secondary hover:bg-interview-surface hover:text-interview-text-primary'"
          >
            <CpuChipIcon class="w-5 h-5 transition-transform group-hover:scale-110" />
            Generate Questions
          </NuxtLink>
          
          <NuxtLink
            to="/hr/reports"
            class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 group"
            :class="isActiveRoute('/hr/reports') 
              ? 'bg-interview-primary text-interview-bg shadow-glow-amber' 
              : 'text-interview-text-secondary hover:bg-interview-surface hover:text-interview-text-primary'"
          >
            <ChartBarSquareIcon class="w-5 h-5 transition-transform group-hover:scale-110" />
            Reports
          </NuxtLink>
        </nav>
      </div>
    </aside>

    <!-- Bottom Navigation (Mobile) -->
    <nav class="md:hidden fixed bottom-0 inset-x-0 z-50 bg-interview-bg-secondary/90 backdrop-blur-xl border-t border-interview-surface-border pb-safe">
      <div class="flex justify-around items-center p-2">
        <NuxtLink
          to="/hr/dashboard"
          class="flex flex-col items-center gap-1 p-2 rounded-xl transition-all duration-300"
          :class="isActiveRoute('/hr/dashboard') ? 'text-interview-primary' : 'text-interview-text-secondary'"
        >
          <HomeIcon class="w-6 h-6" />
          <span class="text-[10px] font-medium">Home</span>
        </NuxtLink>
        
        <NuxtLink
          to="/hr/roles"
          class="flex flex-col items-center gap-1 p-2 rounded-xl transition-all duration-300"
          :class="isActiveRoute('/hr/roles') ? 'text-interview-primary' : 'text-interview-text-secondary'"
        >
          <UserGroupIcon class="w-6 h-6" />
          <span class="text-[10px] font-medium">Roles</span>
        </NuxtLink>
        
        <NuxtLink
          to="/hr/generate"
          class="flex flex-col items-center gap-1 p-2 rounded-xl transition-all duration-300"
          :class="isActiveRoute('/hr/generate') ? 'text-interview-primary' : 'text-interview-text-secondary'"
        >
          <CpuChipIcon class="w-6 h-6" />
          <span class="text-[10px] font-medium">Gen AI</span>
        </NuxtLink>
        
        <NuxtLink
          to="/hr/reports"
          class="flex flex-col items-center gap-1 p-2 rounded-xl transition-all duration-300"
          :class="isActiveRoute('/hr/reports') ? 'text-interview-primary' : 'text-interview-text-secondary'"
        >
          <ChartBarSquareIcon class="w-6 h-6" />
          <span class="text-[10px] font-medium">Reports</span>
        </NuxtLink>
      </div>
    </nav>

    <!-- Main content area -->
    <div class="flex-1 flex flex-col">
      <!-- Top header -->
      <header class="bg-interview-surface backdrop-blur-xl border-b border-interview-surface-border px-8 py-4">
        <div class="flex items-center justify-between">
          <!-- Mobile Logo -->
          <div class="h-8 md:hidden flex items-center">
            <img 
              src="/logo_chono.png" 
              alt="ChonoHire Logo" 
              class="h-full w-auto object-contain"
            />
          </div>
          
          <!-- Desktop: Empty space or subtle breadcrumb placeholder -->
          <div class="hidden md:block"></div>
          
          <!-- User Info & Logout -->
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-full bg-interview-primary/20 border border-interview-primary/30 flex items-center justify-center">
                <span class="text-interview-primary text-sm font-bold">A</span>
              </div>
              <span class="text-interview-text-secondary text-sm hidden sm:inline">
                HR Admin
              </span>
            </div>
            <button
              @click="handleLogout"
              class="p-2 rounded-lg text-interview-text-secondary hover:text-red-400 hover:bg-red-500/10 transition-all duration-300"
              title="Logout"
            >
              <ArrowRightOnRectangleIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
      </header>

      <!-- Page content -->
      <main class="flex-1 p-8 overflow-y-auto bg-interview-bg pb-24 md:pb-8">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { HomeIcon, UserGroupIcon, CpuChipIcon, ChartBarSquareIcon, ArrowRightOnRectangleIcon } from '@heroicons/vue/24/solid'
import { useAuth } from '@/store/auth'
const route = useRoute()
const router = useRouter()
const authStore = useAuth()

// Check if route is active
const isActiveRoute = (path: string) => {
  return route.path === path || route.path.startsWith(path + '/')
}

// Handle logout
const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
