import { isAxiosError } from "axios";
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
    ): Promise<ApiResponse<null>> {
      const result: ApiResponse<null> = { success: false, content: null };
      try {
        const resp = await API.auth.authenticate({ username, password });
        this.setToken(resp.data, keepMe);
        result.success = true;
      } catch (error) {
        if (isAxiosError(error)) {
          if (error.response) {
            // Request made but the server responded with an error
            console.log(error.response.status, error.response.data);
            result.status = error.response.status;
            result.message = error.response.data.detail;
          } else if (error.request) {
            // Request made but no response is received from the server.
            console.log(error.request);
            result.message = "No response from server. Try later.";
          } else {
            // Error occured while setting up the request
            console.log("Error", error.message);
            result.status = 500;
          }
        } else {
          result.status = 500;
        }
      } finally {
        return result;
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
