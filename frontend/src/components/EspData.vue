<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { io } from "socket.io-client";
import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  type ChartData,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
);

const timeLabels = ref<string[]>([]);
const tempHistory = ref<number[]>([]);
const humHistory = ref<number[]>([]);
const MAX_DATAPOINTS = 15;

const chartData = ref<ChartData<"line">>({
  labels: timeLabels.value,
  datasets: [
    {
      label: "Temperatura (°C)",
      backgroundColor: "#3b82f6",
      borderColor: "#3b82f6",
      data: [] as number[],
      tension: 0.4,
    },
    {
      label: "Wilgotność (%)",
      backgroundColor: "#10b981",
      borderColor: "#10b981",
      data: [] as number[],
      tension: 0.4,
    },
  ],
});

// Opcje wyglądu wykresu
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: false,
    },
  },
  animation: {
    duration: 0,
  },
};

const route = useRoute();
const espId = computed(() => route.params.id);
const temperature = ref<number | string>("Oczekiwanie...");
const humidity = ref<number | string>("Oczekiwanie...");

const socket = io("http://127.0.0.1:5000");
onMounted(() => {
  socket.on("sensor_update", (data) => {
    if (data.id === espId.value) {
      temperature.value = data.temp;
      humidity.value = data.humidity;
      const now = new Date();

      const timeStr = now.toLocaleTimeString("pl-PL", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });
      tempHistory.value.push(data.temp);
      humHistory.value.push(data.humidity);

      // 3. ZMIANA: Kopiujemy obecne dane do nowych tablic (BEZ UŻYWANIA .push()!)
      const newLabels = [...(chartData.value.labels ?? []), timeStr];
      const newTemps = [
        ...(chartData.value.datasets[0]?.data ?? []),
        data.temp,
      ];
      const newHums = [
        ...(chartData.value.datasets[1]?.data ?? []),
        data.humidity,
      ];

      if (newLabels.length > MAX_DATAPOINTS) {
        newLabels.shift();
        newTemps.shift();
        newHums.shift();
      }

      chartData.value = {
        labels: newLabels,
        datasets: [
          { ...chartData.value.datasets[0], data: newTemps },
          { ...chartData.value.datasets[1], data: newHums },
        ],
      };
    }
  });
});

onUnmounted(() => {
  socket.disconnect();
});
</script>
<template>
  <div>
    <h2 class="text-lg font-semibold mb-2">ESP {{ espId }}</h2>

    <p>{{ temperature }}</p>
    <p>{{ humidity }}</p>

    <div class="relative h-72 w-full">
      <Line :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>
