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
        <UButton
          @click="goToRecord"
          size="xl"
          color="primary"
          icon="i-heroicons-video-camera"
        >
          พร้อมแล้ว! เริ่มอัดวิดีโอเลย
        </UButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { question } = useInterview();
const router = useRouter();

const timeLeft = ref(30);
let timer: NodeJS.Timeout;

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
