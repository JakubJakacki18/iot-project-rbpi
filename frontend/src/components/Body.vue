<script setup lang="ts"></script>
<template>
  <main class="flex-1 flex justify-center px-10 py-8 overflow-y-auto">
    <div class="p-10 w-full h bg-gray-900 rounded-xl shadow self-start">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
  </main>
</template>
