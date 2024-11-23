<script setup lang="ts">
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/yup";
import * as yup from "yup";
import { useUserStore } from "@/stores";

const props = defineProps({ token: String });
console.log("Token: ", props.token);

const schema = toTypedSchema(
  yup.object({
    email: yup.string().email().required(),
  })
);

const { meta, errors, handleSubmit, isSubmitting, defineField } = useForm({
  validationSchema: schema,
  initialValues: {
    email: "",
  },
});

const [email, emailAttrs] = defineField("email");
const router = useRouter();
const dialog = ref(false);

const onSubmit = handleSubmit(async (values, { setFieldError }) => {
  // 1. via api, validate the email / token pair
  // 2. if success, inform user its account is activated and propose to log in
  // 3. else if email is a known inactive a user, prose to resend activation email (3 times max)
  // 4. else if max activation attempts reached, delete user, inform and redirect to the sign up page
  // 5. else (unknown email), inform and redirect to the sign up page

  const userStore = useUserStore();
  const { success, status, message } = await userStore.activate(
    values.email,
    props.token ?? ""
  );
  if (success) {
    dialog.value = true
  } else {
    console.log(status, message);
    // let msg: string;
    // if (status == 500 || !message) {
    //   msg = "Unattended server error: contact your app provider.";
    // } else {
    //   msg = message;
    // }
    setFieldError("email", message);
  }
});

const visible = ref(false);

function onConfirm() {
  // Close pop-up dialog and redirect to the log in page
  dialog.value = false;
  router.push({ name: "Login" });
}
</script>

<template>
  <h3 class="text-h3 text-primary text-center mb-0">Sign up and ride!</h3>
  <form @submit="onSubmit" class="mt-7">
    <div class="mb-6">
      <div
        class="d-flex align-center justify-space-between text-subtitle-1 text-medium-emphasis"
      >
        E-mail
        <router-link to="/auth/login" class="text-primary text-decoration-none"
          >Already a member? Log in
        </router-link>
      </div>
      <v-text-field
        aria-label="email address"
        v-model="email"
        v-bind="emailAttrs"
        :error-messages="errors.email"
        placeholder="Email address"
        prepend-inner-icon="mdi-email-outline"
        required
        density="compact"
        variant="outlined"
        hide-details="auto"
        color="primary"
        class="mt-2"
      ></v-text-field>
    </div>

    <v-btn
      type="submit"
      variant="flat"
      size="large"
      block
      color="primary"
      :loading="isSubmitting"
      :disabled="!meta.valid"
      class="mt-5"
    >
      Activate account
    </v-btn>
  </form>
  <v-dialog v-model="dialog" width="auto" persistent>
    <v-card max-width="500" elevation="16">
      <template v-slot:prepend>
        <v-icon icon="mdi-bike" color="primary" class="me-2"></v-icon>
      </template>
      <template v-slot:title>
        <div class="text-h6 font-weight-black text-primary">
          Wellome to the Cycliti community!
        </div>
      </template>
      <v-divider></v-divider>
      <v-card-text class="pa-6">
        <div>
          Your account is now activated. Log in and enjoy Cycliti!
        </div>
      </v-card-text>
      <template v-slot:actions>
        <v-btn
          color="primary"
          rounded="xl"
          variant="flat"
          class="ms-auto"
          text="Log in"
          @click="onConfirm"
        ></v-btn>
      </template>
    </v-card>
  </v-dialog>
</template>
