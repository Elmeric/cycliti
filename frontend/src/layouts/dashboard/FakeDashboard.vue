<script setup lang="ts">
import { onMounted, ref, type Ref } from "vue";
import { useAuthStore, useUserStore } from "@/stores";
import { storeToRefs } from "pinia";

const authStore = useAuthStore();
const userStore = useUserStore();
const currentUser = storeToRefs(userStore).currentUser;
const loading = ref(true);
const msg: Ref<string | undefined> = ref(undefined);

onMounted(async () => {
  const { success, message } = await userStore.getCurrentUser();
  if (!success) {
    msg.value = message;
  }
  loading.value = false;
});
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
            <div class="ml-auto">
              <v-btn
                variant="text"
                color="primary"
                rounded="sm"
                icon
                size="large"
                @click="authStore.logout()"
              >
                <v-icon
                  :style="{ fontSize: '20px' }"
                  icon="mdi-logout"
                  end
                >
                </v-icon>
              </v-btn>
            </div>

          </div>
        </div>
      </div>
    </v-container>
  </v-main>
</template>
