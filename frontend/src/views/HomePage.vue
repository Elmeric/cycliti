<template>
  <v-row class="position-relative bg-home" no-gutters>
    <v-col cols="12" class="d-flex align-center">
      <v-sheet
        class="d-flex flex-wrap align-center justify-center text-center mx-auto"
        elevation="0"
        height="calc(100dvh - 104px)"
        color="transparent"
      >
        <div class="pa-4 bg-surface rounded-xl">
          <v-icon icon="mdi-bike" color="primary" size="x-large"></v-icon>

          <h2 class="text-h4 font-weight-black text-primary mb-4">
            Welcome on Cycliti!
          </h2>

          <div class="text-h5 font-weight-medium mb-10">
            Sign up to plan your next circuit. Enjoy!
          </div>

          <p class="text-body-1 mb-6">
            Already a member:
            <span>
              <v-btn
                prepend-icon="mdi-login"
                to="/auth/login"
                variant="elevated"
                color="secondary  font-weight-bold"
                size="small"
              >
                Log in
              </v-btn>
            </span>
          </p>

          <v-btn
            to="/auth/register"
            color="primary"
            variant="elevated"
            size="x-large"
            block
            class="mb-2"
          >
            Sign up here !
          </v-btn>

          <p class="text-body-2">
            By signing up for Cycliti, you agree to the
            <span>
              <router-link to="/legal/terms" class="text-secondary text-decoration-none"
                >Terms of Service</router-link
              > </span
            >. View our
            <span>
              <router-link
                to="/legal/privacy"
                class="text-secondary text-decoration-none"
                >Privacy Policy</router-link
              > </span
            >.
          </p>
        </div>
      </v-sheet>
    </v-col>
  </v-row>
</template>
