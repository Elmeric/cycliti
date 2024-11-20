import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "@/App.vue";
import { router } from "@/router";
import vuetify from "@/plugins/vuetify";
import '@/styles/shared-styles.scss';

import { fakeBackend } from "./utils/helpers/fake-backend";

//i18
import { createI18n } from "vue-i18n";
import messages from "@/utils/locales/messages";

const i18n = createI18n({
  locale: "en",
  messages: messages,
  silentTranslationWarn: true,
  silentFallbackWarn: true,
});

const app = createApp(App);

fakeBackend();

app.use(router);
app.use(createPinia());
app.use(i18n);
app.use(vuetify);

// Run!
router
  .isReady()
  .then(() => app.mount("#app"))
  .catch((e: any) => console.error(e));

// app.mount('#app')
