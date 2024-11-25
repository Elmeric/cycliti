<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/yup";
import * as yup from "yup";

import { useUserStore } from "@/stores";
import ConfirmDialog from "@/components/ConfirmationDialog.vue"

const props = defineProps<{
  token: string;
}>();
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
  const userStore = useUserStore();
  const { success, status, message } = await userStore.activate(
    values.email,
    props.token ?? ""
  );
  if (success) {
    dialog.value = true
  } else {
    console.log(status, message);
    setFieldError("email", message);
  }
});

function onConfirm() {
  // Close pop-up dialog and redirect to the log in page
  dialog.value = false;
  router.push({ name: "Login" });
}
</script>

<template>
  <h3 class="text-h3 text-primary text-center mb-0">Activate your account</h3>
  
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

    <v-btn
      type="submit"
      variant="flat"
      size="large"
      block
      color="primary"
      :loading="isSubmitting"
      :disabled="!meta.valid"
      class="mt-5"
      text="Confirm email"
    ></v-btn>
  </form>

  <ConfirmDialog 
    v-model="dialog"
    title="Wellcome to Cycliti!"
    text="Your account is now activated. Log in and enjoy Cycliti!"
    @close="onConfirm"
  ></ConfirmDialog>
</template>
