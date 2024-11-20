import { defineStore } from "pinia";

import type { UserCreate, UserIn } from "@/models/User";
import type { ApiResponse } from "@/services/types";
import { API } from "@/services";
import { isAxiosError } from "axios";

interface UsersState {
  users: UserIn[];
  currentUser: UserIn | null;
}

export default defineStore({
  id: "User",

  state: (): UsersState => {
    return {
      users: [],
      currentUser: null,
    };
  },

  actions: {
    setCurrentUser(user: UserIn) {
      this.currentUser = user;
    },

    async getCurrentUser(): Promise<ApiResponse<UserIn | null>> {
      const result: ApiResponse<UserIn | null> = { success: false, content: null };
      try {
        const resp = await API.users.getCurrentUser();
        this.setCurrentUser(resp.data);
        result.success = true;
        result.content = resp.data;
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
            result.message = "No response from server: retry later!";
          } else {
            // Error occured while setting up the request
            console.log("Error", error.message);
            result.status = 500;
            result.message = error.message;
          }
        } else {
          result.status = 500;
          result.message = "Internal error: retry later!";
        }
      } finally {
        return result;
      }
    },

    async createUser(
      email: string,
      password: string
    ): Promise<ApiResponse<UserIn | null>> {
      const user: UserCreate = {
        email: email,
        username: "username",
        password: password,
        is_active: false,
        is_superuser: false,
      }
      const result: ApiResponse<UserIn | null> = { success: false, content: null };
      try {
        const resp = await API.users.createUser(user);
        console.log("Create user: ", resp)
        result.success = true;
        result.content = resp.data;
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
            result.message = "No response from server: retry later!";
          } else {
            // Error occured while setting up the request
            console.log("Error", error.message);
            result.status = 500;
            result.message = error.message;
          }
        } else {
          result.status = 500;
          result.message = "Internal error: retry later!";
        }
      } finally {
        return result;
      }
    },
  },
});
