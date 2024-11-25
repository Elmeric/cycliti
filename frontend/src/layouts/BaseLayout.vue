<template>
  <slot name="header"></slot>

  <v-main>
    <v-container fluid class="pa-0">
      <slot></slot>
    </v-container>
  </v-main>

  <slot name="footer"></slot>
</template>
