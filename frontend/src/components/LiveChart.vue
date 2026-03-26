<script setup lang="ts">
import { chartOptions } from "@/constants/chart";

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
import { computed, ref, watch } from "vue";
import { useSensorStore } from "@/stores/sensors";
import type { SensorType } from "@/types/sensors";
import { useRoute } from "vue-router";
import { sensorConfigs } from "@/constants/sensor";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
);

const store = useSensorStore();
const route = useRoute();

const espId = computed<string>(() => {
  const id = route.params.id;
  return (Array.isArray(id) ? id[0] : id) || "-1";
});

const { sensorType: sensorType } = defineProps<{ sensorType: SensorType }>();
const sensorValue = computed(() =>
  store.getSensorValues(espId.value, sensorType),
);

const chartLabel: string =
  sensorConfigs[sensorType].label + " " + sensorConfigs[sensorType].unit;
const chartColor: string = sensorConfigs[sensorType].color;

const chartData = ref<ChartData<"line">>({
  labels: [],
  datasets: [
    {
      label: chartLabel,
      backgroundColor: chartColor,
      borderColor: chartColor,
      data: [] as number[],
      tension: 0.4,
    },
  ],
});

watch(
  sensorValue,
  (newValue) => {
    console.log("test", newValue);
    if (!newValue) return;
    // chartData.value.labels = [...newValue.map((item) => item.time)];
    // if (chartData.value.datasets[0])
    //   chartData.value.datasets[0].data = [
    //     ...newValue.map((item) => item.value),
    //   ];
    chartData.value = {
      labels: newValue.map((item) => item.time),
      datasets: [
        {
          ...chartData.value.datasets[0],
          data: newValue.map((item) => item.value),
        },
      ],
    };
  },
  {
    deep: true,
    immediate: true,
  },
);
</script>
<template>
  <div class="h-72 w-full">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>
