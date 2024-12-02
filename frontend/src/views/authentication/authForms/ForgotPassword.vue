<script setup lang="ts">
import { useRouter } from "vue-router";
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/yup";
import * as yup from "yup";

import { useUserStore } from "@/stores";

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

const onSubmit = handleSubmit(async (values, { setFieldError }) => {
  const userStore = useUserStore();
  const { success, status, message } = await userStore.forgotPassword(values.email);
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
    <div class="text-h6 mb-6">
      Enter your e-mail address below and we'll send you a link with instructions.
    </div>

    <div class="mb-6">
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
      text="Send"
    ></v-btn>
  </form>
</template>
