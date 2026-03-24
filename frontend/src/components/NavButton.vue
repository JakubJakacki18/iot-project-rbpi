<script setup lang="ts">
import { RouterLink } from "vue-router";
defineProps<{
  label: string;
  to: string;
}>();
</script>
<template>
  <RouterLink
    :to="to"
    class="w-full px-4 py-3 rounded-lg transition-colors font-medium text-gray-300 hover:bg-gray-800 hover:text-white"
    active-class="bg-blue-600 text-white"
  >
    {{ label }}
  </RouterLink>
</template>
<style scoped></style>
