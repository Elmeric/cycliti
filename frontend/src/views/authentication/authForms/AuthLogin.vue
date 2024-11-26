<script setup lang="ts">
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/yup";
import * as yup from "yup";

import { useAuthStore } from "@/stores";

const schema = toTypedSchema(
  yup.object({
    email: yup.string().email().required(),
    password: yup.string().min(8).max(64).required(),
    keepMe: yup.boolean().default(false),
  })
);

const { meta, errors, handleSubmit, isSubmitting, defineField } = useForm({
  validationSchema: schema,
  initialValues: {
    email: "",
    password: "",
    keepMe: false,
  },
});

const [email, emailAttrs] = defineField("email");
const [password, passwordAttrs] = defineField("password");
const [keepMe, keepMeAttrs] = defineField("keepMe");
const router = useRouter();
const route = useRoute();
const isVisiblePwd = ref(false);

const onSubmit = handleSubmit(async (values, { setFieldError }) => {
  const authStore = useAuthStore();
  const { success, status, message } = await authStore.authenticate(
    values.email,
    values.password,
    values.keepMe
  );
  if (success) {
    // redirect to previous url or default to home page
    const redirs = route.query.redirect;
    let redir: string;
    if (Array.isArray(redirs)) {
      redir = redirs[0] as string;
    } else redir = redirs as string;
    router.push(redir || { name: "Dashboard" });
  } else {
    setFieldError("email", message);
    setFieldError("password", message);
  }
});

</script>

<template>
  <h3 class="text-h3 text-primary text-center mb-0">Log in</h3>
  
  <form @submit="onSubmit" class="mt-7">
    <div class="mb-6">
      <div
        class="d-flex align-center justify-space-between text-subtitle-1 text-medium-emphasis"
      >
        Account
        <router-link to="/auth/register" class="text-primary text-decoration-none"
          >Don't have an account?
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

    <div>
      <div
        class="d-flex align-center justify-space-between text-subtitle-1 text-medium-emphasis"
      >
        Password
        <router-link to="/auth/login" class="text-primary text-decoration-none">
          Forgot Password?
        </router-link>
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
        required
        density="compact"
        variant="outlined"
        hide-details="auto"
        color="primary"
        class="mt-2"
      ></v-text-field>
    </div>

    <div class="d-flex align-center mt-4 mb-7 mb-sm-0">
      <v-checkbox
        v-model="keepMe"
        v-bind="keepMeAttrs"
        label="Keep me sign in"
        hide-details
        color="primary"
        class="ms-n2"
      ></v-checkbox>
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
      text="Log in"
    >
    </v-btn>
  </form>
</template>
