<script setup lang="ts">
import { RouterView } from 'vue-router';
import AuthHeader from "@/layouts/authentication/AuthHeader.vue";
import HomeFooter from "@/layouts/home/HomeFooter.vue";
</script>

<template>

<AuthHeader />

<v-main>
  <v-container fluid class="pa-0">
    <RouterView />
  </v-container>
</v-main>

<HomeFooter />

</template>
