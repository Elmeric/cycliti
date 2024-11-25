<script setup lang="ts">
import { RouterView } from "vue-router";
import BaseLayout from "@/layouts/BaseLayout.vue";
import AuthHeader from "@/layouts/authentication/AuthHeader.vue";
import HomeFooter from "@/layouts/home/HomeFooter.vue";
</script>

<template>
  <BaseLayout>
    <template #header>
      <AuthHeader />
    </template>

    <RouterView />

    <template #footer>
      <HomeFooter />
    </template>
  </BaseLayout>
</template>
