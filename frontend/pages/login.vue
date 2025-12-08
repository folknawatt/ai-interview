<template>
  <div
    class="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-4"
  >
    <div
      class="w-full max-w-md bg-gray-800 p-8 rounded-lg shadow-lg text-center"
    >
      <h1 class="text-3xl font-bold mb-2">👋 ยินดีต้อนรับ</h1>
      <p class="text-gray-400 mb-8">เข้าสู่ระบบสัมภาษณ์งานอัตโนมัติ</p>

      <form @submit.prevent="startInterview" class="space-y-6">
        <div>
          <label class="block text-left text-sm font-medium mb-2"
            >ชื่อ-นามสกุล ของคุณ</label
          >
          <input
            v-model="name"
            type="text"
            placeholder="กรอกชื่อของคุณ..."
            autofocus
            required
            class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white placeholder-gray-400"
          />
        </div>

        <button
          type="submit"
          :disabled="!name.trim()"
          class="w-full px-6 py-3 text-lg font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          เริ่มการสัมภาษณ์ (Start Interview)
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
const { setCandidateName } = useInterview();
const router = useRouter();
const name = ref("");

const startInterview = () => {
  if (name.value.trim()) {
    setCandidateName(name.value);
    router.push("/question");
  }
};
</script>
