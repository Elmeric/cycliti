const HomeRoutes = {
  path: "/home",
  meta: {
    requireAuth: false,
  },
  component: () => import("@/layouts/home/HomeLayout.vue"),
  children: [
    {
      name: "Home",
      path: "",
      component: () => import("@/views/home/HomePage.vue"),
    },
  ],
};

export default HomeRoutes;
