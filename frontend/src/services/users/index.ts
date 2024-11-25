import http from "@/services/api";
import type { Msg, UserCreate, UserIn } from "@/models/User";
import { useAuthStore } from "@/stores";

async function getCurrentUser() {
  return await http.post<UserIn>("/login/test-token", null, { headers: authHeader() });
}

async function createUser(user: UserCreate) {
  return await http.post<Msg>("/users", user);
}

async function resendEmail(email: string) {
  return await http.post<Msg>("/users/resend-activation-email", email);
}

async function activate(email: string, token: string) {
  return await http.post<Msg>("/users/activate-account", {
    email: email,
    nonce: token,
  });
}

// function authHeader(url: string): Record<string, string> {
function authHeader(): Record<string, string> {
  // return auth header with jwt if user is logged in and request is to the api url
  const authStore = useAuthStore();
  const isLoggedIn = authStore.isAuthenticated;
  // const isApiUrl = url.startsWith(import.meta.env.VITE_API_BASE_URL);
  if (isLoggedIn) {
    // if (isLoggedIn && isApiUrl) {
    return { Authorization: `Bearer ${authStore.token?.access_token}` };
  } else {
    return {};
  }
}

export default {
  getCurrentUser,
  createUser,
  resendEmail,
  activate,
};
