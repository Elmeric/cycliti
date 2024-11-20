const HomeRoutes = {
  path: "/",
  meta: {
    requireAuth: false,
  },
  component: () => import("@/layouts/home/HomeLayout.vue"),
  children: [
    {
      name: "Home",
      path: "",
      component: () => import("@/views/HomePage.vue"),
    },
  ],
};

export default HomeRoutes;
