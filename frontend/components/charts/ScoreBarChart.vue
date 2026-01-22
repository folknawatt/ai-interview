<template>
  <div class="bar-chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import {
  Chart as ChartJS,
  BarController,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(BarController, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const props = defineProps<{
  questions: Array<{
    question: string
    average_score: number
  }>
}>()

const chartCanvas = ref<HTMLCanvasElement | null>(null)
let chart: ChartJS | null = null

const getBarColor = (score: number) => {
  if (score >= 4) return 'rgba(34, 197, 94, 0.8)' // Green
  if (score >= 3) return 'rgba(59, 130, 246, 0.8)' // Blue
  if (score >= 2) return 'rgba(255, 196, 40, 0.8)' // Amber
  return 'rgba(239, 68, 68, 0.8)' // Red
}

onMounted(() => {
  if (!props.questions || props.questions.length === 0) return
  if (chartCanvas.value) {
    const ctx = chartCanvas.value.getContext('2d')
    if (ctx) {
      const labels = props.questions.map((_, idx) => `Q${idx + 1}`)
      const scores = props.questions.map(q => q.average_score)
      const colors = scores.map(score => getBarColor(score))

      chart = new ChartJS(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            {
              label: 'Score',
              data: scores,
              backgroundColor: colors,
              borderColor: colors.map(c => c.replace('0.8', '1')),
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 5,
              ticks: {
                stepSize: 1,
                color: '#a1a1aa',
              },
              title: {
                display: true,
                text: 'Score (out of 5)',
                color: '#a1a1aa',
              },
              grid: {
                color: 'rgba(255, 255, 255, 0.1)',
              },
            },
            x: {
              ticks: {
                color: '#a1a1aa',
              },
              title: {
                display: true,
                text: 'Questions',
                color: '#a1a1aa',
              },
              grid: {
                color: 'rgba(255, 255, 255, 0.1)',
              },
            },
          },
          plugins: {
            legend: {
              display: false,
            },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              titleColor: '#fff',
              bodyColor: '#fff',
              callbacks: {
                label: function (context) {
                  return `Score: ${context.parsed.y?.toFixed(1) ?? 'N/A'} / 5`
                },
                afterLabel: function (context) {
                  const question = props.questions[context.dataIndex]
                  return question?.question?.substring(0, 50) + '...'
                },
              },
            },
          },
        },
      })
    }
  }
})

onUnmounted(() => {
  if (chart) {
    chart.destroy()
  }
})
</script>

<style scoped>
.bar-chart-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}
</style>
