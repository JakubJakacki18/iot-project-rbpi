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
    <body
      class="mx-auto flex min-h-screen w-full flex-col bg-gray-800 text-gray-300"
    >
      <Header />
      <Body />
      <Footer />
    </body>
  </html>
</template>

<style scoped></style>
