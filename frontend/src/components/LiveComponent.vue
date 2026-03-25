<script setup lang="ts">
import { useSensorStore } from "@/stores/sensors";
import type { SensorType } from "@/types/sensors";
import { sensorConfigs } from "@/constants/sensor";

import LiveChart from "./LiveChart.vue";
import { computed } from "vue";
import { useRoute } from "vue-router";

const store = useSensorStore();
const route = useRoute();

const espId = computed<string>(() => {
  const id = route.params.id;
  return (Array.isArray(id) ? id[0] : id) || "-1";
});

const { sensorData } = defineProps<{ sensorData: SensorType }>();
const sensorValue = computed(() =>
  store.getLastSensorValue(espId.value, sensorData),
);
</script>
<template>
  <article v-if="sensorValue">
    {{ sensorConfigs[sensorData].label }}:
    <div>
      <p class="text-2xl font-bold">
        {{ sensorValue.value?.toFixed(2) }} {{ sensorConfigs[sensorData].unit }}
      </p>
      <span class="text-xs text-gray-500"
        >Ostatnia aktualizacja: {{ sensorValue.time }}</span
      >
    </div>
    <!-- <div v-else class="text-gray-500 italic">
      Oczekiwanie na dane...
    </div> -->
    <LiveChart :sensorData="sensorData" />
  </article>
</template>
