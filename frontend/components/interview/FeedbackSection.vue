<template>
  <div class="bg-minimal-card p-6 rounded-lg shadow-sm border border-minimal-border md:col-span-2">
    <h2 class="text-xl font-semibold mb-4">คำติชม (Feedback)</h2>
    <div class="space-y-6">
      <!-- Strengths -->
      <div v-if="strengths.length > 0">
        <h3 class="text-sm font-medium text-minimal-success mb-2 flex items-center gap-1">
          <SparklesIcon class="w-4 h-4" />
          จุดแข็ง
        </h3>
        <ul class="list-disc list-inside text-minimal-text-secondary space-y-1">
          <li v-for="(item, index) in strengths" :key="index">{{ item }}</li>
        </ul>
      </div>
      <div v-else>
        <h3 class="text-sm font-medium text-minimal-success mb-2 flex items-center gap-1">
          <SparklesIcon class="w-4 h-4" />
          จุดแข็ง
        </h3>
        <p class="text-minimal-text-secondary italic">ไม่มีระบุ</p>
      </div>

      <!-- Weaknesses -->
      <div v-if="weaknesses.length > 0">
        <h3 class="text-sm font-medium text-amber-500 mb-2 flex items-center gap-1">
          <ExclamationTriangleIcon class="w-4 h-4" />
          จุดที่ควรพัฒนา
        </h3>
        <ul class="list-disc list-inside text-minimal-text-secondary space-y-1">
          <li v-for="(item, index) in weaknesses" :key="index">{{ item }}</li>
        </ul>
      </div>
      <div v-else>
        <h3 class="text-sm font-medium text-amber-500 mb-2 flex items-center gap-1">
          <ExclamationTriangleIcon class="w-4 h-4" />
          จุดที่ควรพัฒนา
        </h3>
        <p class="text-minimal-text-secondary italic">ไม่มีระบุ</p>
      </div>

      <!-- Summary -->
      <div v-if="summary">
        <h3 class="text-sm font-medium text-minimal-info mb-2 flex items-center gap-1">
          <DocumentTextIcon class="w-4 h-4" />
          สรุปภาพรวม
        </h3>
        <p class="text-minimal-text-secondary">{{ summary }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { SparklesIcon, ExclamationTriangleIcon, DocumentTextIcon } from '@heroicons/vue/24/solid'

defineProps<{
  strengths: string[]
  weaknesses: string[]
  summary?: string
}>()
</script>
