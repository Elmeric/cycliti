<script setup lang="ts">
import { useConfigStore } from "@/stores";

/** Config Store */
const configStore = useConfigStore();
</script>

<template>
  <!-- Toggle Dark mode -->
  <v-btn
    class="bg-surface on-surface"
    icon="mdi-theme-light-dark"
    variant="flat"
    @click="configStore.toggleTheme"
  />
</template>
