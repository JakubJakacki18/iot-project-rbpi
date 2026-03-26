<script setup lang="ts">
import { SENSOR_KEYS, type SensorType } from "@/types/sensors";
import SummaryBarChartComponent from "./SummaryBarChartComponent.vue";
const sensorkeys: SensorType[] = [...SENSOR_KEYS];
</script>
<template>
  <section>
    <h2 class="text-3xl font-bold mb-10">Panel główny</h2>
    <div class="grid grid-cols-1 xl:grid-cols-2">
      <div v-for="key in SENSOR_KEYS" :key="key">
        <SummaryBarChartComponent :sensorType="key" />
      </div>
    </div>
  </section>
</template>
