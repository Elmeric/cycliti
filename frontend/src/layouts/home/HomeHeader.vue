<script setup lang="ts">
import { shallowRef } from "vue";
import { storeToRefs } from "pinia";
import { useUIStore } from "@/stores";
import ToolbarProgressIndicator from "@/components/ToolbarProgressIndicator.vue";
import AppBarToggleDarkMode from "@/components/AppBarToggleDarkMode.vue";

const appTitle = import.meta.env.VITE_APP_TITLE;
const headerLinks = shallowRef([
  {
    id: 1,
    title: "Features",
    link: "/home/features",
    icon: "mdi-eye",
  },
  {
    id: 2,
    title: "Help",
    link: "/help",
    icon: "mdi-help",
  },
]);

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

    <v-spacer></v-spacer>

    <v-toolbar-items class="hidden-sm-and-down">
      <v-btn
        v-for="item in headerLinks"
        :key="item.id"
        :to="item.link"
        :prepend-icon="item.icon"
        variant="flat"
        size="large"
        class="px-8 text-primary font-weight-bold"
      >
        {{ item.title }}
      </v-btn>

      <v-btn
        prepend-icon="mdi-login"
        to="/auth/login"
        variant="elevated"
        color="secondary"
        size="x-large"
        class="mx-16"
      >
        Log in
      </v-btn>
    </v-toolbar-items>

    <AppBarToggleDarkMode />

    <v-menu class="hidden-md-and-up">
      <template v-slot:activator="{ props }">
        <v-btn
          class="bg-surface on-surface hidden-md-and-up"
          icon="mdi-dots-vertical"
          variant="flat"
          v-bind="props"
        >
        </v-btn>
      </template>
      <v-list>
        <v-list-item v-for="item in headerLinks" :key="item.id">
          <v-btn
            :prepend-icon="item.icon"
            :to="item.link"
            variant="flat"
            class="text-primary font-weight-bold"
          >
            {{ item.title }}
          </v-btn>
        </v-list-item>

        <v-list-item>
          <v-btn
            prepend-icon="mdi-login"
            to="/auth/login"
            variant="elevated"
            color="secondary"
          >
            Log in
          </v-btn>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-toolbar>
</template>
