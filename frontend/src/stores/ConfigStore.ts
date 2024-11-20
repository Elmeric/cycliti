import { defineStore } from "pinia";
import { ref, type Ref } from "vue";

/** Config Store */
export default defineStore(
  "config",
  () => {
    /** Dark Theme mode */
    const isDarkTheme: Ref<boolean> = ref(
      window.matchMedia("(prefers-color-scheme: dark)").matches
    );

    const locale: Ref<string> = ref(
      window.navigator.languages[0] ?? window.navigator.language
    );

    /** Toggle Dark/Light mode */
    const toggleTheme = () => (isDarkTheme.value = !isDarkTheme.value);
    /**
     * Set Locale.
     *
     * @param locale - Locale
     */
    const setLocale = (l: string) => (locale.value = l);

    return { isDarkTheme, toggleTheme, setLocale };
  },
  {
    // Data persistence destination
    persist: {
      key: import.meta.env.VITE_WEBSTORAGE_NAMESPACE ?? "vuetify",
      storage: window.sessionStorage,
    },
  }
);
