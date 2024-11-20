<script setup lang="ts">
import { RouterView } from "vue-router";
import { useConfigStore } from "@/stores";
import { computed, type ComputedRef } from "vue";

/** Config Store */
const configStore = useConfigStore();

/** Toggle Dark mode */
const isDark: ComputedRef<string> = computed(() =>
  configStore.isDarkTheme ? "dark" : "light"
);
</script>

<template>
  <v-app :theme="isDark">
    <RouterView></RouterView>
  </v-app>
</template>
