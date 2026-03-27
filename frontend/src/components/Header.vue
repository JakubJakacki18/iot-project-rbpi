<script setup lang="ts">
import NavButton from "./NavButton.vue";
import { ref } from "vue";

const menuOpen = ref(false);

const lista: { to: string; label: string }[] = [];
for (let i = 0; i < 3; i++) {
  lista.push({
    to: `/esp/${i + 1}`,
    label: `Dane z ESP${i + 1}`,
  });
}
const navItems = [{ to: "/", label: "Dashboard" }, ...lista];
</script>
<!-- <template>
  <header
    class="flex flex-row flex-none justify-between z-50 border-b border-gray-700 bg-gray-900"
  >
    <div
      class="w-64 p-4 bg-gray-950 rounded-br-2xl border-r border-gray-800 flex items-center justify-center text-center"
    >
      <h2
        class="text-center text-xl lg:text-2xl font-bold tracking-wider text-blue-400"
      >
        IoT Project
      </h2>
    </div>
    <div class="px-4 py-6 space-x-2 space-y-2 items-center ml-auto mr-0">
      <NavButton
        v-for="item in navItems"
        :key="item.to"
        :label="item.label"
        :to="item.to"
      />
    </div>
  </header>
</template> -->
<template>
  <header class="relative">
    <div
      class="flex flex-row flex-none justify-between z-50 border-b border-gray-700 bg-gray-900"
    >
      <!-- Logo / Tytuł -->
      <div
        class="w-64 p-4 bg-gray-950 rounded-br-2xl border-r border-gray-800 flex items-center justify-center text-center"
      >
        <h2
          class="text-center text-xl lg:text-2xl font-bold tracking-wider text-blue-400"
        >
          IoT Project
        </h2>
      </div>

      <!-- Hamburger (mobile < lg) -->
      <button
        class="lg:hidden p-2 rounded-md hover:bg-gray-800 ml-auto mr-4"
        @click="menuOpen = !menuOpen"
      >
        <svg
          class="w-6 h-6 text-gray-300"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </button>

      <!-- Menu desktop (>= lg) -->
      <div
        class="hidden lg:block px-4 py-6 space-x-2 space-y-2 items-center text-center ml-auto mr-0"
      >
        <NavButton
          v-for="item in navItems"
          :key="item.to"
          :label="item.label"
          :to="item.to"
        />
      </div>

      <!-- Menu mobilne (< lg) -->
    </div>
    <div
      v-if="menuOpen"
      class="lg:hidden absolute top-full right-4 bg-gray-950 shadow-md rounded-md p-4 flex flex-col gap-2 z-50"
    >
      <NavButton
        v-for="item in navItems"
        :key="item.to"
        :label="item.label"
        :to="item.to"
        @click="menuOpen = false"
      />
    </div>
  </header>
</template>
