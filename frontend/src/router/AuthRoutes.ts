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
    },
    {
      name: "Register",
      path: "register",
      component: () => import("@/views/authentication/auth/RegisterPage.vue"),
    },
    {
      name: "ConfirmEmail",
      path: "activate",
      component: () => import("@/views/authentication/auth/ConfirmEmailPage.vue"),
      props: (route: RouteLocationNormalized) => ({query: route.query.token}),
    },
    {
      name: "Error 404",
      path: "pages/error",
      component: () => import("@/views/pages/maintenance/error/Error404Page.vue"),
    },
  ],
};

export default AuthRoutes;
