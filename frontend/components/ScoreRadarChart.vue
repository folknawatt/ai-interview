<template>
  <div class="radar-chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

const props = defineProps<{
  communicationAvg: number;
  relevanceAvg: number;
  logicalThinkingAvg: number;
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chart: ChartJS | null = null;

onMounted(() => {
  if (chartCanvas.value) {
    const ctx = chartCanvas.value.getContext('2d');
    if (ctx) {
      chart = new ChartJS(ctx, {
        type: 'radar',
        data: {
          labels: ['Communication', 'Relevance', 'Logical Thinking'],
          datasets: [
            {
              label: 'Scores',
              data: [
                props.communicationAvg,
                props.relevanceAvg,
                props.logicalThinkingAvg
              ],
              backgroundColor: 'rgba(102, 126, 234, 0.2)',
              borderColor: 'rgba(102, 126, 234, 1)',
              borderWidth: 2,
              pointBackgroundColor: 'rgba(102, 126, 234, 1)',
              pointBorderColor: '#fff',
              pointHoverBackgroundColor: '#fff',
              pointHoverBorderColor: 'rgba(102, 126, 234, 1)'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          scales: {
            r: {
              angleLines: {
                display: true
              },
              suggestedMin: 0,
              suggestedMax: 10,
              ticks: {
                stepSize: 2
              }
            }
          },
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return context.parsed.r.toFixed(2) + ' / 10';
                }
              }
            }
          }
        }
      });
    }
  }
});

onUnmounted(() => {
  if (chart) {
    chart.destroy();
  }
});

watch(
  () => [props.communicationAvg, props.relevanceAvg, props.logicalThinkingAvg],
  (newValues) => {
    if (chart && chart.data && chart.data.datasets && chart.data.datasets[0]) {
      chart.data.datasets[0].data = newValues;
      chart.update();
    }
  }
);
</script>

<style scoped>
.radar-chart-container {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}
</style>
