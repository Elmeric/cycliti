import qs from "qs";
import http from "@/services/api";
import type { ApiResponse } from "@/services/types";
import type { UserOut, Token } from "@/models/User";

// export interface AuthError extends Error {
//   name: "AuthError";
// }

// function AuthError(msg: string): AuthError {
//   const error = new Error(msg) as AuthError;
//   error.name = "AuthError";
//   return error;
// }

// export function isAuthError(error: any): error is AuthError {
//   return error.name === "AuthError";
// }

async function authenticate(user: UserOut) {
  const data = qs.stringify(user);
  return await http.post<Token>("/login/access-token", data, {
    headers: { "Content-Encoding": "application/x-www-form-urlencoded" },
  });
}

export default {
  authenticate,
};
