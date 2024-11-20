<script setup lang="ts">
import AuthRegister from '@/views/authentication/authForms/AuthRegister.vue';
</script>

<template>
  <v-row class="position-relative bg-home" no-gutters>
    <v-col cols="12" class="d-flex align-center">
      <v-container>
        <div 
          class="d-flex align-center justify-center" 
          style="min-height: calc(100vh - 148px)"
        >
          <v-row justify="center">
            <v-col cols="12">
              <v-card elevation="24" max-width="30rem" class="mx-auto my-0">

                <v-card-text class="pa-sm-10 pa-6">
                  <AuthRegister />
                </v-card-text>
                
              </v-card>
            </v-col>
          </v-row>
        </div>
      </v-container>
    </v-col>
  </v-row>
</template>
