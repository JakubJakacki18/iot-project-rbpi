<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { io } from "socket.io-client";
import { useSensorStore } from "@/stores/sensors";
import type { SensorType, TimeValue } from "@/types/sensors";
import { SENSOR_KEYS } from "@/types/sensors";
import LiveComponent from "./LiveComponent.vue";
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
const store = useSensorStore();
const route = useRoute();
const espId = computed(() => route.params.id);
const espIdTest = computed<string>(() => {
  const id = route.params.id;
  return (Array.isArray(id) ? id[0] : id) || "-1";
});
const allLastValues = computed(() =>
  store.getAllLastSensorValue(espIdTest.value),
);

const temperature = ref<number | string>("Oczekiwanie...");
const humidity = ref<number | string>("Oczekiwanie...");

const socket = io("http://127.0.0.1:5000");
onMounted(() => {
  socket.on("sensor_update", (data) => {
    console.log("Odebrano dane", data);
    const now = new Date();
    const timeStr = now.toLocaleTimeString("pl-PL", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
    for (const key of SENSOR_KEYS) {
      if (data[key] === undefined) {
        continue;
      }
      const timeValue: TimeValue = { time: timeStr, value: data[key] };
      store.setSensorValue(data.id, key, timeValue);
    }
    console.log(store.getAllLastSensorValue(data.id));
    // if (data.id === espId.value) {
    //   temperature.value = data.temp;
    //   humidity.value = data.humidity;

    //   tempHistory.value.push(data.temp);
    //   humHistory.value.push(data.humidity);

    //   // 3. ZMIANA: Kopiujemy obecne dane do nowych tablic (BEZ UŻYWANIA .push()!)
    //   const newLabels = [...(chartData.value.labels ?? []), timeStr];
    //   const newTemps = [
    //     ...(chartData.value.datasets[0]?.data ?? []),
    //     data.temp,
    //   ];
    //   const newHums = [
    //     ...(chartData.value.datasets[1]?.data ?? []),
    //     data.humidity,
    //   ];

    //   if (newLabels.length > MAX_DATAPOINTS) {
    //     newLabels.shift();
    //     newTemps.shift();
    //     newHums.shift();
    //   }

    //   chartData.value = {
    //     labels: newLabels,
    //     datasets: [
    //       { ...chartData.value.datasets[0], data: newTemps },
    //       { ...chartData.value.datasets[1], data: newHums },
    //     ],
    //   };
    // }
  });
});

onUnmounted(() => {
  socket.disconnect();
});
</script>
<template>
  <div>
    <h2 class="text-3xl font-bold mb-6">ESP {{ espId }}</h2>

    <!-- <p>{{ lastTemp }}</p> -->
    <!-- <div v-for="(lastValue, key) in allLastValues" :key="key">
      {{ key }}: {{ lastValue ? lastValue : "Oczekiwanie na dane..." }}
    </div> -->
    <div>
      <LiveComponent
        v-for="key in SENSOR_KEYS"
        :key="key"
        :sensorData="key"
        class="mb-2"
      />
    </div>

    <!-- <div class="h-72 w-full">
      <Line :data="chartData" :options="chartOptions" />
    </div> -->
  </div>
</template>
