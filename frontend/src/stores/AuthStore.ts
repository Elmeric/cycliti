import { defineStore } from "pinia";
import { router } from "@/router";

import { API } from "@/services";

import type { Token } from "@/models/User";
import type { ApiResponse } from "@/services/types";

interface AuthState {
  // user: UserInStore | null;
  token: Token | null;
}

function getToken(): Token | null {
  const token = localStorage.getItem("token") ?? "null";
  try {
    return JSON.parse(token);
  } catch (error) {
    localStorage.removeItem("token");
    return null;
  }
}

const initialState: AuthState = {
  // user: getUser(),
  token: getToken(),
};

export default defineStore({
  id: "auth",
  // initialize state from local storage to enable user to stay logged in
  state: (): AuthState => {
    return initialState;
  },

  getters: {
    isAuthenticated: (state) => state.token !== null,

    authHeader(): Record<string, string> {
      // return auth header with jwt if user is logged in and request is to the api url
      const isLoggedIn = this.isAuthenticated;
      if (isLoggedIn) {
        return { Authorization: `Bearer ${this.token?.access_token}` };
      } else {
        return {};
      }
    },
  },

  actions: {
    setToken(token: Token, persist: boolean = false) {
      this.token = token;
      if (persist) {
        localStorage.setItem("token", JSON.stringify(token));
      } else {
        localStorage.removeItem("token");
      }
    },

    removeToken() {
      this.token = null;
      localStorage.removeItem("token");
    },

    async authenticate(
      username: string,
      password: string,
      keepMe: boolean = false
    ): Promise<ApiResponse<Token | null>> {
      try {
        const result = await API.auth.authenticate({ username, password });
        this.setToken(result.content, keepMe);
        return result;
      } catch (error) {
        return API.handleError(error);
      }
    },

    logout() {
      // this.user = null;
      // localStorage.removeItem("user");
      this.removeToken();
      router.push("/auth/login"); // To be moved in the calling Vue components
    },
  },
});
