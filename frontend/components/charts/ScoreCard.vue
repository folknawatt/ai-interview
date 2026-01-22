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
          strokeDashoffset: strokeDashoffset,
        }"
      />
    </svg>
    <div class="score-content">
      <div class="score-value" :style="{ color: scoreColor }">{{ score }}</div>
      <div class="score-max">/ {{ maxScore }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    score: number
    maxScore?: number
    size?: number
    strokeWidth?: number
  }>(),
  {
    maxScore: 5,
    size: 150,
    strokeWidth: 12,
  }
)

const size = computed(() => props.size)
const strokeWidth = computed(() => props.strokeWidth)
const radius = computed(() => (size.value - strokeWidth.value) / 2)
const circumference = computed(() => radius.value * 2 * Math.PI)

const percentage = computed(() => (props.score / props.maxScore) * 100)

const strokeDashoffset = computed(() => {
  const offset = circumference.value - (percentage.value / 100) * circumference.value
  return offset
})

const scoreColor = computed(() => {
  const p = percentage.value
  if (p >= 80) return '#22c55e' // Green (>= 8/10 or 24/30)
  if (p >= 60) return '#3b82f6' // Blue
  if (p >= 40) return '#FFC428' // Amber
  return '#ef4444' // Red
})

// Dark theme background
const bgColor = 'rgba(255, 255, 255, 0.1)'
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
}

.score-max {
  font-size: 1.2rem;
  color: #a1a1aa;
}
</style>
