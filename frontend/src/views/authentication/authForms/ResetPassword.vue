<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/yup";
import * as yup from "yup";

import { useUserStore } from "@/stores";

const props = defineProps<{
  nonce: string;
}>();
console.log("Nonce: ", props.nonce);

const schema = toTypedSchema(
  yup.object({
    email: yup.string().email().required(),
    password: yup.string().min(8).max(64).required(),
  })
);

const { meta, errors, handleSubmit, isSubmitting, defineField } = useForm({
  validationSchema: schema,
  initialValues: {
    email: "",
    password: "",
  },
});

const [email, emailAttrs] = defineField("email");
const [password, passwordAttrs] = defineField("password");
const router = useRouter();
const isVisiblePwd = ref(false);

const onSubmit = handleSubmit(async (values, { setFieldError }) => {
  const userStore = useUserStore();
  const { success, status, message } = await userStore.resetPassword(
    values.email,
    values.password,
    props.nonce ?? ""
  );
  if (success) {
    router.push({
      name: "Login",
      query: { msg: message },
    });
  } else {
    console.log(status, message);
    setFieldError("email", message);
  }
});
</script>

<template>
  <h3 class="text-h3 text-primary text-center mb-0">Reset your password</h3>

  <form @submit="onSubmit" class="mt-7">
    <div class="mb-6">
      <div
        class="d-flex align-center justify-space-between text-subtitle-1 text-medium-emphasis"
      >
        E-mail
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
      text="Reset password"
    ></v-btn>
  </form>
</template>
