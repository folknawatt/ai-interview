<template>
  <div class="relative min-h-[80vh] flex flex-col items-center justify-center p-6 z-10">
    <!-- Ambient Background Elements -->
    <div class="fixed inset-0 z-0 pointer-events-none">
      <div class="absolute top-0 right-0 w-[500px] h-[500px] bg-interview-accent-sky/10 rounded-full blur-[100px] animate-pulse"></div>
      <div class="absolute bottom-0 left-0 w-[300px] h-[300px] bg-interview-primary/5 rounded-full blur-[80px]"></div>
    </div>

    <div class="w-full max-w-3xl opacity-0 animate-fade-in-up" style="animation-delay: 0ms">
      <!-- Nav -->
      <div class="mb-8">
        <NuxtLink 
          to="/hr/dashboard" 
          class="inline-flex items-center gap-2 text-interview-text-secondary hover:text-white transition-colors mb-4 group"
        >
          <ArrowLeftIcon class="w-4 h-4 transition-transform group-hover:-translate-x-1" />
          Back to Dashboard
        </NuxtLink>
        <div class="flex items-center justify-between">
          <h1 class="text-4xl font-black tracking-tight text-white flex items-center gap-3">
            <SparklesIcon class="w-8 h-8 text-interview-primary animate-pulse" />
            AI Generator
          </h1>
          <!-- Step Indicators -->
          <div class="flex items-center gap-2">
             <div class="h-2 w-8 rounded-full transition-all duration-500" :class="step >= 1 ? 'bg-interview-primary' : 'bg-interview-surface-border'"></div>
             <div class="h-2 w-8 rounded-full transition-all duration-500" :class="step >= 2 ? 'bg-interview-primary' : 'bg-interview-surface-border'"></div>
             <div class="h-2 w-8 rounded-full transition-all duration-500" :class="step >= 3 ? 'bg-interview-success' : 'bg-interview-surface-border'"></div>
          </div>
        </div>
      </div>

      <!-- Main Console Card -->
      <div class="relative bg-interview-surface backdrop-blur-xl border border-interview-surface-border rounded-3xl overflow-hidden shadow-2xl transition-all duration-500">
        
        <!-- Step 1: Input Form -->
        <div v-if="step === 1" class="p-8 animate-fade-in">
          <div class="mb-6">
            <h2 class="text-2xl font-bold text-white mb-2">Define The Role</h2>
            <p class="text-interview-text-secondary">Provide the job details so our AI can craft the perfect interview questions.</p>
          </div>
          
          <form @submit.prevent="generateQuestions">
            <div class="mb-6 space-y-2">
              <label class="block text-sm font-bold text-interview-text-primary uppercase tracking-wider">Role Title</label>
              <div class="relative group">
                <input
                  v-model="roleTitle"
                  type="text"
                  required
                  placeholder="e.g. Senior Frontend Engineer"
                  class="w-full px-5 py-4 bg-interview-bg-secondary/50 border border-interview-surface-border rounded-xl focus:outline-none focus:border-interview-primary focus:ring-1 focus:ring-interview-primary text-white placeholder-interview-text-muted transition-all group-hover:border-interview-surface-border/80"
                />
                <BriefcaseIcon class="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-interview-text-muted" />
              </div>
            </div>

            <div class="mb-8 space-y-2">
              <label class="block text-sm font-bold text-interview-text-primary uppercase tracking-wider">Job Description</label>
              <div class="relative group">
                <textarea
                  v-model="jobDescription"
                  required
                  rows="6"
                  placeholder="Paste the full job description here (responsibilities, requirements, etc.)..."
                  class="w-full px-5 py-4 bg-interview-bg-secondary/50 border border-interview-surface-border rounded-xl focus:outline-none focus:border-interview-primary focus:ring-1 focus:ring-interview-primary text-white placeholder-interview-text-muted resize-none transition-all group-hover:border-interview-surface-border/80 custom-scrollbar"
                ></textarea>
              </div>
            </div>

            <button
              type="submit"
              :disabled="isGenerating"
              class="w-full px-6 py-4 bg-gradient-to-r from-interview-primary to-interview-primary-hover text-interview-bg rounded-xl font-bold text-lg transition-all duration-300 disabled:opacity-70 disabled:cursor-not-allowed shadow-glow-amber hover:shadow-glow-amber-lg transform hover:-translate-y-0.5 flex items-center justify-center gap-3"
            >
              <span v-if="!isGenerating" class="flex items-center gap-2">
                <CpuChipIcon class="w-6 h-6" />
                Generate Questions
              </span>
              <span v-else class="flex items-center gap-2">
                <ArrowPathIcon class="w-6 h-6 animate-spin" />
                Processing with AI...
              </span>
            </button>
          </form>
        </div>

        <!-- Step 2: Review Questions -->
        <div v-if="step === 2" class="p-8 animate-fade-in">
          <div class="flex items-center justify-between mb-6">
            <div>
              <h2 class="text-2xl font-bold text-white mb-1">Review Questions</h2>
              <p class="text-interview-text-secondary">AI has generated {{ generatedQuestions.length }} questions. Review and refine them below.</p>
            </div>
            <div class="hidden sm:block text-xs font-mono text-interview-primary bg-interview-primary/10 px-2 py-1 rounded">
               AI_CONFIDENCE: HIGH
            </div>
          </div>
          
          <div class="space-y-4 mb-8 max-h-[60vh] overflow-y-auto custom-scrollbar pr-2 -mr-2 pl-1">
            <TransitionGroup name="list">
              <div
                v-for="(question, index) in generatedQuestions"
                :key="index"
                class="group relative bg-interview-bg-secondary/50 p-5 rounded-2xl border border-interview-surface-border hover:border-interview-primary/50 focus-within:border-interview-primary/80 focus-within:bg-interview-bg-secondary focus-within:shadow-lg transition-all duration-300"
              >
                <!-- Question Number & Delete -->
                <div class="flex items-center justify-between mb-3">
                   <span class="text-xs font-black text-interview-primary/80 uppercase tracking-widest bg-interview-primary/10 px-2 py-1 rounded">
                     Question {{ index + 1 }}
                   </span>
                   <button 
                     @click="removeGeneratedQuestion(index)"
                     class="text-interview-text-muted hover:text-red-400 p-1 rounded-lg hover:bg-red-500/10 transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100"
                     title="Remove Question"
                   >
                     <TrashIcon class="w-4 h-4" />
                   </button>
                </div>
                
                <!-- Editable Text Area -->
                <textarea
                  v-model="generatedQuestions[index]"
                  rows="3"
                  class="w-full bg-transparent border-none p-0 text-white placeholder-interview-text-muted focus:ring-0 resize-y leading-relaxed text-base"
                  placeholder="Enter interview question..."
                ></textarea>
              </div>
            </TransitionGroup>

            <!-- Add Question Button -->
            <button 
              @click="addGeneratedQuestion"
              class="w-full py-4 border-2 border-dashed border-interview-surface-border rounded-xl text-interview-text-secondary hover:text-interview-primary hover:border-interview-primary/50 hover:bg-interview-surface transition-all flex items-center justify-center gap-2 group"
            >
              <PlusIcon class="w-5 h-5 transition-transform group-hover:rotate-90" />
              Add Another Question
            </button>
          </div>

          <!-- Actions -->
          <div class="flex flex-col sm:flex-row gap-4 pt-6 border-t border-interview-surface-border">
            <button
              @click="step = 1"
              class="px-6 py-3 rounded-xl border border-interview-surface-border text-interview-text-secondary hover:text-white hover:bg-interview-surface-hover transition-colors font-medium"
            >
              Back to Edit
            </button>
            <button
              @click="saveQuestionsToDb"
              :disabled="isSaving || generatedQuestions.length === 0"
              class="flex-1 px-6 py-3 bg-interview-success text-white rounded-xl font-bold transition-all hover:bg-green-500 shadow-glow-green disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 transform active:scale-95"
            >
              <span v-if="!isSaving" class="flex items-center gap-2">
                <CheckCircleIcon class="w-5 h-5" />
                Approve & Save ({{ generatedQuestions.length }})
              </span>
              <span v-else class="flex items-center gap-2">
                <ArrowPathIcon class="w-5 h-5 animate-spin" />
                Saving...
              </span>
            </button>
          </div>
        </div>

        <!-- Success Message -->
        <div v-if="step === 3" class="p-12 text-center animate-fade-in flex flex-col items-center">
          <div class="w-24 h-24 bg-interview-success/10 rounded-full flex items-center justify-center mb-6 animate-bounce-slow">
            <CheckCircleIcon class="w-12 h-12 text-interview-success" />
          </div>
          <h2 class="text-3xl font-black text-white mb-4">Mission Complete!</h2>
          <p class="text-interview-text-secondary mb-8 text-lg max-w-md mx-auto">
            The interview questions for <strong class="text-white">{{ roleTitle }}</strong> have been successfully saved to the database.
          </p>
          
          <div class="flex flex-col sm:flex-row gap-4 w-full max-w-md">
            <button
              @click="resetForm"
              class="flex-1 px-6 py-3 bg-interview-surface border border-interview-surface-border hover:bg-interview-surface-hover text-white rounded-xl font-bold transition-all"
            >
              Generate More
            </button>
            <NuxtLink
              to="/hr/roles"
              class="flex-1 px-6 py-3 bg-interview-primary text-interview-bg hover:bg-interview-primary-hover rounded-xl font-bold transition-all shadow-glow-amber text-center"
            >
              View Roles
            </NuxtLink>
          </div>
        </div>

      </div>

      <!-- Error Message -->
      <Transition
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="opacity-0 translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 translate-y-2"
      >
        <div v-if="error" class="mt-6 p-4 bg-red-500/10 border border-red-500/30 rounded-xl flex items-center gap-3">
          <ExclamationTriangleIcon class="w-6 h-6 text-red-500 flex-shrink-0" />
          <p class="text-red-400 font-medium">{{ error }}</p>
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
  CheckCircleIcon,
  ArrowLeftIcon,
  ExclamationTriangleIcon,
  BriefcaseIcon,
  TrashIcon,
  PlusIcon
} from '@heroicons/vue/24/outline';

definePageMeta({
  layout: 'hr',
  middleware: ['hr']
})

const { generateQuestions: generateQuestionsAPI, saveQuestions } = useHR();

const step = ref(1);
const roleTitle = ref('');
const jobDescription = ref('');
const generatedQuestions = ref<string[]>([]);
const isGenerating = ref(false);
const isSaving = ref(false);
const error = ref('');

const removeGeneratedQuestion = (index: number) => {
  generatedQuestions.value.splice(index, 1);
};

const addGeneratedQuestion = () => {
  generatedQuestions.value.push('');
};

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

<style scoped>

.animate-bounce-slow {
  animation: bounce-slow 3s infinite;
}

@keyframes bounce-slow {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}
</style>

