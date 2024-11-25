<script setup lang="ts">
defineProps<{
  title: string;
  text: string;
}>();

const visible = defineModel<boolean>({ required: true })

defineEmits<{
  close: [];
}>();
</script>

<template>
  <v-dialog v-model="visible" width="auto" persistent>
    <v-card max-width="500" elevation="16">
      <template v-slot:prepend>
        <v-icon icon="mdi-bike" color="primary" class="me-2"></v-icon>
      </template>
      <template v-slot:title>
        <div class="text-h6 font-weight-black text-primary">
          {{ title }}
        </div>
      </template>
      <v-divider></v-divider>
      <v-card-text class="pa-6">
        <div>
          {{ text }}
        </div>
      </v-card-text>
      <template v-slot:actions>
        <v-btn
          color="primary"
          rounded="xl"
          variant="flat"
          class="ms-auto"
          text="Close"
          @click="$emit('close')"
        ></v-btn>
      </template>
    </v-card>
  </v-dialog>
</template>
