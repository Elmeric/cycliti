<script setup lang="ts">

defineProps(["loading", "color"]);

</script>

<template>
  <v-progress-linear
    :active="loading"
    :indeterminate="loading"
    :color="color"
    absolute
    bottom
  ></v-progress-linear>

</template>