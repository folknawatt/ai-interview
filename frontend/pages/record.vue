<template>
  <div
    class="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-4"
  >
    <div class="w-full max-w-4xl bg-gray-800 p-6 rounded-lg shadow-lg">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">📹 บันทึกคำตอบ (Record Answer)</h2>
        <div
          class="text-2xl font-mono font-bold"
          :class="{ 'text-red-500': isRecording }"
        >
          {{ formatTime(timer) }}
        </div>
      </div>

      <div
        class="relative aspect-video bg-black rounded-lg overflow-hidden mb-6"
      >
        <video
          ref="videoPreview"
          autoplay
          muted
          playsinline
          class="w-full h-full object-cover"
        ></video>

        <div
          v-if="!isRecording && !recordedBlob"
          class="absolute inset-0 flex items-center justify-center bg-black/50"
        >
          <p class="text-gray-300">กดปุ่ม "เริ่มอัดวิดีโอ" เมื่อพร้อม</p>
        </div>
      </div>

      <div class="flex justify-center space-x-4">
        <UButton
          v-if="!isRecording && !recordedBlob"
          @click="startRecording"
          size="xl"
          color="red"
          icon="i-heroicons-video-camera"
        >
          เริ่มอัดวิดีโอ (Start Recording)
        </UButton>

        <UButton
          v-if="isRecording"
          @click="stopRecording"
          size="xl"
          color="gray"
          icon="i-heroicons-stop"
        >
          หยุดอัด (Stop Recording)
        </UButton>

        <UButton
          v-if="recordedBlob"
          @click="submitRecording"
          size="xl"
          color="primary"
          :loading="isSubmitting"
          icon="i-heroicons-paper-airplane"
        >
          ส่งคำตอบ (Submit Answer)
        </UButton>

        <UButton
          v-if="recordedBlob && !isSubmitting"
          @click="resetRecording"
          size="xl"
          color="white"
          variant="outline"
        >
          อัดใหม่ (Retake)
        </UButton>
      </div>

      <div
        v-if="isSubmitting"
        class="mt-4 text-center text-gray-400 animate-pulse"
      >
        กำลังอัพโหลดและวิเคราะห์ผล... (Uploading & Analyzing...)
      </div>
      <div v-if="error" class="mt-4 text-center text-red-500">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { question, setAnalysisResult } = useInterview();
const router = useRouter();

const videoPreview = ref<HTMLVideoElement | null>(null);
const mediaRecorder = ref<MediaRecorder | null>(null);
const recordedChunks = ref<Blob[]>([]);
const recordedBlob = ref<Blob | null>(null);
const isRecording = ref(false);
const isSubmitting = ref(false);
const timer = ref(120); // 2 minutes
const error = ref<string | null>(null);
let timerInterval: NodeJS.Timeout;

const formatTime = (seconds: number) => {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
};

const startCamera = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: true,
    });
    if (videoPreview.value) {
      videoPreview.value.srcObject = stream;
    }
  } catch (e) {
    console.error("Error accessing camera:", e);
    error.value = "ไม่สามารถเข้าถึงกล้อง/ไมโครโฟนได้";
  }
};

const startRecording = async () => {
  if (!videoPreview.value?.srcObject) await startCamera();

  const stream = videoPreview.value?.srcObject as MediaStream;
  if (!stream) return;

  recordedChunks.value = [];
  // Try to use mp4 mime type if available, otherwise webm
  const mimeType = MediaRecorder.isTypeSupported("video/mp4")
    ? "video/mp4"
    : "video/webm";

  const recorder = new MediaRecorder(stream, { mimeType });

  recorder.ondataavailable = (e) => {
    if (e.data.size > 0) {
      recordedChunks.value.push(e.data);
    }
  };

  recorder.onstop = () => {
    recordedBlob.value = new Blob(recordedChunks.value, { type: mimeType });
    clearInterval(timerInterval);
    isRecording.value = false;
  };

  recorder.start();
  mediaRecorder.value = recorder;
  isRecording.value = true;

  timerInterval = setInterval(() => {
    if (timer.value > 0) {
      timer.value--;
    } else {
      stopRecording();
    }
  }, 1000);
};

const stopRecording = () => {
  if (mediaRecorder.value && isRecording.value) {
    mediaRecorder.value.stop();
  }
};

const resetRecording = () => {
  recordedBlob.value = null;
  recordedChunks.value = [];
  timer.value = 120;
  startCamera();
};

const submitRecording = async () => {
  if (!recordedBlob.value) return;

  isSubmitting.value = true;
  error.value = null;

  try {
    const formData = new FormData();
    // Determine extension based on mime type
    const ext = recordedBlob.value.type.includes("mp4") ? "mp4" : "webm";
    formData.append("file", recordedBlob.value, `interview_recording.${ext}`);

    // 1. Upload
    const uploadRes = await $fetch<{ filename: string; transcript: string }>(
      "http://localhost:8000/upload",
      {
        method: "POST",
        body: formData,
      }
    );

    // 2. Analyze
    const analyzeRes = await $fetch("http://localhost:8000/analyze", {
      method: "POST",
      body: {
        transcript: uploadRes.transcript,
        question: question.value,
      },
    });

    setAnalysisResult(analyzeRes);
    router.push("/result");
  } catch (e: any) {
    console.error(e);
    error.value = e.message || "เกิดข้อผิดพลาดในการส่งข้อมูล";
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(() => {
  startCamera();
});

onUnmounted(() => {
  clearInterval(timerInterval);
  if (videoPreview.value?.srcObject) {
    const tracks = (videoPreview.value.srcObject as MediaStream).getTracks();
    tracks.forEach((track) => track.stop());
  }
});
</script>
