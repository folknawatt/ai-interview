<template>
  <div class="relative min-h-[80vh] pb-20 z-10">
    <!-- Ambient Background Elements -->
    <div class="fixed inset-0 z-0 pointer-events-none">
      <div class="absolute top-20 right-1/4 w-[400px] h-[400px] bg-interview-primary/5 rounded-full blur-[100px] animate-pulse"></div>
      <div class="absolute bottom-40 left-10 w-[300px] h-[300px] bg-interview-accent-teal/10 rounded-full blur-[80px]"></div>
    </div>

    <!-- Header Section -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-10 opacity-0 animate-fade-in-up" style="animation-delay: 0ms">
      <div>
        <NuxtLink 
          to="/hr/dashboard" 
          class="inline-flex items-center gap-2 text-interview-text-secondary hover:text-white transition-colors mb-4 group"
        >
          <ArrowLeftIcon class="w-4 h-4 transition-transform group-hover:-translate-x-1" />
          Back to Dashboard
        </NuxtLink>
        <h1 class="text-4xl md:text-5xl font-black tracking-tight text-white mb-2 flex items-center gap-3">
          Manage Roles
          <span class="text-lg font-normal text-interview-text-secondary bg-interview-surface px-3 py-1 rounded-full border border-interview-surface-border">
            {{ roles.length }} Total
          </span>
        </h1>
        <p class="text-interview-text-secondary text-lg">
          Create and manage interview questions for different positions.
        </p>
      </div>

      <!-- Primary Action -->
      <div v-if="!loading && roles.length > 0">
        <NuxtLink
          to="/hr/generate"
          class="inline-flex items-center gap-2 px-6 py-3 bg-interview-primary text-interview-bg rounded-xl font-bold transition-all hover:bg-interview-primary-hover hover:shadow-glow-amber group"
        >
          <PlusIcon class="w-5 h-5 transition-transform group-hover:rotate-90" />
          Add New Role
        </NuxtLink>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-20">
      <div class="animate-spin w-12 h-12 border-4 border-interview-primary border-t-transparent rounded-full mb-4"></div>
      <p class="text-interview-text-secondary">Loading roles...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="roles.length === 0" class="flex flex-col items-center justify-center py-20 bg-interview-surface/30 rounded-3xl border border-interview-surface-border opacity-0 animate-fade-in-up" style="animation-delay: 100ms">
      <div class="w-20 h-20 bg-interview-bg-secondary rounded-full flex items-center justify-center mb-6">
        <DocumentTextIcon class="w-10 h-10 text-interview-text-muted" />
      </div>
      <h2 class="text-2xl font-bold text-white mb-2">No Roles Found</h2>
      <p class="text-interview-text-secondary mb-8 max-w-md text-center">
        Your question bank is empty. Start by generating questions for a new role using AI.
      </p>
      <NuxtLink
        to="/hr/generate"
        class="inline-flex items-center gap-2 px-8 py-4 bg-interview-primary text-interview-bg rounded-xl font-bold transition-all hover:bg-interview-primary-hover hover:shadow-glow-amber hover:scale-105"
      >
        <SparklesIcon class="w-5 h-5" />
        Generate Questions
      </NuxtLink>
    </div>

    <!-- Roles Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="(role, roleIndex) in roles"
        :key="role.id"
        class="group relative bg-interview-surface backdrop-blur-xl p-6 rounded-3xl border border-interview-surface-border hover:border-interview-primary/50 transition-all duration-300 hover:shadow-lg hover:-translate-y-1 role-card"
        :style="{ '--delay': `${roleIndex * 50}ms` }"
      >
        <!-- Card Header -->
        <div class="flex items-start justify-between mb-6">
          <div class="p-3 rounded-2xl bg-gradient-to-br from-interview-surface to-interview-bg-secondary border border-interview-surface-border group-hover:border-interview-primary/30 transition-colors">
            <BriefcaseIcon class="w-8 h-8 text-interview-primary" />
          </div>
          <div class="flex gap-2">
            <button
               @click="startEdit(role)"
               class="p-2 rounded-xl text-interview-text-muted hover:text-white hover:bg-interview-surface-hover transition-colors"
               title="Edit Questions"
            >
              <PencilSquareIcon class="w-5 h-5" />
            </button>
            <button
               @click="startDelete(role)"
               class="p-2 rounded-xl text-interview-text-muted hover:text-red-400 hover:bg-red-500/10 transition-colors"
               title="Delete Role"
            >
              <TrashIcon class="w-5 h-5" />
            </button>
          </div>
        </div>

        <h3 class="text-xl font-bold text-white mb-2 group-hover:text-interview-primary transition-colors">{{ role.title }}</h3>
        <div class="flex items-center gap-2 mb-6">
           <span class="text-xs font-bold px-2 py-1 rounded bg-interview-bg-secondary text-interview-text-secondary border border-interview-surface-border">
             {{ role.questionCount }} Questions
           </span>
        </div>

        <!-- Preview Questions (First 2) -->
        <div class="space-y-3 mb-6 min-h-[100px]">
           <div 
             v-for="(question, qIndex) in role.questions.slice(0, 2)" 
             :key="qIndex"
             class="flex gap-3 text-sm text-interview-text-secondary"
           >
             <span class="font-mono text-interview-primary/50">0{{ qIndex + 1 }}</span>
             <p class="line-clamp-2">{{ question }}</p>
           </div>
           <p v-if="role.questions.length > 2" class="text-xs text-interview-text-muted italic pl-7">
             + {{ role.questions.length - 2 }} more questions...
           </p>
        </div>

        <!-- Action Footer -->
        <div class="pt-4 border-t border-interview-surface-border flex justify-between items-center">
            <button 
              @click="copyQuestions(role)"
              class="text-sm font-medium text-interview-text-secondary hover:text-white flex items-center gap-2 transition-colors"
            >
              <ClipboardDocumentIcon class="w-4 h-4" />
              Copy All
            </button>
            <span class="text-[10px] text-interview-text-muted uppercase tracking-wider">Updated Now</span>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-if="editingRole" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/80 backdrop-blur-sm" @click="cancelEdit"></div>
        
        <!-- Modal Content -->
        <div class="relative bg-interview-bg w-full max-w-3xl rounded-3xl border border-interview-surface-border shadow-2xl flex flex-col max-h-[85vh]">
          
          <!-- Header -->
          <div class="p-6 border-b border-interview-surface-border flex items-center justify-between bg-interview-bg-secondary/30 backdrop-blur-xl">
            <div>
              <h2 class="text-2xl font-bold text-white flex items-center gap-2">
                <PencilSquareIcon class="w-6 h-6 text-interview-primary" />
                Edit Questions
              </h2>
              <p class="text-interview-text-secondary text-sm mt-1">Editing {{ editingRole.title }}</p>
            </div>
            <button @click="cancelEdit" class="text-interview-text-muted hover:text-white transition-colors">
              <XMarkIcon class="w-6 h-6" />
            </button>
          </div>

          <!-- Body -->
          <div class="p-6 overflow-y-auto custom-scrollbar space-y-4">
             <!-- Role Title Input -->
             <div class="mb-2">
                <label class="block text-xs font-bold text-interview-text-muted uppercase tracking-wider mb-2">Role Title</label>
                <input 
                  v-model="editingRoleTitle"
                  type="text"
                  class="w-full bg-interview-bg-secondary border border-interview-surface-border rounded-xl px-4 py-3 text-white font-bold text-lg focus:border-interview-primary focus:ring-1 focus:ring-interview-primary outline-none transition-all"
                  placeholder="Role Title"
                />
             </div>
             
             <div class="h-px bg-interview-surface-border my-4"></div>

             <div v-for="(question, index) in editedQuestions" :key="index" class="group flex gap-4 items-start">
                <span class="mt-4 text-sm font-mono text-interview-text-muted w-6 text-right">{{ index + 1 }}.</span>
                <div class="flex-1">
                  <textarea 
                    v-model="editedQuestions[index]"
                    rows="2"
                    class="w-full bg-interview-bg-secondary border border-interview-surface-border rounded-xl p-3 text-interview-text-primary focus:border-interview-primary focus:ring-1 focus:ring-interview-primary outline-none transition-all resize-none"
                    placeholder="Enter question..."
                  ></textarea>
                </div>
                <button 
                  @click="removeQuestion(index)"
                  class="mt-3 p-2 rounded-lg text-interview-text-muted hover:bg-red-500/10 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-all"
                  :disabled="editedQuestions.length === 1"
                  title="Remove"
                >
                  <TrashIcon class="w-5 h-5" />
                </button>
             </div>

             <button 
               @click="addQuestion"
               class="w-full py-4 border-2 border-dashed border-interview-surface-border rounded-xl text-interview-text-secondary hover:text-interview-primary hover:border-interview-primary/50 hover:bg-interview-surface transition-all flex items-center justify-center gap-2"
             >
               <PlusIcon class="w-5 h-5" />
               Add New Question
             </button>
          </div>

          <!-- Footer -->
          <div class="p-6 border-t border-interview-surface-border bg-interview-bg-secondary/30 backdrop-blur-xl flex justify-end gap-3 rounded-b-3xl">
            <button 
              @click="cancelEdit"
              class="px-6 py-2.5 rounded-xl border border-interview-surface-border text-interview-text-primary hover:bg-interview-surface-hover transition-colors font-medium"
            >
              Cancel
            </button>
            <button 
              @click="saveEdit"
              :disabled="saving"
              class="px-6 py-2.5 rounded-xl bg-interview-primary text-interview-bg hover:bg-interview-primary-hover font-bold transition-all shadow-glow-amber disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <span v-if="saving" class="animate-spin w-4 h-4 border-2 border-interview-bg border-t-transparent rounded-full"></span>
              {{ saving ? 'Saving Changes...' : 'Save Changes' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Delete Confirmation Modal (Reused styles) -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-if="deletingRole" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/80 backdrop-blur-sm" @click="cancelDelete"></div>
        <div class="relative bg-interview-bg w-full max-w-md rounded-3xl border border-interview-surface-border shadow-2xl p-6">
          <div class="flex flex-col items-center text-center">
            <div class="w-16 h-16 bg-red-500/10 rounded-full flex items-center justify-center mb-4">
               <ExclamationTriangleIcon class="w-8 h-8 text-red-500" />
            </div>
            <h3 class="text-xl font-bold text-white mb-2">Delete Role?</h3>
            <p class="text-interview-text-secondary mb-6">
              Are you sure you want to delete <strong class="text-white">{{ deletingRole.title }}</strong>? This action cannot be undone.
            </p>
            <div class="flex gap-3 w-full">
              <button 
                @click="cancelDelete"
                class="flex-1 px-4 py-2.5 rounded-xl border border-interview-surface-border text-interview-text-primary hover:bg-interview-surface-hover transition-colors font-medium"
              >
                Cancel
              </button>
              <button 
                @click="confirmDelete"
                :disabled="saving"
                class="flex-1 px-4 py-2.5 rounded-xl bg-red-500 text-white hover:bg-red-600 font-bold transition-colors disabled:opacity-50"
              >
                {{ saving ? 'Deleting...' : 'Delete' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Clean Toast -->
    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="transform translate-y-4 opacity-0"
      enter-to-class="transform translate-y-0 opacity-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="transform translate-y-0 opacity-100"
      leave-to-class="transform translate-y-4 opacity-0"
    >
      <div
        v-if="showToast"
        class="fixed bottom-6 right-6 px-6 py-4 bg-interview-surface/90 backdrop-blur-xl border border-interview-primary/30 text-white rounded-2xl shadow-2xl flex items-center gap-3 z-50"
      >
        <CheckCircleIcon class="w-6 h-6 text-interview-success" />
        <span class="font-medium">{{ toastMessage }}</span>
      </div>
    </Transition>

  </div>
</template>

<script setup lang="ts">
import {
  DocumentTextIcon,
  PencilSquareIcon,
  ClipboardDocumentIcon,
  TrashIcon,
  PlusIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ArrowLeftIcon,
  BriefcaseIcon,
  SparklesIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'; // Switched to outline for modern look

definePageMeta({
  layout: 'hr',
  middleware: ['hr']
})

const { getRoles, updateQuestions, deleteRole } = useHR();

interface Role {
  id: string;
  title: string;
  questionCount: number;
  questions: string[];
}

const roles = ref<Role[]>([]);
const loading = ref(true);
const saving = ref(false);
const showToast = ref(false);
const toastMessage = ref('');

// Edit state
const editingRole = ref<Role | null>(null);
const editingRoleTitle = ref('');
const editedQuestions = ref<string[]>([]);

// Delete state
const deletingRole = ref<Role | null>(null);

// Load roles with actual questions
const loadRoles = async () => {
  loading.value = true;
  try {
    const rolesData = await getRoles();

    // Filter out candidate specific roles
    const filteredRoles = rolesData.filter((role: any) => !role.title.includes('(Candidate'));
    
    // Load questions for each role (Optimized: questions now come from getRoles)
    const rolesWithQuestions = filteredRoles.map((role: any) => ({
      ...role,
      questions: (role.questions || []).map((q: any) => typeof q === 'string' ? q : q.content),
      questionCount: role.question_count || (role.questions ? role.questions.length : 0)
    }));
    
    roles.value = rolesWithQuestions as Role[];
  } catch (error) {
    console.error('Error loading roles:', error);
    showToastMessage('❌ Failed to load roles');
  } finally {
    loading.value = false;
  }
};

const startEdit = (role: Role) => {
  editingRole.value = role;
  editingRoleTitle.value = role.title;
  editedQuestions.value = [...role.questions];
};

const addQuestion = () => {
  editedQuestions.value.push('');
};

const removeQuestion = (index: number) => {
  if (editedQuestions.value.length > 1) {
    editedQuestions.value.splice(index, 1);
  }
};

const saveEdit = async () => {
  if (!editingRole.value) return;
  
  // Filter out empty questions
  const validQuestions = editedQuestions.value
    .map(q => q.trim())
    .filter(q => q !== '');
  
  const cleanTitle = editingRoleTitle.value.trim();

  if (cleanTitle === '') {
     showToastMessage('⚠️ Title cannot be empty');
     return;
  }
  
  if (validQuestions.length === 0) {
    showToastMessage('⚠️ Please add at least one question');
    return;
  }
  
  saving.value = true;
  try {
    await updateQuestions(editingRole.value.id, validQuestions, cleanTitle);
    showToastMessage('✅ Role updated successfully');
    editingRole.value = null;
    editedQuestions.value = [];
    editingRoleTitle.value = '';
    await loadRoles(); // Reload data
  } catch (error) {
    console.error('Error updating role:', error);
    showToastMessage('❌ Failed to update role');
  } finally {
    saving.value = false;
  }
};

const cancelEdit = () => {
  editingRole.value = null;
  editedQuestions.value = [];
};

const startDelete = (role: Role) => {
  deletingRole.value = role;
};

const confirmDelete = async () => {
  if (!deletingRole.value) return;
  
  saving.value = true;
  try {
    await deleteRole(deletingRole.value.id);
    showToastMessage(`✅ Deleted ${deletingRole.value.title}`);
    deletingRole.value = null;
    await loadRoles(); // Reload data
  } catch (error) {
    console.error('Error deleting role:', error);
    showToastMessage('❌ Failed to delete role');
  } finally {
    saving.value = false;
  }
};

const cancelDelete = () => {
  deletingRole.value = null;
};

const copyQuestions = (role: Role) => {
  const text = role.questions.map((q: string, i: number) => `${i + 1}. ${q}`).join('\n');
  navigator.clipboard.writeText(text);
  
  showToastMessage('✅ Questions copied to clipboard!');
};

const showToastMessage = (message: string) => {
  toastMessage.value = message;
  showToast.value = true;
  setTimeout(() => {
    showToast.value = false;
  }, 3000);
};

onMounted(loadRoles);
</script>

<style scoped>
.role-card {
  opacity: 0;
  transform: translate3d(0, 20px, 0);
  animation: role-fade-in 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: var(--delay, 0ms);
}

@keyframes role-fade-in {
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

