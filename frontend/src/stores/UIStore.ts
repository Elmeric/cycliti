import { defineStore } from "pinia";
import { ref, type Ref } from "vue";

export default defineStore("ui", () => {
  const isLoading: Ref<boolean> = ref(false);

  return {
    isLoading,
  };
});
