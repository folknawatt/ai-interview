<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center p-4">
    <div class="bg-white p-8 rounded-xl shadow-lg w-full max-w-2xl text-center">
      <h1 class="text-3xl font-bold text-gray-800 mb-6">🎥 ระบบจำลอง AI Interview (Camera)</h1>
      
      <div class="mb-5 font-semibold text-gray-600 p-3 bg-gray-100 rounded-lg">
        {{ statusText }}
      </div>

      <div class="text-2xl text-blue-600 my-8 p-5 border-l-4 border-blue-600 bg-blue-50 min-h-[80px] flex items-center justify-center">
        <div v-html="questionText"></div>
      </div>

      <div class="space-x-2 mt-4">
        <button
          v-if="!isInterviewStarted"
          @click="startInterview"
          style="background-color: #10b981; color: white; padding: 12px 24px; font-size: 1.125rem; border-radius: 8px; border: none; cursor: pointer;"
          class="px-6 py-3 text-lg bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors font-semibold"
        >
          เริ่มการสัมภาษณ์
        </button>

        <button
          v-if="isInterviewStarted && !isInterviewFinished"
          @click="stopCurrentSegment"
          :disabled="isProcessing"
          style="background-color: #3b82f6; color: white; padding: 12px 24px; font-size: 1.125rem; border-radius: 8px; border: none; cursor: pointer;"
          class="px-6 py-3 text-lg bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed font-semibold"
        >
          {{ nextButtonText }}
        </button>
      </div>

      <div v-if="isInterviewFinished" class="mt-8 text-left border-t-2 border-gray-200 pt-5">
        <h3 class="text-xl font-semibold mb-4">🎉 การสัมภาษณ์เสร็จสิ้น!</h3>
        <p class="mb-4">คลิกลิงก์ด้านล่างเพื่อดาวน์โหลดวิดีโอคำตอบของคุณ (แยกตามคำถาม)</p>
        
        <div class="space-y-3">
          <a
            v-for="link in videoLinks"
            :key="link.index"
            :href="link.url"
            :download="`Interview_Q${link.index}_Answer.webm`"
            class="block p-3 bg-gray-100 hover:bg-gray-200 text-gray-800 no-underline rounded transition-colors"
          >
            ⬇️ ดาวน์โหลดวิดีโอคำตอบ ข้อที่ {{ link.index }}
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// --- Types ---
interface VideoLink {
  index: number;
  url: string;
}

// --- Data ---
const questions = [
  "คำถามที่ 1: ช่วยแนะนำตัวเองสั้นๆ และเล่าถึงประสบการณ์ทำงานหรือการเรียนที่โดดเด่นที่สุดของคุณให้ฟังหน่อยครับ",
  "คำถามที่ 2: ลองยกตัวอย่างสถานการณ์ที่คุณต้องเผชิญกับปัญหาหรือความกดดันในการทำงาน คุณมีวิธีรับมือและแก้ไขสถานการณ์นั้นอย่างไร?",
  "คำถามที่ 3: ทำไมคุณถึงสนใจในตำแหน่งงานนี้ และคุณมองภาพตัวเองในอีก 3-5 ปีข้างหน้าไว้อย่างไรในเส้นทางอาชีพนี้?"
];

const currentQuestionIndex = ref(0);
const isInterviewStarted = ref(false);
const isInterviewFinished = ref(false);
const isProcessing = ref(false);
const statusText = ref("สถานะ: พร้อมเริ่มการสัมภาษณ์ (ทั้งหมด 3 คำถาม)");
const questionText = ref("กดปุ่ม \"เริ่มการสัมภาษณ์\" เพื่อเริ่มต้น<br>(ระบบจะขออนุญาตเข้าถึงกล้องและไมโครโฟนในแต่ละคำถาม)");
const nextButtonText = ref("ตอบเสร็จแล้ว / ไปคำถามถัดไป");
const videoLinks = ref<VideoLink[]>([]);

let mediaRecorder: MediaRecorder | null = null;
let recordedChunks: Blob[] = [];
let stream: MediaStream | null = null;

// --- Methods ---
const startInterview = () => {
  isInterviewStarted.value = true;
  currentQuestionIndex.value = 0;
  videoLinks.value = [];
  runQuestionSegment();
};

const runQuestionSegment = async () => {
  // Check if all questions are done
  if (currentQuestionIndex.value >= questions.length) {
    finishInterview();
    return;
  }

  // Update UI
  statusText.value = `สถานะ: กำลังบันทึก... (คำถามที่ ${currentQuestionIndex.value + 1} / 3)`;
  questionText.value = questions[currentQuestionIndex.value] || '';
  isProcessing.value = true;
  nextButtonText.value = "กำลังเตรียมการบันทึก...";

  // Start screen recording
  try {
    await startCameraRecording();
    isProcessing.value = false;
    nextButtonText.value = "ตอบเสร็จแล้ว / ไปคำถามถัดไป";
  } catch (err) {
    console.error("Error starting recording:", err);
    alert("เกิดข้อผิดพลาด: ไม่สามารถเข้าถึงกล้องหรือไมโครโฟนได้ กรุณาลองใหม่และอนุญาตสิทธิ์");
    statusText.value = "สถานะ: เกิดข้อผิดพลาด";
    isInterviewStarted.value = false;
  }
};

const startCameraRecording = async () => {
  console.log('🎥 Starting camera recording...');
  recordedChunks = [];
  
  // Check if getUserMedia is available
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    throw new Error('Camera recording is not supported in this browser');
  }
  
  console.log('🎥 Requesting camera and microphone permission...');
  
  try {
    // Request camera and microphone permission
    stream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: true
    });
    
    console.log('✅ Camera and microphone permission granted', stream);

    mediaRecorder = new MediaRecorder(stream);

    // Collect video data
    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        recordedChunks.push(event.data);
      }
    };

    // Handle recording stop
    mediaRecorder.onstop = () => {
      // Create video file from recorded data
      const blob = new Blob(recordedChunks, { type: 'video/webm' });
      const url = URL.createObjectURL(blob);
      videoLinks.value.push({ 
        index: currentQuestionIndex.value + 1, 
        url: url 
      });

      // Stop stream tracks
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }

      // Move to next question
      currentQuestionIndex.value++;
      runQuestionSegment();
    };

    // Start recording
    console.log('🎬 Starting MediaRecorder...');
    mediaRecorder.start();
    console.log('✅ Recording started successfully');
  } catch (error) {
    console.error('❌ Error in startCameraRecording:', error);
    throw error;
  }
};

const stopCurrentSegment = () => {
  if (mediaRecorder && mediaRecorder.state === "recording") {
    statusText.value = "สถานะ: กำลังประมวลผลวิดีโอ...";
    isProcessing.value = true;
    nextButtonText.value = "กรุณารอสักครู่...";
    mediaRecorder.stop();
  }
};

const finishInterview = () => {
  isInterviewFinished.value = true;
  statusText.value = "สถานะ: การสัมภาษณ์เสร็จสิ้น";
  questionText.value = "ขอบคุณที่ร่วมการสัมภาษณ์ กรุณาดาวน์โหลดไฟล์วิดีโอด้านล่าง";
};

// Cleanup on unmount
onUnmounted(() => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
  }
  // Revoke object URLs to free memory
  videoLinks.value.forEach(link => {
    URL.revokeObjectURL(link.url);
  });
});
</script>
