<template>
  <div class="min-h-screen bg-minimal-bg text-minimal-text-primary flex items-center justify-center p-4">
    <div class="w-full max-w-4xl">
      <div class="text-center mb-12">
        <h1 class="text-5xl font-bold mb-4 flex items-center justify-center gap-3">
          <ChartPieIcon class="w-12 h-12 text-minimal-info" />
          Select Your Role
        </h1>
        <p class="text-minimal-text-secondary text-lg">Choose the position you're interviewing for</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin w-12 h-12 border-4 border-minimal-info border-t-transparent rounded-full mx-auto mb-4"></div>
        <p class="text-minimal-text-secondary">Loading available positions...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border-2 border-red-200 rounded- xl p-8 text-center">
        <div class="flex justify-center mb-4">
          <ExclamationTriangleIcon class="w-16 h-16 text-red-600" />
        </div>
        <p class="text-red-600 mb-4">{{ error }}</p>
        <button
          @click="loadRoles"
          class="px-6 py-3 bg-minimal-warning hover:bg-red-700 text-white rounded-lg font-semibold transition-all shadow-sm"
        >
          Try Again
        </button>
      </div>

      <!-- Roles Grid -->
      <div v-else-if="roles.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <button
          v-for="role in roles"
          :key="role.id"
          @click="selectRole(role)"
          class="bg-minimal-card p-8 rounded-xl border-2 border-minimal-border hover:border-minimal-info hover:shadow-md hover:scale-[1.02] transition-all text-left"
        >
          <div class="flex justify-center mb-4">
            <BriefcaseIcon class="w-14 h-14 text-minimal-info" />
          </div>
          <h3 class="text-2xl font-bold mb-2 text-minimal-text-primary">{{ role.title }}</h3>
          <p class="text-minimal-text-secondary text-sm">Click to start interview</p>
        </button>
      </div>

      <!-- Empty State -->
      <div v-else class="bg-minimal-card rounded-xl p-12 text-center border border-minimal-border">
        <div class="flex justify-center mb-4">
          <DocumentTextIcon class="w-16 h-16 text-minimal-text-muted" />
        </div>
        <h2 class="text-2xl font-semibold mb-2">No Positions Available</h2>
        <p class="text-minimal-text-secondary mb-6">Please contact HR to set up interview questions</p>
        <NuxtLink
          to="/"
          class="inline-block px-6 py-3 bg-minimal-info hover:bg-sky-600 text-white rounded-lg font-semibold transition-all shadow-sm"
        >
          Go Back
        </NuxtLink>
      </div>

      <!-- Back Button -->
      <div v-if="!loading" class="mt-8 text-center">
        <NuxtLink
          to="/login"
          class="text-minimal-text-secondary hover:text-minimal-text-primary transition-colors"
        >
          ← Back to Login
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  ChartPieIcon,
  ExclamationTriangleIcon,
  BriefcaseIcon,
  DocumentTextIcon
} from '@heroicons/vue/24/solid';

import type { Role } from '@/types';

const { getRoles } = useHR();
const { setSelectedRole } = useInterview();
const router = useRouter();

const roles = ref<Role[]>([]);
const loading = ref(true);
const error = ref('');

const loadRoles = async () => {
  loading.value = true;
  error.value = '';

  try {
    roles.value = await getRoles();
  } catch (err: any) {
    error.value = err.message || 'Failed to load available roles';
  } finally {
    loading.value = false;
  }
};

const selectRole = (role: any) => {
  setSelectedRole(role);
  router.push('/question');
};

onMounted(() => {
  loadRoles();
});
</script>
