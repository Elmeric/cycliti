import { defineStore } from "pinia";

import type { Msg, UserCreate, UserIn } from "@/models/User";
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
            result.message = "An error occur, please retry.";
          } else {
            // Error occured while setting up the request
            console.log("Error", error.message);
            result.status = 500;
            result.message = error.message;
          }
        } else {
          result.status = 500;
          result.message = "An error occur, please retry.";
        }
      } finally {
        return result;
      }
    },

    async createUser(
      email: string,
      username: string,
      password: string
    ): Promise<ApiResponse<Msg | null>> {
      const user: UserCreate = {
        email: email,
        username: username,
        password: password,
        is_active: false,
        is_superuser: false,
      }
      const result: ApiResponse<Msg | null> = { success: false, content: null };
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
            result.message = "An error occur, please retry.";
          } else {
            // Error occured while setting up the request
            console.log("Error", error.message);
            result.status = 500;
            result.message = error.message;
          }
        } else {
          result.status = 500;
          result.message = "An error occur, please retry.";
        }
      } finally {
        return result;
      }
    },

    async activate(
      email: string,
      token: string
    ): Promise<ApiResponse<Msg | null>> {
      const result: ApiResponse<Msg | null> = { success: false, content: null };
      try {
        const resp = await API.users.activate(email, token);
        console.log("Activate user: ", resp)
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
            result.message = "An error occur, please retry.";
          } else {
            // Error occured while setting up the request
            console.log("Error", error.message);
            result.status = 500;
            result.message = error.message;
          }
        } else {
          result.status = 500;
          result.message = "An error occur, please retry.";
        }
      } finally {
        return result;
      }
    },
  },
});
