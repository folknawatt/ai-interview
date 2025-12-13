<template>
  <div
    class="min-h-screen bg-minimal-bg text-minimal-text-primary flex flex-col items-center justify-center p-4"
  >
    <div
      class="w-full max-w-md bg-minimal-card p-8 rounded-lg shadow-sm border border-minimal-border text-center"
    >
      <h1 class="text-3xl font-bold mb-2 flex items-center justify-center gap-2">
        <HandRaisedIcon class="w-8 h-8 text-minimal-info" />
        ยินดีต้อนรับ
      </h1>
      <p class="text-minimal-text-secondary mb-8">เข้าสู่ระบบสัมภาษณ์งานอัตโนมัติ</p>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div>
          <label class="block text-left text-sm font-medium mb-2 text-minimal-text-primary"
            >ชื่อ-นามสกุล ของคุณ</label
          >
          <input
            v-model="name"
            type="text"
            placeholder="กรอกชื่อของคุณ..."
            autofocus
            required
            class="w-full px-4 py-3 bg-white border-2 border-minimal-border rounded-lg focus:outline-none focus:ring-2 focus:ring-minimal-info focus:border-transparent text-minimal-text-primary placeholder-minimal-text-muted transition-all"
          />
        </div>

        <button
          type="submit"
          :disabled="!name.trim()"
          class="w-full px-6 py-3 text-lg font-semibold text-white bg-minimal-info rounded-lg hover:bg-sky-600 focus:outline-none focus:ring-2 focus:ring-minimal-info focus:ring-offset-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
        >
          เริ่มการสัมภาษณ์ (Start Interview)
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { HandRaisedIcon } from '@heroicons/vue/24/solid';

const { setCandidateName } = useInterview();
const router = useRouter();
const name = ref("");

const handleSubmit = () => {
  if (name.value.trim()) {
    setCandidateName(name.value);
    router.push("/role-selection");
  }
};
</script>
