<template>
  <div 
    class="min-h-screen bg-interview-bg text-interview-text-primary flex items-center justify-center p-4 relative overflow-hidden"
    @mousemove="handleMouseMove"
  >
    <!-- Background gradient effects -->
    <div class="fixed inset-0 z-0 bg-interview-bg">
      <div class="absolute inset-0 bg-gradient-to-b from-black/80 via-interview-bg to-black"></div>
      <div 
        class="absolute top-1/3 -left-48 w-[500px] h-[500px] bg-interview-primary/10 rounded-full blur-3xl transition-transform duration-100 ease-out will-change-transform"
        :style="{ transform: `translate(${mouseParallax.x * 20}px, ${mouseParallax.y * 20}px)` }"
      ></div>
      <div 
        class="absolute bottom-1/3 -right-48 w-[500px] h-[500px] bg-interview-accent-teal/10 rounded-full blur-3xl transition-transform duration-100 ease-out will-change-transform delay-75"
        :style="{ transform: `translate(${mouseParallax.x * -15}px, ${mouseParallax.y * -15}px)` }"
      ></div>
    </div>

    <!-- Main Content (Blurred when modal is open) -->
    <div 
      class="relative z-10 w-full max-w-5xl transition-all duration-300"
      :class="{ 'blur-sm pointer-events-none scale-95': isUploadModalOpen }"
    >
      <div class="text-center mb-12 animate-fade-in">
        <h1 class="text-4xl md:text-5xl font-bold mb-4 flex items-center justify-center gap-3">
          <ChartPieIcon class="w-12 h-12 text-interview-primary drop-shadow-[0_0_10px_rgba(255,191,0,0.5)]" />
          <span class="bg-gradient-to-r from-interview-text-primary via-white to-interview-primary bg-clip-text text-transparent drop-shadow-lg">Select Your Role</span>
        </h1>
        <p class="text-interview-text-secondary text-lg">Choose the position you're interviewing for</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin w-12 h-12 border-4 border-interview-primary border-t-transparent rounded-full mx-auto mb-4"></div>
        <p class="text-interview-text-secondary">Loading available positions...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-interview-warning/10 border border-interview-warning/30 backdrop-blur-xl rounded-2xl p-8 text-center">
        <div class="flex justify-center mb-4">
          <ExclamationTriangleIcon class="w-16 h-16 text-interview-warning" />
        </div>
        <p class="text-interview-warning mb-4">{{ error }}</p>
        <button
          @click="loadRoles"
          class="px-6 py-3 bg-interview-warning hover:bg-red-600 text-white rounded-xl font-semibold transition-all shadow-sm"
        >
          Try Again
        </button>
      </div>

      <!-- Roles Grid -->
      <div v-else-if="roles.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <button
          v-for="(role, index) in roles"
          :key="role.id"
          @click="openUploadModal(role)"
          :style="{ animationDelay: `${index * 100}ms` }"
          class="group bg-interview-surface backdrop-blur-xl p-8 rounded-2xl border border-interview-surface-border hover:border-interview-primary/50 hover:bg-interview-surface-hover transition-all duration-300 text-left animate-fade-in-up hover:shadow-glow-amber hover:-translate-y-1 h-full flex flex-col items-center"
        >
          <div class="mb-4 flex-shrink-0">
            <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-interview-primary/10 to-interview-primary/5 flex items-center justify-center group-hover:bg-interview-primary/20 transition-all duration-300 ring-1 ring-interview-primary/20 group-hover:ring-interview-primary/50 group-hover:shadow-glow-amber">
              <BriefcaseIcon class="w-10 h-10 text-interview-primary transition-transform duration-300 group-hover:scale-110" />
            </div>
          </div>
          <h3 class="text-xl font-bold mb-3 text-interview-text-primary text-center group-hover:text-interview-primary transition-colors">{{ role.title }}</h3>
          <p class="text-interview-text-muted text-sm text-center mt-auto flex items-center gap-1 group-hover:text-interview-text-secondary transition-colors">
            Tap to select
            <ArrowRightIcon class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity transform translate-x-[-4px] group-hover:translate-x-0" />
          </p>
        </button>
      </div>

      <!-- Empty State -->
      <div v-else class="bg-interview-surface backdrop-blur-xl rounded-2xl p-12 text-center border border-interview-surface-border">
        <div class="flex justify-center mb-4">
          <DocumentTextIcon class="w-16 h-16 text-interview-text-muted" />
        </div>
        <h2 class="text-2xl font-semibold mb-2 text-interview-text-primary">No Positions Available</h2>
        <p class="text-interview-text-secondary mb-6">Please contact HR to set up interview questions</p>
        <NuxtLink
          to="/"
          class="inline-block px-6 py-3 bg-interview-primary hover:bg-interview-primary-hover text-interview-bg rounded-xl font-semibold transition-all shadow-glow-amber"
        >
          Go Back
        </NuxtLink>
      </div>

      <!-- Back Button -->
      <div v-if="!loading" class="mt-8 text-center">
        <NuxtLink
          to="/login"
          class="text-interview-text-secondary hover:text-interview-primary transition-colors duration-300 flex items-center justify-center gap-2"
        >
          <ArrowLeftIcon class="w-4 h-4" />
          Back to Login
        </NuxtLink>
      </div>
    </div>

    <!-- Upload Modal Overlay -->
    <Transition
      enter-active-class="transition-all duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-all duration-300"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="isUploadModalOpen" class="fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-4">
        <div class="bg-interview-bg-secondary border border-interview-surface-border rounded-2xl shadow-2xl max-w-md w-full p-8 animate-fade-in-up relative overflow-hidden">
           <!-- Decorative blob -->
           <div class="absolute -top-20 -right-20 w-40 h-40 bg-interview-primary/10 rounded-full blur-2xl pointer-events-none"></div>

           <!-- Modal Data -->
           <h2 class="text-2xl font-bold mb-2 text-center text-interview-text-primary relative z-10">
             Upload Resume
           </h2>
           <p class="text-center text-interview-text-secondary mb-6 relative z-10">Generate AI questions for <span class="text-interview-primary font-semibold">{{ selectedRoleForUpload?.title }}</span> based on your CV</p>

           <!-- Drop Zone / File Input -->
           <div 
              class="border-2 border-dashed border-interview-surface-border rounded-2xl p-8 mb-6 text-center transition-all duration-300 cursor-pointer bg-interview-surface/30 group relative overflow-hidden"
              :class="{ 'border-interview-primary bg-interview-primary/5': isDragging, 'hover:border-interview-primary/50 hover:bg-interview-surface/60': !isDragging }"
              @click="triggerFileInput"
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
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
                  <DocumentTextIcon class="w-12 h-12 text-interview-text-muted mx-auto mb-2 group-hover:text-interview-primary transition-colors" />
                  <p class="text-sm font-medium text-interview-text-secondary">Click to upload PDF</p>
                  <p class="text-xs text-interview-text-muted mt-1">or drag and drop</p>
               </div>
               <div v-else>
                   <DocumentTextIcon class="w-12 h-12 text-interview-success mx-auto mb-2" />
                   <p class="text-sm font-medium text-interview-text-primary truncate">{{ selectedFile.name }}</p>
                   <p class="text-xs text-interview-success mt-1">Ready to upload</p>
               </div>
           </div>

           <!-- Error Message -->
           <div v-if="uploadError" class="mb-4 text-sm text-interview-warning bg-interview-warning/10 p-3 rounded-xl flex items-start gap-2 border border-interview-warning/30">
              <ExclamationTriangleIcon class="w-5 h-5 flex-shrink-0" />
              <span>{{ uploadError }}</span>
           </div>
           
           <!-- Actions -->
           <div class="flex flex-col gap-3">
              <button 
                @click="handleUploadAndStart"
                :disabled="!selectedFile || isUploading"
                class="w-full py-3.5 bg-interview-primary hover:bg-interview-primary-hover disabled:bg-interview-text-muted disabled:cursor-not-allowed text-interview-bg rounded-xl font-semibold transition-all duration-300 shadow-glow-amber hover:shadow-glow-amber-lg flex justify-center items-center gap-2"
              >
                <span v-if="isUploading" class="animate-spin w-5 h-5 border-2 border-interview-bg border-t-transparent rounded-full"></span>
                {{ isUploading ? 'Generating Questions...' : 'Start Interview' }}
              </button>
              
              <button 
                @click="closeUploadModal"
                :disabled="isUploading"
                class="w-full py-3 text-interview-text-secondary hover:text-interview-text-primary disabled:text-interview-text-muted transition-colors duration-300"
              >
                Cancel
              </button>
           </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import {
  ChartPieIcon,
  ExclamationTriangleIcon,
  BriefcaseIcon,
  DocumentTextIcon,
  ArrowRightIcon,
  ArrowLeftIcon
} from '@heroicons/vue/24/solid';

import type { Role } from '@/types';

definePageMeta({
  layout: 'blank'
})

// Use composables
const { getRoles } = useHR();
const { setSelectedRole, uploadResume, sessionId } = useInterview();
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
const isDragging = ref(false);

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
  isDragging.value = false;
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
    // 1. Upload Resume & Generate Questions (and Session)
    // accessible via useInterview destructuring if needed, or just use result
    const result = await uploadResume(selectedFile.value, selectedRoleForUpload.value.id);
    
    // 2. Set Global State
    // We use the Base Role ID (not candidate specific anymore)
    const baseRole = {
       id: result.role_id,
       name: selectedRoleForUpload.value.title
    };
    
    // Set role (this triggers a client session ID generation)
    setSelectedRole(baseRole);

    // 3. Update Session ID from Server
    if (result.session_id) {
        sessionId.value = result.session_id;
    }
    
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
