<script setup lang="ts">
import { shallowRef } from "vue";

const footerLinks = shallowRef([
  {
    id: 1,
    title: "Terms and Conditions",
    link: "/legal/terms",
  },
  {
    id: 2,
    title: "Privacy Policy",
    link: "/legal/privacy",
  },
]);
</script>

<template>
  <v-footer min-height="3rem">
    <v-row justify="center" no-gutters>
      <!-- <v-col cols="12" md="6" class="text-md-left text-center">
        <p class="text-subtitle-2 mb-md-0 mb-4">
          Cycliti protects your data. Read more in our
          <router-link to="/legal/privacy" class="text-secondary text-decoration-none">
            Privacy Policy
          </router-link>
        </p>
      </v-col> -->
      <v-col
        class="d-flex flex-md-row flex-column justify-md-end align-center"
        cols="12"
      >
        <p class="text-subtitle-2 mx-md-0 mx-2 mb-md-0 mb-4">
          Cycliti protects your data. Read more in our
          <router-link to="/legal/privacy" class="text-secondary text-decoration-none">
            Privacy Policy
          </router-link>
        </p>
        <v-spacer></v-spacer>
        <router-link
          v-for="item in footerLinks"
          :key="item.id"
          :to="{ path: item.link }"
          class="mx-md-3 mx-2 mb-md-0 mb-2 text-subtitle-2 text-secondary text-decoration-none"
        >
          {{ item.title }}
        </router-link>
        <a href="https://strava.com">
          <img class="strava-img" src="@/assets/images/powered-by-strava.svg" />
        </a>
      </v-col>
    </v-row>
  </v-footer>
</template>

<style lang="scss">
.strava-img {
  height: 30px;
}
</style>
