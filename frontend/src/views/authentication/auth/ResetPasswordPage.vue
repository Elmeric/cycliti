<script setup lang="ts">
import CenteredForm from "@/components/CenteredForm.vue";
import ConfirmEmail from "@/views/authentication/authForms/ResetPassword.vue";

const props = defineProps<{
  nonce: string;
}>();
console.log(props);
console.log(props.nonce);
</script>

<template>
  <CenteredForm>
    <ConfirmEmail :nonce="props.nonce" />
  </CenteredForm>
</template>
