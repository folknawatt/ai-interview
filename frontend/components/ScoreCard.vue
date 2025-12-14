<template>
  <div class="score-card">
    <svg class="progress-ring" :width="size" :height="size">
      <circle
        class="progress-ring__circle-bg"
        :stroke="bgColor"
        :stroke-width="strokeWidth"
        fill="transparent"
        :r="radius"
        :cx="size / 2"
        :cy="size / 2"
      />
      <circle
        class="progress-ring__circle"
        :stroke="scoreColor"
        :stroke-width="strokeWidth"
        fill="transparent"
        :r="radius"
        :cx="size / 2"
        :cy="size / 2"
        :style="{
          strokeDasharray: `${circumference} ${circumference}`,
          strokeDashoffset: strokeDashoffset
        }"
      />
    </svg>
    <div class="score-content">
      <div class="score-value">{{ score }}</div>
      <div class="score-max">/ 10</div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  score: number; // 0-10 scale
  size?: number;
  strokeWidth?: number;
}>();

const size = computed(() => props.size || 150);
const strokeWidth = computed(() => props.strokeWidth || 12);
const radius = computed(() => (size.value - strokeWidth.value) / 2);
const circumference = computed(() => radius.value * 2 * Math.PI);

const percentage = computed(() => (props.score / 10) * 100);

const strokeDashoffset = computed(() => {
  const offset = circumference.value - (percentage.value / 100) * circumference.value;
  return offset;
});

const scoreColor = computed(() => {
  if (props.score >= 8) return '#10b981'; // Green
  if (props.score >= 6) return '#3b82f6'; // Blue
  if (props.score >= 4) return '#f59e0b'; // Orange
  return '#ef4444'; // Red
});

const bgColor = '#e5e7eb';
</script>

<style scoped>
.score-card {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.progress-ring {
  transform: rotate(-90deg);
}

.progress-ring__circle {
  transition: stroke-dashoffset 0.8s ease-in-out;
  stroke-linecap: round;
}

.score-content {
  position: absolute;
  display: flex;
  align-items: baseline;
  gap: 0.2rem;
}

.score-value {
  font-size: 2.5rem;
  font-weight: bold;
  color: #1a1a1a;
}

.score-max {
  font-size: 1.2rem;
  color: #666;
}
</style>
