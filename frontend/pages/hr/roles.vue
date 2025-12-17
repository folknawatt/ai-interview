<template>
  <div class="min-h-screen bg-minimal-bg text-minimal-text-primary p-8">
    <div class="max-w-6xl mx-auto">
      <div class="mb-6">
        <NuxtLink to="/hr/dashboard" class="text-minimal-info hover:text-sky-600">
          ← Back to Dashboard
        </NuxtLink>
      </div>

      <h1 class="text-4xl font-bold mb-8 flex items-center gap-3">
        <ClipboardDocumentListIcon class="w-10 h-10 text-minimal-info" />
        Manage Roles & Questions
      </h1>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin w-12 h-12 border-4 border-minimal-info border-t-transparent rounded-full mx-auto mb-4"></div>
        <p class="text-minimal-text-secondary">Loading roles...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="roles.length === 0" class="text-center py-12 bg-minimal-card rounded-xl border border-minimal-border">
        <div class="flex justify-center mb-4">
          <DocumentTextIcon class="w-16 h-16 text-minimal-text-muted" />
        </div>
        <h2 class="text-2xl font-semibold mb-2">No Roles Yet</h2>
        <p class="text-minimal-text-secondary mb-6">Start by generating some interview questions</p>
        <NuxtLink
          to="/hr/generate"
          class="inline-block px-6 py-3 bg-minimal-info hover:bg-sky-600 text-white rounded-lg font-semibold transition-all shadow-sm"
        >
          Generate Questions
        </NuxtLink>
      </div>

      <!-- Roles Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="role in roles"
          :key="role.id"
          class="bg-minimal-card p-6 rounded-xl border-2 border-minimal-border hover:border-minimal-info transition-colors"
        >
          <div class="flex items-start justify-between mb-4">
            <h3 class="text-xl font-bold">{{ role.title }}</h3>
            <span class="px-2 py-1 bg-sky-50 text-minimal-info border border-sky-200 rounded text-sm">
              {{ role.questionCount }} questions
            </span>
          </div>

          <div class="space-y-3 mb-6">
            <div
              v-for="(question, index) in role.questions"
              :key="index"
              class="p-3 bg-sky-50 border border-sky-100 rounded-lg text-sm text-minimal-text-primary"
            >
              <span class="font-semibold text-minimal-info">Q{{index + 1}}:</span>
              {{ question }}
           </div>
          </div>

          <div class="flex gap-2">
            <button
              @click="startEdit(role)"
              class="flex-1 px-4 py-2 bg-amber-500 hover:bg-amber-600 text-white rounded-lg text-sm transition-all flex items-center justify-center gap-1"
              title="Edit questions"
            >
              <PencilSquareIcon class="w-4 h-4" />
              Edit
            </button>
            <button
              @click="copyQuestions(role)"
              class="flex-1 px-4 py-2 bg-minimal-border hover:bg-slate-300 text-minimal-text-primary rounded-lg text-sm transition-all flex items-center justify-center gap-1"
              title="Copy to clipboard"
            >
              <ClipboardDocumentIcon class="w-4 h-4" />
              Copy
            </button>
            <button
              @click="startDelete(role)"
              class="px-4 py-2 bg-minimal-warning hover:bg-red-700 text-white rounded-lg text-sm transition-all flex items-center justify-center"
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
          class="inline-flex items-center gap-2 px-6 py-3 bg-minimal-success hover:bg-emerald-600 text-white rounded-lg font-semibold transition-all shadow-sm"
        >
          <PlusCircleIcon class="w-5 h-5" />
          Add New Role
        </NuxtLink>
      </div>

      <!-- Edit Modal -->
      <div v-if="editingRole" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="cancelEdit">
        <div class="bg-minimal-card p-8 rounded-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto m-4 border border-minimal-border">
          <h2 class="text-2xl font-bold mb-6 flex items-center gap-2">
            <PencilSquareIcon class="w-7 h-7 text-amber-500" />
            Edit Questions: {{ editingRole.title }}
          </h2>
          
          <div class="space-y-4 mb-6">
            <div v-for="(question, index) in editedQuestions" :key="index" class="flex gap-2">
              <textarea
                v-model="editedQuestions[index]"
                class="flex-1 bg-white border-2 border-minimal-border text-minimal-text-primary p-3 rounded-lg resize-none focus:ring-2 focus:ring-minimal-info"
                rows="2"
                placeholder="Enter question..."
              />
              <button
                @click="removeQuestion(index)"
                class="px-3 py-2 bg-minimal-warning hover:bg-red-700 text-white rounded-lg transition-all"
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
            class="w-full mb-4 px-4 py-2 bg-minimal-success hover:bg-emerald-600 text-white rounded-lg transition-all flex items-center justify-center gap-2"
          >
            <PlusCircleIcon class="w-5 h-5" />
            Add Question
          </button>
          
          <div class="flex gap-4">
            <button
              @click="cancelEdit"
              class="flex-1 px-4 py-2 bg-minimal-text-secondary hover:bg-minimal-text-primary text-white rounded-lg transition-all"
            >
              Cancel
            </button>
            <button
              @click="saveEdit"
              :disabled="saving"
              class="flex-1 px-4 py-2 bg-minimal-info hover:bg-sky-600 text-white rounded-lg transition-all disabled:opacity-50"
            >
              {{ saving ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Delete Confirmation Modal -->
      <div v-if="deletingRole" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="cancelDelete">
        <div class="bg-minimal-card p-8 rounded-xl max-w-md w-full m-4 border border-minimal-border">
          <h2 class="text-2xl font-bold mb-4 flex items-center gap-2">
            <ExclamationTriangleIcon class="w-7 h-7 text-minimal-warning" />
            Confirm Delete
          </h2>
          <p class="text-minimal-text-secondary mb-6">
            Are you sure you want to delete <strong class="text-minimal-text-primary">{{ deletingRole.title }}</strong>?
            This action cannot be undone.
          </p>
          
          <div class="flex gap-4">
            <button
              @click="cancelDelete"
              class="flex-1 px-4 py-2 bg-minimal-text-secondary hover:bg-minimal-text-primary text-white rounded-lg transition-all"
            >
              Cancel
            </button>
            <button
              @click="confirmDelete"
              :disabled="saving"
              class="flex-1 px-4 py-2 bg-minimal-warning hover:bg-red-700 text-white rounded-lg transition-all disabled:opacity-50"
            >
              {{ saving ? 'Deleting...' : 'Delete' }}
            </button>
          </div>
        </div>
      </div>

      <!--Toast Notification -->
      <div
        v-if="showToast"
        class="fixed bottom-4 right-4 px-6 py-3 bg-minimal-success text-white rounded-lg shadow-lg animate-fade-in"
      >
        {{ toastMessage }}
      </div>
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

const roles = ref<any[]>([]);
const loading = ref(true);
const saving = ref(false);
const showToast = ref(false);
const toastMessage = ref('');

// Edit state
const editingRole = ref<any>(null);
const editedQuestions = ref<string[]>([]);

// Delete state
const deletingRole = ref<any>(null);

// Load roles with actual questions
const loadRoles = async () => {
  loading.value = true;
  try {
    const rolesData = await getRoles();
    
    // Load questions for each role
    const rolesWithQuestions = await Promise.all(
      rolesData.map(async (role) => {
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
    
    roles.value = rolesWithQuestions;
  } catch (error) {
    console.error('Error loading roles:', error);
    showToastMessage('❌ Failed to load roles');
  } finally {
    loading.value = false;
  }
};

const startEdit = (role: any) => {
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

const startDelete = (role: any) => {
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

const copyQuestions = (role: any) => {
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
