

<template>
  <div class="min-h-screen bg-minimal-bg text-minimal-text-primary flex items-center justify-center p-4">
    <!-- Main Content (Blurred when modal is open) -->
    <div 
      class="w-full max-w-4xl transition-all duration-300"
      :class="{ 'blur-sm pointer-events-none': isUploadModalOpen }"
    >
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
      <div v-else-if="error" class="bg-red-50 border-2 border-red-200 rounded-xl p-8 text-center">
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
          @click="openUploadModal(role)"
          class="bg-minimal-card p-8 rounded-xl border-2 border-minimal-border hover:border-minimal-info hover:shadow-md hover:scale-[1.02] transition-all text-left"
        >
          <div class="flex justify-center mb-4">
            <BriefcaseIcon class="w-14 h-14 text-minimal-info" />
          </div>
          <h3 class="text-2xl font-bold mb-2 text-minimal-text-primary">{{ role.title }}</h3>
          <p class="text-minimal-text-secondary text-sm">Click to select</p>
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

    <!-- Upload Modal Overlay -->
    <div v-if="isUploadModalOpen" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 animate-fade-in-up">
         <!-- Modal Data -->
         <h2 class="text-2xl font-bold mb-2 text-center">
           Upload Resume
         </h2>
         <p class="text-center text-gray-500 mb-6">Create custom questions for {{ selectedRoleForUpload?.title }}</p>

         <!-- Drop Zone / File Input -->
         <div 
            class="border-2 border-dashed border-gray-300 rounded-xl p-8 mb-6 text-center hover:border-minimal-info transition-colors cursor-pointer bg-gray-50"
            @click="triggerFileInput"
            @dragover.prevent
            @drop.prevent="handleDrop"
         >
             <input 
               type="file" 
               ref="fileInputRef" 
               class="hidden" 
               accept=".pdf"
               @change="handleFileChange"
             />
             <div v-if="!selectedFile">
                <DocumentTextIcon class="w-12 h-12 text-gray-400 mx-auto mb-2" />
                <p class="text-sm font-medium text-gray-700">Click to upload PDF</p>
                <p class="text-xs text-gray-500 mt-1">or drag and drop</p>
             </div>
             <div v-else>
                 <DocumentTextIcon class="w-12 h-12 text-green-500 mx-auto mb-2" />
                 <p class="text-sm font-medium text-gray-900 truncate">{{ selectedFile.name }}</p>
                 <p class="text-xs text-green-600 mt-1">Ready to upload</p>
             </div>
         </div>

         <!-- Error Message -->
         <div v-if="uploadError" class="mb-4 text-sm text-red-600 bg-red-50 p-3 rounded-lg flex items-start gap-2">
            <ExclamationTriangleIcon class="w-5 h-5 flex-shrink-0" />
            <span>{{ uploadError }}</span>
         </div>
         
         <!-- Actions -->
         <div class="flex flex-col gap-3">
            <button 
              @click="handleUploadAndStart"
              :disabled="!selectedFile || isUploading"
              class="w-full py-3 bg-minimal-info hover:bg-sky-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white rounded-lg font-semibold transition-all shadow-md flex justify-center items-center gap-2"
            >
              <span v-if="isUploading" class="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full"></span>
              {{ isUploading ? 'Generating Questions...' : 'Start Interview' }}
            </button>
            
            <button 
              @click="closeUploadModal"
              :disabled="isUploading"
              class="w-full py-3 text-gray-500 hover:text-gray-700 disabled:text-gray-300 transition-colors"
            >
              Cancel
            </button>
         </div>
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

// Use composables
const { getRoles } = useHR();
const { setSelectedRole, uploadResume } = useInterview();
const router = useRouter();

// State
const roles = ref<Role[]>([]);
const loading = ref(true);
const error = ref('');

// Modal State
const isUploadModalOpen = ref(false);
const selectedRoleForUpload = ref<Role | null>(null);
const selectedFile = ref<File | null>(null);
const fileInputRef = ref<HTMLInputElement | null>(null);
const isUploading = ref(false);
const uploadError = ref('');

// Load Roles
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

// Modal Actions
const openUploadModal = (role: Role) => {
  selectedRoleForUpload.value = role;
  selectedFile.value = null;
  uploadError.value = '';
  isUploadModalOpen.value = true;
};

const closeUploadModal = () => {
  if (isUploading.value) return;
  isUploadModalOpen.value = false;
  selectedRoleForUpload.value = null;
  selectedFile.value = null;
};

// File Handlers
const triggerFileInput = () => {
  fileInputRef.value?.click();
};

const handleFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    validateAndSetFile(target.files[0]);
  }
};

const handleDrop = (e: DragEvent) => {
  if (e.dataTransfer?.files && e.dataTransfer.files[0]) {
    validateAndSetFile(e.dataTransfer.files[0]);
  }
};

const validateAndSetFile = (file: File) => {
  uploadError.value = '';
  if (file.type !== 'application/pdf') {
    uploadError.value = 'Please upload a PDF file.';
    return;
  }
  selectedFile.value = file;
};

// Upload & Start
const handleUploadAndStart = async () => {
  if (!selectedFile.value || !selectedRoleForUpload.value) return;
  
  isUploading.value = true;
  uploadError.value = '';

  try {
    // 1. Upload Resume & Generate Questions
    const result = await uploadResume(selectedFile.value, selectedRoleForUpload.value.id);
    
    // 2. Set the NEW candidate-specific Role (using the ID returned by backend)
    // Create detailed role object
    const candidateRole = {
       id: result.role_id,
       name: selectedRoleForUpload.value.title // Map title to name as expected by store
    };
    
    // 3. Set Global State & Navigate
    setSelectedRole(candidateRole);
    router.push('/question');
    
  } catch (err: any) {
    console.error(err);
    uploadError.value = err.message || 'Failed to upload resume. Please try again.';
  } finally {
    isUploading.value = false;
  }
};

onMounted(() => {
  loadRoles();
});
</script>
