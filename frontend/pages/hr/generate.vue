<template>
  <div class="text-interview-text-primary p-8">
    <div class="max-w-4xl mx-auto">
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

      <h1 class="text-4xl font-bold mb-8 flex items-center gap-3 text-interview-text-primary">
        <CpuChipIcon class="w-10 h-10 text-interview-primary" />
        AI Question Generator
      </h1>

      <!-- Step 1: Input Form -->
      <div v-if="step === 1" class="bg-interview-surface backdrop-blur-xl p-8 rounded-2xl border border-interview-surface-border animate-fade-in-up">
        <h2 class="text-2xl font-semibold mb-6 text-interview-text-primary">Step 1: Input Job Details</h2>
        
        <form @submit.prevent="generateQuestions">
          <div class="mb-6">
            <label class="block text-sm font-medium mb-2 text-interview-text-secondary">Role Title</label>
            <input
              v-model="roleTitle"
              type="text"
              required
              placeholder="e.g., Frontend Developer, Sales Manager"
              class="w-full px-4 py-3 bg-interview-bg-secondary border border-interview-surface-border rounded-xl focus:outline-none focus:ring-2 focus:ring-interview-primary focus:border-transparent text-interview-text-primary placeholder-interview-text-muted"
            />
          </div>

          <div class="mb-6">
            <label class="block text-sm font-medium mb-2 text-interview-text-secondary">Job Description</label>
            <textarea
              v-model="jobDescription"
              required
              rows="8"
              placeholder="Paste the job description here..."
              class="w-full px-4 py-3 bg-interview-bg-secondary border border-interview-surface-border rounded-xl focus:outline-none focus:ring-2 focus:ring-interview-primary focus:border-transparent text-interview-text-primary placeholder-interview-text-muted resize-none"
            ></textarea>
          </div>

          <button
            type="submit"
            :disabled="isGenerating"
            class="w-full px-6 py-3 bg-interview-primary hover:bg-interview-primary-hover text-interview-bg rounded-xl font-semibold transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-glow-amber flex items-center justify-center gap-2"
          >
            <SparklesIcon v-if="!isGenerating" class="w-5 h-5" />
            <ArrowPathIcon v-else class="w-5 h-5 animate-spin" />
            {{ isGenerating ? 'Generating...' : 'Generate Questions with AI' }}
          </button>
        </form>
      </div>

      <!-- Step 2: Review Questions -->
      <div v-if="step === 2" class="bg-interview-surface backdrop-blur-xl p-8 rounded-2xl border border-interview-surface-border animate-fade-in-up">
        <h2 class="text-2xl font-semibold mb-6 text-interview-text-primary">Step 2: Review & Edit Questions</h2>
        
        <div class="space-y-4 mb-8">
          <div
            v-for="(question, index) in generatedQuestions"
            :key="index"
            class="bg-interview-bg-secondary p-4 rounded-xl border border-interview-surface-border"
          >
            <label class="block text-sm font-medium mb-2 text-interview-primary">Question {{ index + 1 }}</label>
            <textarea
              v-model="generatedQuestions[index]"
              rows="3"
              class="w-full px-4 py-3 bg-interview-surface border border-interview-surface-border rounded-xl focus:outline-none focus:ring-2 focus:ring-interview-primary focus:border-transparent text-interview-text-primary resize-none"
            ></textarea>
          </div>
        </div>

        <div class="flex gap-4">
          <button
            @click="step = 1"
            class="flex-1 px-6 py-3 bg-interview-surface border border-interview-surface-border hover:bg-interview-surface-hover text-interview-text-secondary hover:text-interview-text-primary rounded-xl font-semibold transition-all duration-300"
          >
            ← Back
          </button>
          <button
            @click="saveQuestionsToDb"
            :disabled="isSaving"
            class="flex-1 px-6 py-3 bg-interview-success hover:bg-green-600 text-white rounded-xl font-semibold transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <DocumentCheckIcon v-if="!isSaving" class="w-5 h-5" />
            <ArrowPathIcon v-else class="w-5 h-5 animate-spin" />
            {{ isSaving ? 'Saving...' : 'Save Questions' }}
          </button>
        </div>
      </div>

      <!-- Success Message -->
      <div v-if="step === 3" class="bg-interview-surface backdrop-blur-xl p-8 rounded-2xl text-center border border-interview-surface-border animate-fade-in-up">
        <div class="flex justify-center mb-4">
          <div class="p-4 bg-interview-success/20 rounded-full">
            <CheckCircleIcon class="w-16 h-16 text-interview-success animate-float" />
          </div>
        </div>
        <h2 class="text-3xl font-bold mb-4 text-interview-text-primary">Questions Saved Successfully!</h2>
        <p class="text-interview-text-secondary mb-8">The questions for "{{ roleTitle }}" have been saved to the database.</p>
        
        <div class="flex gap-4 justify-center">
          <button
            @click="resetForm"
            class="px-6 py-3 bg-interview-primary hover:bg-interview-primary-hover text-interview-bg rounded-xl font-semibold transition-all duration-300 shadow-glow-amber"
          >
            Generate More Questions
          </button>
          <NuxtLink
            to="/hr/roles"
            class="px-6 py-3 bg-interview-success hover:bg-green-600 text-white rounded-xl font-semibold transition-all duration-300 inline-block"
          >
            View All Roles
          </NuxtLink>
        </div>
      </div>

      <!-- Error Message -->
      <Transition
        enter-active-class="transition-all duration-300"
        enter-from-class="opacity-0 translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition-all duration-300"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 translate-y-2"
      >
        <div v-if="error" class="mt-4 p-4 bg-red-500/20 border border-red-500/30 rounded-xl">
          <p class="text-red-400">{{ error }}</p>
        </div>
      </Transition>
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
