<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useForm, useIsFieldValid } from "vee-validate";
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

const { meta, errors, handleSubmit, isSubmitting, defineField, setFieldError } =
  useForm({
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
const isVisiblePwd = ref(false);
const isValidEmail = useIsFieldValid("email");

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
    router.push({
      name: "Landing",
      query: { msg: message },
    });
  } else {
    console.log(status, message);
    setFieldError("email", message);
    setFieldError("username", message);
    setFieldError("password", message);
  }
});

async function onResend() {
  console.log("onResend");
  const userStore = useUserStore();
  const { success, status, message } = await userStore.resendEmail(email.value ?? "");
  console.log("onResend: ", success);
  if (success) {
    router.push({
      name: "Landing",
      query: { msg: message },
    });
  } else {
    console.log(status, message);
    setFieldError("email", message);
  }
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
        <v-btn
          type="submit"
          variant="text"
          size="small"
          text="Resend activation email"
          class="text-primary"
          :disabled="!isValidEmail"
          @click="onResend"
        >
        </v-btn>
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
        :type="isVisiblePwd ? 'text' : 'password'"
        v-model="password"
        v-bind="passwordAttrs"
        :error-messages="errors.password"
        :append-inner-icon="isVisiblePwd ? 'mdi-eye' : 'mdi-eye-off'"
        @click:append-inner="isVisiblePwd = !isVisiblePwd"
        placeholder="Enter your password"
        prepend-inner-icon="mdi-lock-outline"
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
      text="Sign up"
    ></v-btn>
    <div class="d-sm-inline-flex align-center mt-2 mb-7 mb-sm-4 font-weight-bold">
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
    <v-divider thichness="6" class="border-opacity-100" color="info"></v-divider>
    <div
      class="d-flex align-center justify-center text-subtitle-1 text-medium-emphasis mt-4"
    >
      <router-link to="/auth/login" class="text-primary text-decoration-none"
        >Already a member? Log in
      </router-link>
    </div>
  </form>
</template>
