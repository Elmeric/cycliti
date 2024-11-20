<script setup lang="ts">
import { RouterView } from "vue-router";
import HomeHeader from "@/layouts/home/HomeHeader.vue";
import HomeFooter from "@/layouts/home/HomeFooter.vue";
</script>

<template>

  <HomeHeader />  

  <v-main>
    <v-container fluid class="pa-0">
      <RouterView />
    </v-container>
  </v-main>

  <HomeFooter />
</template>
