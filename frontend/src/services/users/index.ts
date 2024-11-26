import http from "@/services/api";
import { useAuthStore } from "@/stores";

import type { Msg, UserCreate, UserIn } from "@/models/User";
import type { ApiResponse } from "../types";

async function getCurrentUser(): Promise<ApiResponse<UserIn>> {
  const resp = await http.post<UserIn>("/login/test-token", null, {
    headers: useAuthStore().authHeader,
  });
  return {
    success: true,
    content: resp.data,
    status: resp.status,
    message: "",
  };
}

async function createUser(user: UserCreate): Promise<ApiResponse<Msg>> {
  const resp = await http.post<Msg>("/users", user);
  return {
    success: true,
    content: resp.data,
    status: resp.status,
    message: "",
  };
}

async function resendEmail(email: string): Promise<ApiResponse<Msg>> {
  const resp = await http.post<Msg>("/users/resend-activation-email", email);
  return {
    success: true,
    content: resp.data,
    status: resp.status,
    message: "",
  };
}

async function activate(email: string, token: string): Promise<ApiResponse<Msg>> {
  console.log(email, token);
  const resp = await http.post<Msg>("/users/activate-account", {
    email: email,
    nonce: token,
  });
  return {
    success: true,
    content: resp.data,
    status: resp.status,
    message: resp.data.msg,
  };
}

export default {
  getCurrentUser,
  createUser,
  resendEmail,
  activate,
};
