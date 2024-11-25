<script setup lang="ts">
import { RouterView } from "vue-router";
import BaseLayout from "@/layouts/BaseLayout.vue";
import HomeHeader from "@/layouts/home/HomeHeader.vue";
import HomeFooter from "@/layouts/home/HomeFooter.vue";
</script>

<template>
  <BaseLayout>
    <template #header>
      <HomeHeader />
    </template>

    <RouterView />

    <template #footer>
      <HomeFooter />
    </template>
  </BaseLayout>
</template>
