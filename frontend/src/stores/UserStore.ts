import { defineStore } from "pinia";

import { API } from "@/services";

import type { Msg, UserCreate, UserIn } from "@/models/User";
import type { ApiResponse } from "@/services/types";

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
      try {
        const result = await API.users.getCurrentUser();
        this.setCurrentUser(result.content);
        return result;
      } catch (error) {
        return API.handleError(error);
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
      };
      try {
        return await API.users.createUser(user);
      } catch (error) {
        return API.handleError(error);
      }
    },

    async resendEmail(email: string): Promise<ApiResponse<Msg | null>> {
      try {
        return await API.users.resendEmail(email);
      } catch (error) {
        return API.handleError(error);
      }
    },

    async activate(email: string, token: string): Promise<ApiResponse<Msg | null>> {
      try {
        return await API.users.activate(email, token);
      } catch (error) {
        return API.handleError(error);
      }
    },

    async forgotPassword(email: string): Promise<ApiResponse<Msg | null>> {
      try {
        return await API.users.forgotPassword(email);
      } catch (error) {
        return API.handleError(error);
      }
    },

    async resetPassword(
      email: string,
      password: string,
      nonce: string
    ): Promise<ApiResponse<Msg | null>> {
      try {
        return await API.users.resetPassword(email, password, nonce);
      } catch (error) {
        return API.handleError(error);
      }
    },

    linkToStrava(state: string) {
      API.strava.linkStrava(state);
    },
  },
});
