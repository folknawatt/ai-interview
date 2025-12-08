<template>
  <div
    class="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-4"
  >
    <div
      class="w-full max-w-2xl bg-gray-800 p-8 rounded-lg shadow-lg text-center"
    >
      <div class="mb-6">
        <span
          class="bg-primary-900 text-primary-300 text-xs font-medium px-2.5 py-0.5 rounded border border-primary-700"
        >
          คำถามสัมภาษณ์
        </span>
      </div>

      <h2 class="text-2xl md:text-3xl font-bold mb-8 leading-relaxed">
        "{{ question }}"
      </h2>

      <div class="flex flex-col items-center justify-center space-y-4">
        <div class="text-gray-400 text-sm">
          เวลาเตรียมตัว (Preparation Time)
        </div>
        <div class="text-6xl font-mono font-bold text-primary-400">
          {{ timeLeft }}s
        </div>
      </div>

      <div class="mt-10">
        <button
          @click="goToRecord"
          class="inline-flex items-center px-6 py-3 text-lg font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
        >
          <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
          </svg>
          พร้อมแล้ว! เริ่มอัดวิดีโอเลย
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { question } = useInterview();
const router = useRouter();

const timeLeft = ref(30);
let timer: ReturnType<typeof setInterval>;

onMounted(() => {
  timer = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--;
    } else {
      goToRecord();
    }
  }, 1000);
});

onUnmounted(() => {
  clearInterval(timer);
});

const goToRecord = () => {
  router.push("/record");
};
</script>
