<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { io } from "socket.io-client";
import { useSensorStore } from "@/stores/sensors";
import type { TimeValue } from "@/types/sensors";
import { SENSOR_KEYS } from "@/types/sensors";
import LiveComponent from "./LiveComponent.vue";
import { BACKEND_URL } from "@/constants/url";

const store = useSensorStore();
const route = useRoute();

const espId = computed<string>(() => {
  const id = route.params.id;
  return (Array.isArray(id) ? id[0] : id) || "Nieznane";
});

const socket = io(BACKEND_URL);

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
  });
});

onUnmounted(() => {
  socket.disconnect();
});
</script>
<template>
  <section>
    <h2 class="text-3xl font-bold mb-10">ESP {{ espId }}</h2>

    <!-- <p>{{ lastTemp }}</p> -->
    <!-- <div v-for="(lastValue, key) in allLastValues" :key="key">
      {{ key }}: {{ lastValue ? lastValue : "Oczekiwanie na dane..." }}
    </div> -->
    <div>
      <LiveComponent
        v-for="key in SENSOR_KEYS"
        :key="key"
        :sensorData="key"
        class="mb-10 mx-6 bg-gray-950 p-4 rounded-lg border border-gray-800 shadow"
      />
    </div>

    <!-- <div class="h-72 w-full">
      <Line :data="chartData" :options="chartOptions" />
    </div> -->
  </section>
</template>
