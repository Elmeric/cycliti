<script setup lang="ts">
import CenteredForm from "@/components/CenteredForm.vue";
import ConfirmEmail from "@/views/authentication/authForms/ConfirmEmail.vue";

const props = defineProps<{
  query: string;
}>();
console.log(props);
console.log(props.query);
</script>

<template>
  <CenteredForm>
    <ConfirmEmail :token="props.query" />
  </CenteredForm>
</template>
