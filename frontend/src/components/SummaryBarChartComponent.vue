<script setup lang="ts">
import { ref, onMounted } from "vue";
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";
import { SensorService } from "../services/sensorService";
import type { SensorType } from "@/types/sensors";
import { sensorConfigs } from "@/constants/sensor";

const { sensorType: sensorType } = defineProps<{ sensorType: SensorType }>();

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
);

const loading = ref(true);
const error = ref<string | null>(null);
const chartData = ref<any>(null);
const avg = ref<string>("Brak");

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: "top" as const },
  },
};

// Funkcja pomocnicza: losowe kolory dla różnych ESP
const getRandomColor = (id: string) => {
  const colors = ["#42A5F5", "#66BB6A", "#FFA726", "#AB47BC", "#EF5350"];
  return colors[parseInt(id) % colors.length];
};

const loadData = async () => {
  try {
    loading.value = true;
    error.value = null;

    const response = await SensorService.getSensorLastWeekAvgValues(sensorType);
    const rawData = response.data;

    const allDates: string[] = [];
    Object.values(rawData).forEach((espData) => {
      Object.keys(espData).forEach((date) => {
        if (!allDates.includes(date)) {
          allDates.push(date);
        }
      });
    });
    const allValues = allDates.flatMap((date) =>
      Object.values(rawData)
        .map((espData) => espData[date])
        .filter((v) => typeof v === "number"),
    );
    console.log(allValues);
    avg.value = (
      (allValues?.reduce((sum, v) => sum + v, 0) ?? 0) / allValues.length
    ).toFixed(2);

    const datasets = Object.entries(rawData).map(([espId, readings]) => {
      return {
        label: `ESP-${espId}`,
        backgroundColor: getRandomColor(espId),
        data: allDates.map((date) => readings[date] ?? null),
      };
    });

    chartData.value = {
      labels: allDates,
      datasets: datasets,
    };
    console.log(chartData);
  } catch (err: any) {
    console.error(err);
    error.value = "Nie udało się załadować danych.";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadData();
});
</script>

<template>
  <div
    v-if="avg !== `NaN`"
    class="mb-10 mx-6 bg-gray-950 p-4 rounded-lg border border-gray-800 shadow"
  >
    <div class="flex flex-col h-72">
      <h3 class="text-md font-bold mb-4 text-center">
        Dane z tygodnia - {{ sensorConfigs[sensorType].label }}
      </h3>
      <p>Średnia: {{ avg }} {{ sensorConfigs[sensorType].unit }}</p>
      <div
        v-if="loading"
        class="flex-1 flex items-center justify-center text-center"
      >
        Pobieranie danych z bazy...
      </div>
      <div
        v-else-if="error"
        class="flex-1 flex items-center justify-center text-center"
      >
        {{ error }}
      </div>
      <div v-else class="flex-1">
        <Bar :data="chartData" :options="chartOptions" />
      </div>
    </div>
  </div>
</template>
