<template>
  <div class="min-h-screen bg-gray-900 text-white p-8">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold mb-6 text-center">
        📊 ผลการวิเคราะห์ (Analysis Result)
      </h1>

      <div v-if="result" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Scores -->
        <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 class="text-xl font-semibold mb-4">คะแนนประเมิน (Scores)</h2>
          <div class="grid grid-cols-2 gap-4">
            <div class="bg-gray-700 p-4 rounded text-center">
              <div class="text-sm text-gray-400">Communication</div>
              <div class="text-2xl font-bold text-primary-400">
                {{ result.scores.communication }}/10
              </div>
            </div>
            <div class="bg-gray-700 p-4 rounded text-center">
              <div class="text-sm text-gray-400">Relevance</div>
              <div class="text-2xl font-bold text-primary-400">
                {{ result.scores.relevance }}/10
              </div>
            </div>
            <div class="bg-gray-700 p-4 rounded text-center">
              <div class="text-sm text-gray-400">Quality</div>
              <div class="text-2xl font-bold text-primary-400">
                {{ result.scores.quality }}/10
              </div>
            </div>
            <div
              class="bg-gray-700 p-4 rounded text-center border-2 border-primary-500"
            >
              <div class="text-sm text-gray-400">Total Score</div>
              <div class="text-3xl font-bold text-white">
                {{ result.scores.total }}/30
              </div>
            </div>
          </div>
        </div>

        <!-- Pass/Fail -->
        <div
          class="bg-gray-800 p-6 rounded-lg shadow-lg flex flex-col items-center justify-center"
        >
          <h2 class="text-xl font-semibold mb-4">ผลสรุป (Conclusion)</h2>
          <div v-if="result.pass_prediction" class="text-center">
            <div class="text-6xl mb-2">✅</div>
            <div class="text-2xl font-bold text-green-400">ผ่าน (PASS)</div>
          </div>
          <div v-else class="text-center">
            <div class="text-6xl mb-2">❌</div>
            <div class="text-2xl font-bold text-red-400">ไม่ผ่าน (FAIL)</div>
          </div>
        </div>

        <!-- Feedback -->
        <div class="bg-gray-800 p-6 rounded-lg shadow-lg md:col-span-2">
          <h2 class="text-xl font-semibold mb-4">📝 ข้อเสนอแนะ (Feedback)</h2>
          <div class="space-y-4">
            <div>
              <h3 class="font-bold text-green-400">จุดแข็ง (Strengths)</h3>
              <p class="text-gray-300">{{ result.feedback.strengths }}</p>
            </div>
            <div>
              <h3 class="font-bold text-red-400">จุดอ่อน (Weaknesses)</h3>
              <p class="text-gray-300">{{ result.feedback.weaknesses }}</p>
            </div>
            <div>
              <h3 class="font-bold text-blue-400">สรุป (Summary)</h3>
              <p class="text-gray-300">{{ result.feedback.summary }}</p>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center text-gray-400 mt-10">
        <p>ไม่พบข้อมูลผลลัพธ์ กรุณากลับไปหน้าแรก</p>
        <UButton to="/" color="gray" class="mt-4">กลับหน้าแรก</UButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { analysisResult } = useInterview();
const result = analysisResult;
</script>
