<script setup lang="ts">
import NavButton from "./NavButton.vue";

const lista: { to: string; label: string }[] = [];
for (let i = 0; i < 3; i++) {
  lista.push({
    to: `/esp/${i + 1}`,
    label: `Dane z ESP${i + 1}`,
  });
}
const navItems = [{ to: "/", label: "Dashboard" }, ...lista];
</script>
<template>
  <header class="w-full border-b border-gray-700 bg-gray-900">
    <nav class="bg-gray-900 text-white flex flex-row shadow-xl">
      <div class="w-64 p-6 bg-gray-950 rounded-br-2xl border-r border-gray-800">
        <h2 class="text-center text-2xl font-bold tracking-wider text-blue-400">
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
    </nav>
  </header>
</template>
