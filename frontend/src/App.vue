<script setup lang="ts">
import { computed, shallowRef } from "vue";

import Header from "./components/Header.vue";
import Footer from "./components/Footer.vue";
import Body from "./components/Body.vue";
</script>

<template>
  <!doctype html>
  <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>IoT</title>
      <link
        rel="stylesheet"
        href="{{url_for('static',filename='dist/output.css')}}"
      />
    </head>
    <body>
      <div
        class="bg-gray-800 text-gray-300 h-screen flex flex-col overflow-hidden"
      >
        <Header />
        <Body />
        <Footer />
      </div>
    </body>
  </html>
</template>

<style scoped></style>
