import { createRouter, createWebHistory } from "vue-router";
import HomeRoutes from "./HomeRoutes";
import MainRoutes from "./MainRoutes";
import AuthRoutes from "./AuthRoutes";
import { useAuthStore } from "@/stores";
import { useUIStore } from "@/stores";

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/:pathMatch(.*)*",
      component: () => import("@/views/pages/maintenance/error/Error404Page.vue"),
    },
    HomeRoutes,
    MainRoutes,
    AuthRoutes,
  ],
});

router.beforeEach(async (to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const auth = useAuthStore();

  console.log(to.path);

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (to.meta.requiresAuth && !auth.isAuthenticated) {
      console.log("Auth required");
      next({
        name: "Login",
        // save the location we were at to come back later
        query: { redirect: to.fullPath },
      });
    } else next();
  } else if (to.path === "/" && auth.isAuthenticated) {
    next({ name: "Dashboard" });
  } else next();
});

router.beforeEach(() => {
  const uiStore = useUIStore();
  uiStore.isLoading = true;
  console.log("is loading");
  setTimeout(() => (uiStore.isLoading = false), 1500);
});

// router.afterEach(() => {
//   const uiStore = useUIStore();
//   uiStore.isLoading = false;
//   console.log("Loaded");
// });
