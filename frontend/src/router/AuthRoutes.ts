import type { RouteLocationNormalized } from "vue-router";

const AuthRoutes = {
  path: "/auth",
  component: () => import("@/layouts/authentication/AuthLayout.vue"),
  meta: {
    requiresAuth: false,
  },
  children: [
    {
      name: "Login",
      path: "login",
      component: () => import("@/views/authentication/auth/LoginPage.vue"),
      // props: (route: RouteLocationNormalized) => ({ msg: route.query.msg }),
    },
    {
      name: "Register",
      path: "register",
      component: () => import("@/views/authentication/auth/RegisterPage.vue"),
    },
    {
      name: "ForgotPassword",
      path: "forgot-password",
      component: () => import("@/views/authentication/auth/ForgotPasswordPage.vue"),
    },
    {
      name: "ResetPassword",
      path: "reset-password",
      component: () => import("@/views/authentication/auth/ResetPasswordPage.vue"),
      props: (route: RouteLocationNormalized) => ({ nonce: route.query.nonce }),
      beforeEnter: (to: RouteLocationNormalized, from: RouteLocationNormalized) => {
        if (to.query.nonce == null) {
          console.log("A nonce query string is required")
          return false
        }
      },
    },
    {
      name: "ConfirmEmail",
      path: "activate",
      component: () => import("@/views/authentication/auth/ConfirmEmailPage.vue"),
      props: (route: RouteLocationNormalized) => ({ nonce: route.query.nonce }),
      beforeEnter: (to: RouteLocationNormalized, from: RouteLocationNormalized) => {
        if (to.query.nonce == null) {
          console.log("A nonce query string is required")
          return false
        }
      },
    },
    {
      name: "Error 404",
      path: "pages/error",
      component: () => import("@/views/pages/maintenance/error/Error404Page.vue"),
    },
  ],
};

export default AuthRoutes;
