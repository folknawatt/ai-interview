<template>
  <div class="min-h-screen bg-minimal-bg text-minimal-text-primary p-8">
    <div class="max-w-4xl mx-auto">
      <div class="mb-6">
        <NuxtLink to="/hr/dashboard" class="text-minimal-info hover:text-sky-600">
          ← Back to Dashboard
        </NuxtLink>
      </div>

      <h1 class="text-4xl font-bold mb-8 flex items-center gap-3">
        <CpuChipIcon class="w-10 h-10 text-minimal-info" />
        AI Question Generator
      </h1>

      <!-- Step 1: Input Form -->
      <div v-if="step === 1" class="bg-minimal-card p-8 rounded-xl border border-minimal-border">
        <h2 class="text-2xl font-semibold mb-6">Step 1: Input Job Details</h2>
        
        <form @submit.prevent="generateQuestions">
          <div class="mb-6">
            <label class="block text-sm font-medium mb-2">Role Title</label>
            <input
              v-model="roleTitle"
              type="text"
              required
              placeholder="e.g., Frontend Developer, Sales Manager"
              class="w-full px-4 py-3 bg-white border-2 border-minimal-border rounded-lg focus:outline-none focus:ring-2 focus:ring-minimal-info text-minimal-text-primary"
            />
          </div>

          <div class="mb-6">
            <label class="block text-sm font-medium mb-2">Job Description</label>
            <textarea
              v-model="jobDescription"
              required
              rows="8"
              placeholder="Paste the job description here..."
              class="w-full px-4 py-3 bg-white border-2 border-minimal-border rounded-lg focus:outline-none focus:ring-2 focus:ring-minimal-info text-minimal-text-primary"
            ></textarea>
          </div>

          <button
            type="submit"
            :disabled="isGenerating"
            class="w-full px-6 py-3 bg-minimal-info hover:bg-sky-600 text-white rounded-lg font-semibold transition-all disabled:bg-minimal-border disabled:cursor-not-allowed shadow-sm flex items-center justify-center gap-2"
          >
            <SparklesIcon v-if="!isGenerating" class="w-5 h-5" />
            <ArrowPathIcon v-else class="w-5 h-5 animate-spin" />
            {{ isGenerating ? 'Generating...' : 'Generate Questions with AI' }}
          </button>
        </form>
      </div>

      <!-- Step 2: Review Questions -->
      <div v-if="step === 2" class="bg-minimal-card p-8 rounded-xl border border-minimal-border">
        <h2 class="text-2xl font-semibold mb-6">Step 2: Review & Edit Questions</h2>
        
        <div class="space-y-4 mb-8">
          <div
            v-for="(question, index) in generatedQuestions"
            :key="index"
            class="bg-sky-50 p-4 rounded-lg border border-sky-200"
          >
            <label class="block text-sm font-medium mb-2 text-minimal-text-primary">Question {{ index + 1 }}</label>
            <textarea
              v-model="generatedQuestions[index]"
              rows="3"
              class="w-full px-4 py-3 bg-white border-2 border-minimal-border rounded-lg focus:outline-none focus:ring-2 focus:ring-minimal-info text-minimal-text-primary"
            ></textarea>
          </div>
        </div>

        <div class="flex gap-4">
          <button
            @click="step = 1"
            class="flex-1 px-6 py-3 bg-minimal-text-secondary hover:bg-minimal-text-primary text-white rounded-lg font-semibold transition-all"
          >
            ← Back
          </button>
          <button
            @click="saveQuestionsToDb"
            :disabled="isSaving"
            class="flex-1 px-6 py-3 bg-minimal-success hover:bg-emerald-600 text-white rounded-lg font-semibold transition-all disabled:bg-minimal-border disabled:cursor-not-allowed shadow-sm flex items-center justify-center gap-2"
          >
            <DocumentCheckIcon v-if="!isSaving" class="w-5 h-5" />
            <ArrowPathIcon v-else class="w-5 h-5 animate-spin" />
            {{ isSaving ? 'Saving...' : 'Save Questions' }}
          </button>
        </div>
      </div>

      <!-- Success Message -->
      <div v-if="step === 3" class="bg-minimal-card p-8 rounded-xl text-center border border-minimal-border">
        <div class="flex justify-center mb-4">
          <CheckCircleIcon class="w-20 h-20 text-minimal-success" />
        </div>
        <h2 class="text-3xl font-bold mb-4">Questions Saved Successfully!</h2>
        <p class="text-minimal-text-secondary mb-8">The questions for "{{ roleTitle }}" have been saved to the database.</p>
        
        <div class="flex gap-4 justify-center">
          <button
            @click="resetForm"
            class="px-6 py-3 bg-minimal-info hover:bg-sky-600 text-white rounded-lg font-semibold transition-all shadow-sm"
          >
            Generate More Questions
          </button>
          <NuxtLink
            to="/hr/roles"
            class="px-6 py-3 bg-minimal-success hover:bg-emerald-600 text-white rounded-lg font-semibold transition-all inline-block shadow-sm"
          >
            View All Roles
          </NuxtLink>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="mt-4 p-4 bg-red-50 border-2 border-red-200 rounded-lg">
        <p class="text-red-600">{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  CpuChipIcon,
  SparklesIcon,
  ArrowPathIcon,
  DocumentCheckIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/solid';

const { generateQuestions: generateQuestionsAPI, saveQuestions } = useHR();

const step = ref(1);
const roleTitle = ref('');
const jobDescription = ref('');
const generatedQuestions = ref<string[]>([]);
const isGenerating = ref(false);
const isSaving = ref(false);
const error = ref('');

const generateQuestions = async () => {
  isGenerating.value = true;
  error.value = '';

  try {
    const response = await generateQuestionsAPI(roleTitle.value, jobDescription.value);
    generatedQuestions.value = response.suggested_questions;
    step.value = 2;
  } catch (err: any) {
    error.value = err.message || 'Failed to generate questions';
  } finally {
    isGenerating.value = false;
  }
};

const saveQuestionsToDb = async () => {
  isSaving.value = true;
  error.value = '';

  try {
    // Generate role ID from title
    const roleId = roleTitle.value.toLowerCase().replace(/\s+/g, '_');
    
    // Convert Vue Proxy to plain array - handle both array and object formats
    let questionsArray: string[] = Array.isArray(generatedQuestions.value) 
      ? [...generatedQuestions.value]
      : Object.values(generatedQuestions.value) as string[];
    
    // Flatten nested arrays if they exist (AI might return [[q1, q2, q3]] instead of [q1, q2, q3])
    questionsArray = questionsArray.flat(Infinity) as string[];
    
    // Ensure all elements are strings
    questionsArray = questionsArray.map(q => String(q));
    
    console.log('Saving questions:', { roleId, roleTitle: roleTitle.value, questions: questionsArray });
    
    const response = await saveQuestions(roleId, roleTitle.value, questionsArray);
    console.log('Save response:', response);
    
    step.value = 3;
  } catch (err: any) {
    console.error('Save questions error:', err);
    
    // Ensure error message is always a string
    if (err && typeof err === 'object') {
      if (typeof err.message === 'string') {
        error.value = err.message;
      } else if (err.message && typeof err.message === 'object') {
        error.value = JSON.stringify(err.message);
      } else {
        error.value = err.toString() || 'Failed to save questions';
      }
    } else if (typeof err === 'string') {
      error.value = err;
    } else {
      error.value = 'Failed to save questions';
    }
    
    console.error('Error value set to:', error.value);
  } finally {
    isSaving.value = false;
  }
};

const resetForm = () => {
  step.value = 1;
  roleTitle.value = '';
  jobDescription.value = '';
  generatedQuestions.value = [];
  error.value = '';
};
</script>
