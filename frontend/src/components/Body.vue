<script setup lang="ts"></script>
<template>
  <main class="flex-1 flex justify-center px-4 py-6">
    <router-view
      v-slot="{ Component }"
      class="m-4 p-4 w-full h-full bg-gray-900 rounded-xl shadow"
    >
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </main>
</template>
