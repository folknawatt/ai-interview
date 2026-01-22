<template>
  <div class="min-h-screen text-interview-text-primary p-8">
    <div class="max-w-6xl mx-auto">
      <div class="mb-6">
        <NuxtLink 
          to="/hr/dashboard" 
          class="inline-flex items-center gap-2 px-4 py-2 text-interview-text-secondary hover:text-interview-text-primary hover:bg-interview-surface rounded-xl transition-all duration-300 -ml-4"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Back to Dashboard
        </NuxtLink>
      </div>

      <h1 class="text-4xl font-bold mb-8 flex items-center gap-3 text-interview-text-primary animate-fade-in-up">
        <ClipboardDocumentListIcon class="w-10 h-10 text-interview-primary" />
        Manage Roles & Questions
      </h1>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin w-12 h-12 border-4 border-interview-primary border-t-transparent rounded-full mx-auto mb-4"></div>
        <p class="text-interview-text-secondary">Loading roles...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="roles.length === 0" class="text-center py-12 bg-interview-surface backdrop-blur-xl rounded-2xl border border-interview-surface-border animate-fade-in-up">
        <div class="flex justify-center mb-4">
          <DocumentTextIcon class="w-16 h-16 text-interview-text-muted" />
        </div>
        <h2 class="text-2xl font-semibold mb-2 text-interview-text-primary">No Roles Yet</h2>
        <p class="text-interview-text-secondary mb-6">Start by generating some interview questions</p>
        <NuxtLink
          to="/hr/generate"
          class="inline-block px-6 py-3 bg-interview-primary hover:bg-interview-primary-hover text-interview-bg rounded-xl font-semibold transition-all shadow-glow-amber"
        >
          Generate Questions
        </NuxtLink>
      </div>

      <!-- Roles Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="(role, roleIndex) in roles"
          :key="role.id"
          class="role-card bg-interview-surface backdrop-blur-xl p-6 rounded-2xl border border-interview-surface-border hover:border-interview-primary/50 hover:shadow-lg hover:scale-[1.02] transition-all duration-300"
          :style="{ '--delay': `${roleIndex * 80}ms` }"
        >
          <div class="flex items-start justify-between mb-4">
            <h3 class="text-xl font-bold text-interview-text-primary">{{ role.title }}</h3>
            <span class="px-3 py-1 bg-interview-primary/20 text-interview-primary border border-interview-primary/30 rounded-full text-sm">
              {{ role.questionCount }} questions
            </span>
          </div>

          <div class="space-y-3 mb-6">
            <div
              v-for="(question, index) in role.questions"
              :key="index"
              class="p-3 bg-interview-bg-secondary border border-interview-surface-border rounded-xl text-sm text-interview-text-secondary"
            >
              <span class="font-semibold text-interview-primary">Q{{index + 1}}:</span>
              {{ question }}
           </div>
          </div>

          <div class="flex gap-2">
            <button
              @click="startEdit(role)"
              class="flex-1 px-4 py-2 bg-interview-primary hover:bg-interview-primary-hover text-interview-bg rounded-xl text-sm transition-all duration-300 flex items-center justify-center gap-1"
              title="Edit questions"
            >
              <PencilSquareIcon class="w-4 h-4" />
              Edit
            </button>
            <button
              @click="copyQuestions(role)"
              class="flex-1 px-4 py-2 bg-interview-surface border border-interview-surface-border hover:bg-interview-surface-hover text-interview-text-primary rounded-xl text-sm transition-all duration-300 flex items-center justify-center gap-1"
              title="Copy to clipboard"
            >
              <ClipboardDocumentIcon class="w-4 h-4" />
              Copy
            </button>
            <button
              @click="startDelete(role)"
              class="px-4 py-2 bg-red-500/20 hover:bg-red-500 text-red-400 hover:text-white rounded-xl text-sm transition-all duration-300 flex items-center justify-center"
              title="Delete role"
            >
              <TrashIcon class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      <!-- Add New Role Button -->
      <div v-if="!loading && roles.length > 0" class="mt-8 text-center">
        <NuxtLink
          to="/hr/generate"
          class="inline-flex items-center gap-2 px-6 py-3 bg-interview-success hover:bg-green-600 text-white rounded-xl font-semibold transition-all shadow-sm"
        >
          <PlusCircleIcon class="w-5 h-5" />
          Add New Role
        </NuxtLink>
      </div>

      <!-- Edit Modal -->
      <Transition
        enter-active-class="transition-all duration-300"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-all duration-300"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div v-if="editingRole" class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50" @click.self="cancelEdit">
          <div class="bg-interview-bg-secondary p-8 rounded-2xl max-w-2xl w-full max-h-[80vh] overflow-y-auto m-4 border border-interview-surface-border animate-fade-in-up">
            <h2 class="text-2xl font-bold mb-6 flex items-center gap-2 text-interview-text-primary">
              <PencilSquareIcon class="w-7 h-7 text-interview-primary" />
              Edit Questions: {{ editingRole.title }}
            </h2>
            
            <div class="space-y-4 mb-6">
              <div v-for="(question, index) in editedQuestions" :key="index" class="flex gap-2">
                <textarea
                  v-model="editedQuestions[index]"
                  class="flex-1 bg-interview-surface border border-interview-surface-border text-interview-text-primary p-3 rounded-xl resize-none focus:ring-2 focus:ring-interview-primary focus:border-transparent"
                  rows="2"
                  placeholder="Enter question..."
                />
                <button
                  @click="removeQuestion(index)"
                  class="px-3 py-2 bg-red-500/20 hover:bg-red-500 text-red-400 hover:text-white rounded-xl transition-all duration-300"
                  title="Remove question"
                  :disabled="editedQuestions.length === 1"
                  :class="{ 'opacity-50 cursor-not-allowed': editedQuestions.length === 1 }"
                >
                  <TrashIcon class="w-5 h-5" />
                </button>
              </div>
            </div>
            
            <button
              @click="addQuestion"
              class="w-full mb-4 px-4 py-2 bg-interview-success hover:bg-green-600 text-white rounded-xl transition-all duration-300 flex items-center justify-center gap-2"
            >
              <PlusCircleIcon class="w-5 h-5" />
              Add Question
            </button>
            
            <div class="flex gap-4">
              <button
                @click="cancelEdit"
                class="flex-1 px-4 py-2 bg-interview-surface border border-interview-surface-border hover:bg-interview-surface-hover text-interview-text-secondary hover:text-interview-text-primary rounded-xl transition-all duration-300"
              >
                Cancel
              </button>
              <button
                @click="saveEdit"
                :disabled="saving"
                class="flex-1 px-4 py-2 bg-interview-primary hover:bg-interview-primary-hover text-interview-bg rounded-xl transition-all duration-300 disabled:opacity-50"
              >
                {{ saving ? 'Saving...' : 'Save Changes' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>

      <!-- Delete Confirmation Modal -->
      <Transition
        enter-active-class="transition-all duration-300"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-all duration-300"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div v-if="deletingRole" class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50" @click.self="cancelDelete">
          <div class="bg-interview-bg-secondary p-8 rounded-2xl max-w-md w-full m-4 border border-interview-surface-border animate-fade-in-up">
            <h2 class="text-2xl font-bold mb-4 flex items-center gap-2 text-interview-text-primary">
              <ExclamationTriangleIcon class="w-7 h-7 text-red-400" />
              Confirm Delete
            </h2>
            <p class="text-interview-text-secondary mb-6">
              Are you sure you want to delete <strong class="text-interview-text-primary">{{ deletingRole.title }}</strong>?
              This action cannot be undone.
            </p>
            
            <div class="flex gap-4">
              <button
                @click="cancelDelete"
                class="flex-1 px-4 py-2 bg-interview-surface border border-interview-surface-border hover:bg-interview-surface-hover text-interview-text-secondary hover:text-interview-text-primary rounded-xl transition-all duration-300"
              >
                Cancel
              </button>
              <button
                @click="confirmDelete"
                :disabled="saving"
                class="flex-1 px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-xl transition-all duration-300 disabled:opacity-50"
              >
                {{ saving ? 'Deleting...' : 'Delete' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>

      <!--Toast Notification -->
      <Transition
        enter-active-class="transition-all duration-300"
        enter-from-class="opacity-0 translate-y-4"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition-all duration-300"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 translate-y-4"
      >
        <div
          v-if="showToast"
          class="fixed bottom-4 right-4 px-6 py-3 bg-interview-success text-white rounded-xl shadow-lg"
        >
          {{ toastMessage }}
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  ClipboardDocumentListIcon,
  DocumentTextIcon,
  PencilSquareIcon,
  ClipboardDocumentIcon,
  TrashIcon,
  PlusCircleIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  XCircleIcon
} from '@heroicons/vue/24/solid';

const { getRoles, getRoleDetails, updateQuestions, deleteRole } = useHR();

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
    
    // Load questions for each role
    const rolesWithQuestions = await Promise.all(
      filteredRoles.map(async (role) => {
        try {
          const details = await getRoleDetails(role.id) as { questions: string[] };
          return {
            ...role,
            questions: details.questions,
            questionCount: details.questions.length
          };
        } catch (error) {
          console.error(`Error loading details for role ${role.id}:`, error);
          return {
            ...role,
            questions: [],
            questionCount: 0
          };
        }
      })
    );
    

    
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
  
  if (validQuestions.length === 0) {
    showToastMessage('⚠️ Please add at least one question');
    return;
  }
  
  saving.value = true;
  try {
    await updateQuestions(editingRole.value.id, validQuestions);
    showToastMessage('✅ Questions updated successfully');
    editingRole.value = null;
    editedQuestions.value = [];
    await loadRoles(); // Reload data
  } catch (error) {
    console.error('Error updating questions:', error);
    showToastMessage('❌ Failed to update questions');
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
