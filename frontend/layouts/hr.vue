<template>
  <div class="min-h-screen bg-minimal-bg flex">
    <!-- Sidebar Navigation -->
    <aside class="w-64 bg-minimal-card border-r border-minimal-border flex-shrink-0">
      <div class="p-6">
        <h1 class="text-2xl font-bold text-minimal-text-primary mb-8">
          AI Interview
        </h1>
        
        <nav class="space-y-2">
          <NuxtLink
            to="/hr/dashboard"
            class="flex items-center gap-3 px-4 py-3 rounded-lg transition-colors"
            :class="isActiveRoute('/hr/dashboard') 
              ? 'bg-minimal-focus text-white' 
              : 'text-minimal-text-secondary hover:bg-minimal-border'"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            Dashboard
          </NuxtLink>
          
          <NuxtLink
            to="/hr/roles"
            class="flex items-center gap-3 px-4 py-3 rounded-lg transition-colors"
            :class="isActiveRoute('/hr/roles') 
              ? 'bg-minimal-focus text-white' 
              : 'text-minimal-text-secondary hover:bg-minimal-border'"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            Roles & Questions
          </NuxtLink>
          
          <NuxtLink
            to="/hr/generate"
            class="flex items-center gap-3 px-4 py-3 rounded-lg transition-colors"
            :class="isActiveRoute('/hr/generate') 
              ? 'bg-minimal-focus text-white' 
              : 'text-minimal-text-secondary hover:bg-minimal-border'"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            Generate Questions
          </NuxtLink>
          
          <NuxtLink
            to="/hr/reports"
            class="flex items-center gap-3 px-4 py-3 rounded-lg transition-colors"
            :class="isActiveRoute('/hr/reports') 
              ? 'bg-minimal-focus text-white' 
              : 'text-minimal-text-secondary hover:bg-minimal-border'"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Reports
          </NuxtLink>
        </nav>
      </div>
    </aside>

    <!-- Main content area -->
    <div class="flex-1 flex flex-col">
      <!-- Top header -->
      <header class="bg-minimal-card border-b border-minimal-border px-8 py-4">
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-semibold text-minimal-text-primary">
            HR Dashboard
          </h2>
          
          <div class="flex items-center gap-4">
            <span class="text-minimal-text-secondary">
              HR Admin
            </span>
            <button
              @click="handleLogout"
              class="text-minimal-text-secondary hover:text-minimal-warning transition-colors"
              title="Logout"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      <!-- Page content -->
      <main class="flex-1 p-8 overflow-y-auto">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
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
  authStore.clearToken()
  router.push('/login')
}
</script>
