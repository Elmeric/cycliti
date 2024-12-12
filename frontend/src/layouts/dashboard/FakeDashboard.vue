<script setup lang="ts">
import { onMounted, ref, type Ref } from "vue";
import { useAuthStore, useUserStore } from "@/stores";
// import { storeToRefs } from "pinia";
import type { UserIn } from "@/models/User";

const authStore = useAuthStore();
const userStore = useUserStore();
// const currentUser = storeToRefs(userStore).currentUser;
const currentUser = ref<UserIn | null>(null);
const loading = ref(true);
const msg: Ref<string | undefined> = ref(undefined);
// const count = ref(0);

onMounted(async () => {
  const { success, content, message } = await userStore.getCurrentUser();
  if (!success) {
    msg.value = message;
  } else {
    currentUser.value = content
  }
  loading.value = false;
});

async function connectWithStrava(e: any) {
  // count.value++;
  // console.log("Connect with strava clicked!", count.value);
  if (currentUser.value === null) {
    msg.value = "A current user shall exists!"
  } else {
    userStore.linkToStrava(currentUser.value.id.toString())
  }
}
</script>

<template>
  <v-main>
    <v-container class="pa-0">
      <div class="d-flex align-center justify-center" style="min-height: 100vh">
        <v-progress-circular
          v-if="loading"
          color="primary"
          indeterminate
          size="75"
          width="10"
        ></v-progress-circular>
        <div v-else>
          <div v-if="msg">
            <p>Cannot get your username: {{ msg }}</p>
          </div>
          <div v-else>
            <p>Your username is: {{ currentUser?.username }}</p>
            <v-card
              class="d-flex flex-column mx-auto my-4 align-center"
              max-width="344"
              title="Connect to your Strava account"
            >
              <v-btn
                stacked
                color="primary"
                variant="outlined"
                size="x-small"
                @click="connectWithStrava"
                class="my-4"
              >
                <img class="strava-img" src="@/assets/images/connect-with-strava.svg" />
              </v-btn>
            </v-card>
            <div class="ml-auto">
              <v-btn
                variant="text"
                color="primary"
                rounded="sm"
                icon
                size="large"
                @click="authStore.logout()"
              >
                <v-icon :style="{ fontSize: '20px' }" icon="mdi-logout" end> </v-icon>
              </v-btn>
            </div>
          </div>
        </div>
      </div>
    </v-container>
  </v-main>
</template>

<style lang="scss">
.strava-img {
  height: 48px;
}
</style>
