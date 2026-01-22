<template>
  <div class="text-interview-text-primary p-8">
    <div class="max-w-6xl mx-auto">
      <h1 class="dashboard-anim text-4xl font-bold mb-8 flex items-center gap-3 text-interview-text-primary" style="--delay: 0ms">
        <ChartBarIcon class="w-10 h-10 text-interview-primary" />
        HR Dashboard
      </h1>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Generate Questions Card -->
        <NuxtLink
          to="/hr/generate"
          class="dashboard-anim group bg-interview-surface backdrop-blur-xl border border-interview-surface-border p-8 rounded-2xl hover:border-interview-accent-teal/50 transition-all duration-300 hover:scale-[1.02] hover:shadow-lg"
          style="--delay: 80ms"
        >
          <div class="flex justify-center mb-4">
            <div class="p-4 bg-interview-accent-teal/20 rounded-2xl group-hover:bg-interview-accent-teal/30 transition-colors">
              <CpuChipIcon class="w-12 h-12 text-interview-accent-teal" />
            </div>
          </div>
          <h2 class="text-2xl font-bold mb-2 text-interview-text-primary text-center">Generate Questions</h2>
          <p class="text-interview-text-secondary text-center">Use AI to create interview questions from job descriptions</p>
        </NuxtLink>

        <!-- View Roles Card -->
        <NuxtLink
          to="/hr/roles"
          class="dashboard-anim group bg-interview-surface backdrop-blur-xl border border-interview-surface-border p-8 rounded-2xl hover:border-interview-primary/50 transition-all duration-300 hover:scale-[1.02] hover:shadow-lg"
          style="--delay: 160ms"
        >
          <div class="flex justify-center mb-4">
            <div class="p-4 bg-interview-primary/20 rounded-2xl group-hover:bg-interview-primary/30 transition-colors">
              <ClipboardDocumentListIcon class="w-12 h-12 text-interview-primary" />
            </div>
          </div>
          <h2 class="text-2xl font-bold mb-2 text-interview-text-primary text-center">Manage Roles</h2>
          <p class="text-interview-text-secondary text-center">View and manage all interview questions by role</p>
        </NuxtLink>

        <!-- View Reports Card -->
        <NuxtLink
          to="/hr/reports"
          class="dashboard-anim group bg-interview-surface backdrop-blur-xl border border-interview-surface-border p-8 rounded-2xl hover:border-interview-accent-rose/50 transition-all duration-300 hover:scale-[1.02] hover:shadow-lg"
          style="--delay: 240ms"
        >
          <div class="flex justify-center mb-4">
            <div class="p-4 bg-interview-accent-rose/20 rounded-2xl group-hover:bg-interview-accent-rose/30 transition-colors">
              <ChartBarSquareIcon class="w-12 h-12 text-interview-accent-rose" />
            </div>
          </div>
          <h2 class="text-2xl font-bold mb-2 text-interview-text-primary text-center">View Reports</h2>
          <p class="text-interview-text-secondary text-center">Review interview results, scores, and analytics</p>
        </NuxtLink>
      </div>

      <!-- Quick Stats -->
      <div class="dashboard-anim mt-12 bg-interview-surface backdrop-blur-xl p-6 rounded-2xl border border-interview-surface-border" style="--delay: 320ms">
        <h3 class="text-xl font-semibold mb-6 text-interview-text-primary">Quick Stats</h3>
        <div v-if="!loading" class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="text-center p-4 bg-interview-bg-secondary rounded-xl">
            <div class="text-3xl font-bold text-interview-accent-sky">{{ roles.length }}</div>
            <div class="text-interview-text-secondary mt-1">Active Roles</div>
          </div>
          <div class="text-center p-4 bg-interview-bg-secondary rounded-xl">
            <div class="text-3xl font-bold text-interview-accent-teal">{{ totalQuestions }}</div>
            <div class="text-interview-text-secondary mt-1">Total Questions</div>
          </div>
          <div class="text-center p-4 bg-interview-bg-secondary rounded-xl">
            <div class="text-3xl font-bold text-interview-accent-olive">~{{ avgQuestions }}</div>
            <div class="text-interview-text-secondary mt-1">Avg Questions/Role</div>
          </div>
        </div>
        <div v-else class="text-center text-interview-text-secondary py-4">
          <div class="animate-spin w-8 h-8 border-4 border-interview-primary border-t-transparent rounded-full mx-auto mb-2"></div>
          Loading stats...
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  ChartBarIcon,
  CpuChipIcon,
  ClipboardDocumentListIcon,
  ChartBarSquareIcon
} from '@heroicons/vue/24/solid';

const { getRoles } = useHR();

const roles = ref<any[]>([]);
const loading = ref(true);

const totalQuestions = computed(() => roles.value.length * 3); // Assuming 3 questions per role
const avgQuestions = computed(() => roles.value.length > 0 ? 3 : 0);

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

<style scoped>
/* Smooth staggered animation */
.dashboard-anim {
  opacity: 0;
  transform: translate3d(0, 20px, 0);
  animation: dashboard-fade-in 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: var(--delay, 0ms);
}

@keyframes dashboard-fade-in {
  from {
    opacity: 0;
    transform: translate3d(0, 20px, 0);
  }
  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
}
</style>
