<script setup lang="ts">
import { useConfigStore } from "@/stores";
import { computed } from "vue";

const configStore = useConfigStore();

defineProps(["imgFallback", "sourcePaths"]);

const imgFilter = computed(() => {
  return configStore.isDarkTheme
    ? { filter: "contrast(75%) brightness(25%) blur(3px)" }
    : { filter: "contrast(25%) brightness(160%) blur(3px)" };
});
</script>

<template>
  <v-img height="100%" position="center" cover :src="imgFallback" class="blur">
    <template #sources>
      <source
        v-for="(imgPath, idx) in sourcePaths"
        :key="idx"
        :srcset="imgPath"
      />
    </template>
  </v-img>
</template>

<style scoped>
.v-img.blur :deep(img) {
  filter: v-bind("imgFilter.filter");
}
</style>
