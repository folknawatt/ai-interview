<template>
  <div class="min-h-screen bg-minimal-bg text-minimal-text-primary p-8">
    <div class="max-w-6xl mx-auto">
      <h1 class="text-4xl font-bold mb-8 flex items-center gap-3">
        <ChartBarIcon class="w-10 h-10 text-minimal-info" />
        HR Dashboard
      </h1>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Generate Questions Card -->
        <NuxtLink
          to="/hr/generate"
          class="bg-minimal-card border-2 border-minimal-info p-8 rounded-xl shadow-sm hover:shadow-md transition-all hover:scale-[1.02]"
        >
          <div class="flex justify-center mb-4">
            <CpuChipIcon class="w-16 h-16 text-minimal-info" />
          </div>
          <h2 class="text-2xl font-bold mb-2 text-minimal-text-primary">Generate Questions</h2>
          <p class="text-minimal-text-secondary">Use AI to create interview questions from job descriptions</p>
        </NuxtLink>

        <!-- View Roles Card -->
        <NuxtLink
          to="/hr/roles"
          class="bg-minimal-card border-2 border-minimal-success p-8 rounded-xl shadow-sm hover:shadow-md transition-all hover:scale-[1.02]"
        >
          <div class="flex justify-center mb-4">
            <ClipboardDocumentListIcon class="w-16 h-16 text-minimal-success" />
          </div>
          <h2 class="text-2xl font-bold mb-2 text-minimal-text-primary">Manage Roles</h2>
          <p class="text-minimal-text-secondary">View and manage all interview questions by role</p>
        </NuxtLink>

        <!-- View Reports Card -->
        <NuxtLink
          to="/hr/reports"
          class="bg-minimal-card border-2 border-purple-400 p-8 rounded-xl shadow-sm hover:shadow-md transition-all hover:scale-[1.02]"
        >
          <div class="flex justify-center mb-4">
            <ChartBarSquareIcon class="w-16 h-16 text-purple-500" />
          </div>
          <h2 class="text-2xl font-bold mb-2 text-minimal-text-primary">View Reports</h2>
          <p class="text-minimal-text-secondary">Review interview results, scores, and analytics</p>
        </NuxtLink>
      </div>

      <!-- Quick Stats -->
      <div class="mt-12 bg-minimal-card p-6 rounded-xl border border-minimal-border">
        <h3 class="text-xl font-semibold mb-4">Quick Stats</h3>
        <div v-if="!loading" class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="text-center">
            <div class="text-3xl font-bold text-minimal-info">{{ roles.length }}</div>
            <div class="text-minimal-text-secondary">Active Roles</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-minimal-success">{{ totalQuestions }}</div>
            <div class="text-minimal-text-secondary">Total Questions</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-purple-500">~{{ avgQuestions }}</div>
            <div class="text-minimal-text-secondary">Avg Questions/Role</div>
          </div>
        </div>
        <div v-else class="text-center text-minimal-text-secondary">Loading stats...</div>
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
