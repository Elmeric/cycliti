import http from "@/services/api";
import { useAuthStore } from "@/stores";

import type { Msg, UserCreate, UserIn } from "@/models/User";
import type { ApiResponse } from "../types";

function linkStrava(state: string) {
  const stravaClientId = `${import.meta.env.VITE_STRAVA_CLIENT_ID}`;
  let redirectUri = `${import.meta.env.VITE_BACKEND_PROTOCOL}://${import.meta.env.VITE_BACKEND_HOST}`;
  redirectUri = encodeURIComponent(redirectUri);
  const scope = 'read,read_all,profile:read_all,activity:read,activity:read_all';

  const stravaAuthUrl = `http://www.strava.com/oauth/authorize?client_id=${stravaClientId}&response_type=code&redirect_uri=${redirectUri}/strava/link&approval_prompt=force&scope=${scope}&state=${state}`;

  // Redirect to the Strava authorization URL
  window.location.href = stravaAuthUrl;
}

export default {
  linkStrava,
};
