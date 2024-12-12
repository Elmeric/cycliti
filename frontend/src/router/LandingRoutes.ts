const LandingRoutes = {
  path: "/",
  meta: {
    requireAuth: false,
  },
  component: () => import("@/layouts/landing/LandingLayout.vue"),
  children: [
    {
      name: "Landing",
      path: "",
      component: () => import("@/views/LandingPage.vue"),
    },
  ],
};

export default LandingRoutes;
