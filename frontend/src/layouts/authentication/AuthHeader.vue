<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useUIStore } from "@/stores";
import ToolbarProgressIndicator from "@/components/ToolbarProgressIndicator.vue";

const appTitle = import.meta.env.VITE_APP_TITLE;

const uiStore = useUIStore();
const { isLoading } = storeToRefs(uiStore);
</script>

<template>
  <v-toolbar color="surface" density="default" flat class="px-2 text-primary">
    <v-toolbar-title class="text-h4 font-weight-black">
      <RouterLink 
      :to="{ name: 'Home' }"
      aria-label="logo" 
        class="text-h4 font-weight-black text-primary text-decoration-none"
      >
        <v-icon icon="mdi-bike" color="primary" class="me-2"></v-icon>
        {{ appTitle }}
      </RouterLink>
    </v-toolbar-title>

    <ToolbarProgressIndicator :loading="isLoading" color="primary" />

  </v-toolbar>
</template>
