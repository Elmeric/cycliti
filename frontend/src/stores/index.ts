import { createPinia, type Pinia } from "pinia";

import piniaPluginPersistedstate from "pinia-plugin-persistedstate";

// Pinia Stores
import useConfigStore from "@/stores/ConfigStore";
import useGlobalStore from "@/stores/GlobalStore";
import useUIStore from "@/stores/UIStore";
import useAuthStore from "@/stores/AuthStore";
import useUserStore from "@/stores/UserStore";

/** Pinia Store */
const pinia: Pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

export default pinia;

export { useConfigStore, useGlobalStore, useUIStore, useAuthStore, useUserStore };
