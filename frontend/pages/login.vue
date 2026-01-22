<template>
  <div class="min-h-screen bg-interview-bg text-interview-text-primary flex flex-col items-center justify-center p-4 relative overflow-hidden">
    <!-- Background gradient effects -->
    <div class="absolute inset-0 bg-gradient-to-br from-interview-bg via-interview-bg-secondary to-interview-bg-gradient"></div>
    <div class="absolute top-1/4 -left-32 w-96 h-96 bg-interview-primary/10 rounded-full blur-3xl"></div>
    <div class="absolute bottom-1/4 -right-32 w-96 h-96 bg-interview-primary/5 rounded-full blur-3xl"></div>

    <!-- Login Card -->
    <div
      class="relative w-full max-w-md bg-interview-surface backdrop-blur-xl p-8 rounded-2xl border border-interview-surface-border shadow-glass animate-fade-in-up"
    >
      <h1 class="text-3xl font-bold mb-2 flex items-center justify-center gap-3 text-interview-text-primary">
        <HandRaisedIcon class="w-8 h-8 text-interview-primary" />
        ยินดีต้อนรับ
      </h1>
      <p class="text-interview-text-secondary mb-8 text-center">เข้าสู่ระบบสัมภาษณ์งานอัตโนมัติ</p>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div>
          <label class="block text-left text-sm font-medium mb-2 text-interview-text-secondary"
            >ชื่อ-นามสกุล ของคุณ</label
          >
          <input
            v-model="name"
            type="text"
            placeholder="กรอกชื่อของคุณ..."
            autofocus
            required
            class="w-full px-4 py-3 bg-interview-surface border border-interview-surface-border rounded-xl focus:outline-none focus:ring-2 focus:ring-interview-primary focus:border-transparent text-interview-text-primary placeholder-interview-text-muted transition-all backdrop-blur-sm"
          />
        </div>

        <div>
           <label class="block text-left text-sm font-medium mb-2 text-interview-text-secondary"
            >อีเมล (Email)</label
          >
          <input
            v-model="email"
            type="email"
            placeholder="example@email.com"
            required
            class="w-full px-4 py-3 bg-interview-surface border border-interview-surface-border rounded-xl focus:outline-none focus:ring-2 focus:ring-interview-primary focus:border-transparent text-interview-text-primary placeholder-interview-text-muted transition-all backdrop-blur-sm"
          />
        </div>

        <button
          type="submit"
          :disabled="!name.trim() || !email.trim()"
          class="w-full px-6 py-3.5 text-lg font-semibold text-interview-bg bg-interview-primary rounded-xl hover:bg-interview-primary-hover focus:outline-none focus:ring-2 focus:ring-interview-primary focus:ring-offset-2 focus:ring-offset-interview-bg transition-all duration-300 disabled:opacity-40 disabled:cursor-not-allowed shadow-glow-amber hover:shadow-glow-amber-lg"
        >
          เริ่มการสัมภาษณ์ (Start Interview)
        </button>
      </form>
    </div>

    <!-- Footer text -->
    <p class="mt-8 text-interview-text-muted text-sm animate-fade-in">
      Powered by AI Interview Platform
    </p>
  </div>
</template>

<script setup lang="ts">
import { HandRaisedIcon } from '@heroicons/vue/24/solid';

const { setCandidateInfo } = useInterview();
const router = useRouter();
const name = ref("");
const email = ref("");

const handleSubmit = () => {
  if (name.value.trim() && email.value.trim()) {
    setCandidateInfo(name.value, email.value);
    router.push("/role-selection");
  }
};
</script>
