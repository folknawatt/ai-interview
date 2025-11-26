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
          <UInput
            v-model="name"
            size="lg"
            placeholder="กรอกชื่อของคุณ..."
            autofocus
            required
          />
        </div>

        <UButton
          type="submit"
          block
          size="lg"
          color="primary"
          :disabled="!name.trim()"
        >
          เริ่มการสัมภาษณ์ (Start Interview)
        </UButton>
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
