<template>
  <div class="bar-chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const props = defineProps<{
  questions: Array<{
    question: string;
    total_score: number;
  }>;
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chart: ChartJS | null = null;

const getBarColor = (score: number) => {
  if (score >= 8) return 'rgba(16, 185, 129, 0.8)'; // Green
  if (score >= 6) return 'rgba(59, 130, 246, 0.8)'; // Blue
  if (score >= 4) return 'rgba(245, 158, 11, 0.8)'; // Orange
  return 'rgba(239, 68, 68, 0.8)'; // Red
};

onMounted(() => {
  if (chartCanvas.value) {
    const ctx = chartCanvas.value.getContext('2d');
    if (ctx) {
      const labels = props.questions.map((_, idx) => `Q${idx + 1}`);
      const scores = props.questions.map(q => q.total_score);
      const colors = scores.map(score => getBarColor(score));

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
              borderWidth: 1
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 10,
              ticks: {
                stepSize: 2
              },
              title: {
                display: true,
                text: 'Score (out of 10)'
              }
            },
            x: {
              title: {
                display: true,
                text: 'Questions'
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
                  return `Score: ${context.parsed.y.toFixed(1)} / 10`;
                },
                afterLabel: function(context) {
                  const question = props.questions[context.dataIndex];
                  return question.question.substring(0, 50) + '...';
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
</script>

<style scoped>
.bar-chart-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}
</style>
