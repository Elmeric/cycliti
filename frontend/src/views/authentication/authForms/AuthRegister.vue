<script setup lang="ts">
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/yup";
import * as yup from "yup";
import { useUserStore } from "@/stores";

const schema = toTypedSchema(
  yup.object({
    email: yup.string().email().required(),
    username: yup.string().min(4).max(16).required(),
    password: yup.string().min(8).max(64).required(),
  })
);

const { meta, errors, handleSubmit, isSubmitting, defineField } = useForm({
  validationSchema: schema,
  initialValues: {
    email: "",
    username: "",
    password: "",
  },
});

const [email, emailAttrs] = defineField("email");
const [username, usernameAttrs] = defineField("username");
const [password, passwordAttrs] = defineField("password");
const router = useRouter();
const visible = ref(false);
const dialog = ref(false);

// watch(email, (newValue) => {
//       username.value = `${newValue.split("@")[0]}`;
//       // or
//       // setFieldValue('email',  `${newValue}@gmail.com`);
//     });

// https://tutorialedge.net/projects/building-imgur-clone-vuejs-nodejs/part-6-login-register-flow/
const onSubmit = handleSubmit(async (values, { setFieldError }) => {
  const userStore = useUserStore();
  const { success, status, message } = await userStore.createUser(
    values.email,
    values.username,
    values.password
  );
  if (success) {
    // Show email confirmation dialog
    dialog.value = true;
  } else {
    console.log(status, message);
    let msg: string;
    if (status == 500 || !message) {
      msg = "Unattended server error: contact your app provider.";
    } else {
      msg = message;
    }
    setFieldError("email", msg);
    setFieldError("username", msg);
    setFieldError("password", msg);
  }
});

function onConfirm() {
  // Close pop-up dialog and redirect to the landing page
  dialog.value = false;
  router.push({ name: "Home" });
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

    <div class="mb-6">
      <div
        class="d-flex align-center justify-start text-subtitle-1 text-medium-emphasis"
      >
        Nickname
      </div>
      <v-text-field
        aria-label="user name"
        v-model="username"
        v-bind="usernameAttrs"
        :error-messages="errors.username"
        placeholder="Displayed name"
        prepend-inner-icon="mdi-account-outline"
        required
        density="compact"
        variant="outlined"
        hide-details="auto"
        color="primary"
        class="mt-2"
      ></v-text-field>
    </div>

    <div>
      <div
        class="d-flex align-center justify-start text-subtitle-1 text-medium-emphasis"
      >
        Password
      </div>
      <v-text-field
        aria-label="password"
        :type="visible ? 'text' : 'password'"
        v-model="password"
        v-bind="passwordAttrs"
        :error-messages="errors.password"
        :append-inner-icon="visible ? 'mdi-eye' : 'mdi-eye-off'"
        @click:append-inner="visible = !visible"
        placeholder="Enter your password"
        prepend-inner-icon="mdi-lock-outline"
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
      Verify email >
    </v-btn>
    <div class="d-sm-inline-flex align-center mt-2 mb-7 mb-sm-0 font-weight-bold">
      <h6 class="text-caption">
        By Signing up, you agree to our
        <router-link
          to="/auth/register"
          class="text-primary link-hover font-weight-medium"
          >Terms of Service
        </router-link>
        and
        <router-link
          to="/auth/register"
          class="text-primary link-hover font-weight-medium"
          >Privacy Policy</router-link
        >
      </h6>
    </div>
  </form>
  <v-dialog v-model="dialog" width="auto" persistent>
    <v-card
      max-width="500"
      elevation="16"
    >
      <template v-slot:prepend>
        <v-icon icon="mdi-bike" color="primary" class="me-2"></v-icon>
      </template>
      <template v-slot:title>
        <div class="text-h6 font-weight-black text-primary">
           One more step to join the Cycliti community! 
        </div> 
      </template>
      <v-divider></v-divider>
      <v-card-text class="pa-6">
        <div>
          A link to activate your account has been emailed to the address provided.
        </div>
      </v-card-text>
      <template v-slot:actions>
        <v-btn 
          color="primary"
          rounded="xl"
          variant="flat"
          class="ms-auto" 
          text="Ok" 
          @click="onConfirm"
        ></v-btn>
      </template>
    </v-card>
  </v-dialog>
</template>
