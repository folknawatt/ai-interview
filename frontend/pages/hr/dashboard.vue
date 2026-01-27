<template>
  <div class="relative min-h-[80vh] flex flex-col z-10">
    <!-- Ambient Background Elements -->
    <div class="fixed inset-0 z-0 pointer-events-none">
      <div class="absolute top-0 right-0 w-[500px] h-[500px] bg-interview-primary/10 rounded-full blur-[100px] animate-pulse"></div>
      <div class="absolute bottom-0 left-0 w-[300px] h-[300px] bg-interview-accent-teal/10 rounded-full blur-[80px]"></div>
    </div>

    <!-- Header Section -->
    <div class="mb-10 opacity-0 animate-fade-in-up" style="animation-delay: 0ms">
      <h1 class="text-5xl font-black tracking-tight mb-2">
        <span class="bg-gradient-to-r from-white via-white to-interview-text-secondary bg-clip-text text-transparent">
          Dashboard
        </span>
      </h1>
      <p class="text-interview-text-secondary text-lg font-medium">
        Overview of your AI interviewing platform
      </p>
    </div>

    <!-- Main Bento Grid -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      
      <!-- Primary Action: Generate Questions (Span 2 cols) -->
      <NuxtLink
        to="/hr/generate"
        class="group md:col-span-2 relative overflow-hidden rounded-3xl bg-gradient-to-br from-interview-surface to-interview-bg-secondary border border-interview-surface-border p-8 transition-all duration-500 hover:scale-[1.01] hover:shadow-glow-amber opacity-0 animate-fade-in-up"
        style="animation-delay: 100ms"
      >
        <div class="absolute inset-0 bg-interview-primary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
        <div class="relative z-10 h-full flex flex-col justify-between">
          <div>
            <div class="w-14 h-14 rounded-2xl bg-interview-primary/20 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-500">
              <CpuChipIcon class="w-8 h-8 text-interview-primary" />
            </div>
            <h2 class="text-3xl font-bold text-white mb-2">Generate Questions</h2>
            <p class="text-interview-text-secondary max-w-sm">
              Leverage AI to create tailored interview questions from any job description in seconds.
            </p>
          </div>
          <div class="mt-8 flex items-center gap-2 text-interview-primary font-semibold group-hover:translate-x-2 transition-transform">
            <span>Start Generation</span>
            <ArrowRightIcon class="w-5 h-5" />
          </div>
        </div>
        <!-- Decorative bg icon */ -->
        <CpuChipIcon class="absolute -bottom-8 -right-8 w-48 h-48 text-interview-surface-border opacity-10 rotate-[-15deg] group-hover:rotate-0 transition-all duration-700" />
      </NuxtLink>

      <!-- Roles Stat Card -->
      <NuxtLink
        to="/hr/roles"
        class="group col-span-1 relative overflow-hidden rounded-3xl bg-interview-surface backdrop-blur-md border border-interview-surface-border p-6 transition-all duration-300 hover:border-interview-accent-teal/50 opacity-0 animate-fade-in-up"
        style="animation-delay: 200ms"
      >
        <div class="flex justify-between items-start mb-4">
          <div class="p-3 rounded-xl bg-interview-accent-teal/10">
            <ClipboardDocumentListIcon class="w-6 h-6 text-interview-accent-teal" />
          </div>
          <div class="text-xs font-mono text-interview-accent-teal bg-interview-accent-teal/10 px-2 py-1 rounded-full">
            ACTIVE
          </div>
        </div>
        <div class="mt-auto">
          <div v-if="loading" class="h-8 w-16 bg-interview-surface-border animate-pulse rounded"></div>
          <div v-else class="text-4xl font-bold text-white mb-1">{{ roles.length }}</div>
          <div class="text-sm text-interview-text-secondary">Active Roles</div>
        </div>
      </NuxtLink>

      <!-- Reports Stat Card -->
      <NuxtLink
        to="/hr/reports"
        class="group col-span-1 relative overflow-hidden rounded-3xl bg-interview-surface backdrop-blur-md border border-interview-surface-border p-6 transition-all duration-300 hover:border-interview-accent-rose/50 opacity-0 animate-fade-in-up"
        style="animation-delay: 300ms"
      >
        <div class="flex justify-between items-start mb-4">
          <div class="p-3 rounded-xl bg-interview-accent-rose/10">
            <ChartBarSquareIcon class="w-6 h-6 text-interview-accent-rose" />
          </div>
        </div>
        <div class="mt-auto">
          <div v-if="loading" class="h-8 w-16 bg-interview-surface-border animate-pulse rounded"></div>
          <div v-else class="text-4xl font-bold text-white mb-1">{{ totalQuestions }}</div>
          <div class="text-sm text-interview-text-secondary">Questions Generated</div>
        </div>
        <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-interview-accent-rose to-transparent opacity-50"></div>
      </NuxtLink>

      <!-- Manage Roles (Span 2 cols) -->
      <NuxtLink
        to="/hr/roles"
        class="group md:col-span-2 relative overflow-hidden rounded-3xl bg-interview-surface backdrop-blur-xl border border-interview-surface-border p-8 flex items-center justify-between transition-all duration-300 hover:bg-interview-surface-hover opacity-0 animate-fade-in-up"
        style="animation-delay: 400ms"
      >
        <div>
           <div class="flex items-center gap-3 mb-2">
            <h3 class="text-2xl font-bold text-white">Manage Roles</h3>
            <span class="px-3 py-0.5 rounded-full text-xs font-bold bg-interview-bg-secondary border border-interview-surface-border text-interview-text-muted">
              Admin
            </span>
           </div>
           <p class="text-interview-text-secondary">Edit questions, review criteria, and manage role settings.</p>
        </div>
        <div class="w-12 h-12 rounded-full border border-interview-surface-border flex items-center justify-center group-hover:bg-interview-primary group-hover:border-interview-primary group-hover:text-interview-bg transition-all duration-300">
          <ArrowRightIcon class="w-5 h-5" />
        </div>
      </NuxtLink>

      <!-- View Reports (Span 2 cols) -->
      <NuxtLink
        to="/hr/reports"
        class="group md:col-span-2 relative overflow-hidden rounded-3xl bg-interview-surface backdrop-blur-xl border border-interview-surface-border p-8 flex items-center justify-between transition-all duration-300 hover:bg-interview-surface-hover opacity-0 animate-fade-in-up"
        style="animation-delay: 500ms"
      >
        <div>
           <div class="flex items-center gap-3 mb-2">
            <h3 class="text-2xl font-bold text-white">View Reports</h3>
            <span class="px-3 py-0.5 rounded-full text-xs font-bold bg-interview-bg-secondary border border-interview-surface-border text-interview-text-muted">
              Analytics
            </span>
           </div>
           <p class="text-interview-text-secondary">Deep dive into candidate performance and interview metrics.</p>
        </div>
        <div class="w-12 h-12 rounded-full border border-interview-surface-border flex items-center justify-center group-hover:bg-interview-accent-rose group-hover:border-interview-accent-rose group-hover:text-white transition-all duration-300">
          <ArrowRightIcon class="w-5 h-5" />
        </div>
      </NuxtLink>

    </div>

    <!-- Quick Activity / Status -->
    <div class="rounded-3xl bg-interview-bg-secondary/50 border border-interview-surface-border p-6 opacity-0 animate-fade-in-up" style="animation-delay: 600ms">
      <h3 class="text-lg font-semibold text-white mb-4 flex items-center gap-2">
        <div class="w-2 h-2 rounded-full bg-interview-success animate-pulse"></div>
        System Status
      </h3>
      <div v-if="loading" class="animate-pulse flex gap-4">
        <div class="h-4 w-32 bg-interview-surface rounded"></div>
      </div>
      <div v-else class="flex flex-wrap gap-6 text-sm text-interview-text-secondary">
        <div class="flex items-center gap-2">
           <CheckCircleIcon class="w-4 h-4 text-interview-success" />
           <span>System Operational</span>
        </div>
        <div class="flex items-center gap-2">
           <ClockIcon class="w-4 h-4 text-interview-primary" />
           <span>Last Sync: Just now</span>
        </div>
        <div class="flex items-center gap-2">
           <CloudIcon class="w-4 h-4 text-interview-info" />
           <span>Database: Connected</span>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import {
  CpuChipIcon,
  ClipboardDocumentListIcon,
  ChartBarSquareIcon,
  ArrowRightIcon,
  CheckCircleIcon,
  ClockIcon,
  CloudIcon
} from '@heroicons/vue/24/outline'; // Using outline for cleaner modern look, or solid for accents

definePageMeta({
  layout: 'hr',
  middleware: ['hr']
})

const { getRoles } = useHR();

const roles = ref<any[]>([]);
const loading = ref(true);

const totalQuestions = computed(() => {
  return roles.value.reduce((acc, role) => acc + (role.question_count || (role.questions ? role.questions.length : 0)), 0);
});

onMounted(async () => {
  try {
    roles.value = await getRoles();
  } catch (error) {
    console.error('Error loading roles:', error);
  } finally {
    loading.value = false;
  }
});
</script>
