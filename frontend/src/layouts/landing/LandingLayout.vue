<script setup lang="ts">
import { RouterView } from "vue-router";
import BaseLayout from "@/layouts/BaseLayout.vue";
import LandingHeader from "@/layouts/landing/LandingHeader.vue";
import LandingFooter from "@/layouts/landing/LandingFooter.vue";
</script>

<template>
  <BaseLayout>
    <template #header>
      <LandingHeader />
    </template>

    <RouterView />

    <template #footer>
      <LandingFooter />
    </template>
  </BaseLayout>
</template>
