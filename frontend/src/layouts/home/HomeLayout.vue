<script setup lang="ts">
import { RouterView } from "vue-router";
import BaseLayout from "@/layouts/BaseLayout.vue";
import HomeHeader from "@/layouts/home/HomeHeader.vue";
// import LandingFooter from "@/layouts/landing/LandingFooter.vue";
</script>

<template>
  <BaseLayout>
    <template #header>
      <HomeHeader />
    </template>

    <RouterView />

    <!-- <template #footer>
      <LandingFooter />
    </template> -->
  </BaseLayout>
</template>
