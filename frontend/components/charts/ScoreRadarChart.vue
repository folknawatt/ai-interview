<template>
  <div class="radar-chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import {
  Chart as ChartJS,
  RadarController,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(
  RadarController,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
)

const props = defineProps<{
  communicationAvg: number
  relevanceAvg: number
  logicalThinkingAvg: number
}>()

const chartCanvas = ref<HTMLCanvasElement | null>(null)
let chart: ChartJS | null = null

onMounted(() => {
  try {
    if (!chartCanvas.value) return
    if (
      props.communicationAvg == null ||
      props.relevanceAvg == null ||
      props.logicalThinkingAvg == null
    )
      return

    const ctx = chartCanvas.value.getContext('2d')
    if (!ctx) return

    chart = new ChartJS(ctx, {
      type: 'radar',
      data: {
        labels: ['Communication', 'Relevance', 'Logical Thinking'],
        datasets: [
          {
            label: 'Scores',
            data: [props.communicationAvg, props.relevanceAvg, props.logicalThinkingAvg],
            backgroundColor: 'rgba(255, 196, 40, 0.2)',
            borderColor: '#FFC428',
            borderWidth: 2,
            pointBackgroundColor: '#FFC428',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: '#FFC428',
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          r: {
            angleLines: {
              display: true,
              color: 'rgba(255, 255, 255, 0.1)',
            },
            grid: {
              color: 'rgba(255, 255, 255, 0.1)',
            },
            pointLabels: {
              color: '#a1a1aa',
              font: {
                size: 12,
              },
            },
            ticks: {
              stepSize: 1,
              color: '#71717a',
              backdropColor: 'transparent',
            },
            suggestedMin: 0,
            suggestedMax: 5,
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
                return context.parsed.r.toFixed(2) + ' / 5'
              },
            },
          },
        },
      },
    })
  } catch (error) {
    console.error('ScoreRadarChart error:', error)
  }
})

onUnmounted(() => {
  if (chart) {
    chart.destroy()
  }
})

watch(
  () => [props.communicationAvg, props.relevanceAvg, props.logicalThinkingAvg],
  newValues => {
    if (chart && chart.data && chart.data.datasets && chart.data.datasets[0]) {
      chart.data.datasets[0].data = newValues
      chart.update()
    }
  }
)
</script>

<style scoped>
.radar-chart-container {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}
</style>
