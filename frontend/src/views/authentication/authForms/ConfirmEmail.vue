<script setup lang="ts">
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/yup";
import * as yup from "yup";
import { useUserStore } from "@/stores";

const schema = toTypedSchema(
  yup.object({
    email: yup.string().email().required(),
    code: yup.string().min(6).max(6).required(),
  })
);

const { meta, errors, handleSubmit, isSubmitting, defineField } = useForm({
  validationSchema: schema,
  initialValues: {
    email: "",
    code: "",
  },
});

const [email, emailAttrs] = defineField("email");
const [code, codeAttrs] = defineField("code");
const router = useRouter();

// https://tutorialedge.net/projects/building-imgur-clone-vuejs-nodejs/part-6-login-register-flow/
const onSubmit = handleSubmit(async (values, { setFieldError }) => {
  const userStore = useUserStore();
  const { success, status, message } = await userStore.createUser(
    values.email,
    values.code,
  );
  if (success) {
    // redirect to the dashboard page
    router.push({ name: "Dashboard" });
  } else {
    console.log(status, message);
    let msg: string;
    if (status == 500 || !message) {
      msg = "Unattended server error: contact your app provider.";
    } else {
      msg = message;
    }
    setFieldError("email", msg);
    setFieldError("code", msg);
  }
});

const visible = ref(false);
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

    <div>
      <div
        class="d-flex align-center justify-start text-subtitle-1 text-medium-emphasis"
      >
        Password
      </div>
      <v-text-field
        aria-label="code"
        :type="visible ? 'text' : 'password'"
        v-model="code"
        v-bind="codeAttrs"
        :error-messages="errors.code"
        :append-inner-icon="visible ? 'mdi-eye' : 'mdi-eye-off'"
        @click:append-inner="visible = !visible"
        placeholder="Enter your confirmation code"
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
      Sign up
    </v-btn>
    <div class="d-sm-inline-flex align-center mt-2 mb-7 mb-sm-0 font-weight-bold">
      <h6 class="text-caption">
        By Signing up, you agree to our
        <router-link to="/auth/register" class="text-primary link-hover font-weight-medium">Terms of Service </router-link>
        and
        <router-link to="/auth/register" class="text-primary link-hover font-weight-medium">Privacy Policy</router-link>
      </h6>
</div>

  </form>
</template>
