import { AxiosError, isAxiosError } from "axios";

import authController from "./authentication";
import usersController from "./users";
import { getErrorMessage, reportError } from "@/utils/log_utils";

import type { ApiResponse } from "./types";

function handleError(error: AxiosError<any, any> | unknown): ApiResponse<null> {
  const result: ApiResponse<null> = {
    success: false,
    content: null,
    status: 500,
    message: "",
  };
  if (isAxiosError(error) && error.response) {
    // Request made but the server responded with an error
    reportError({ message: getErrorMessage(error) });
    result.status = error.response.status;
    result.message = error.response.data.detail;
  } else {
    reportError({ message: getErrorMessage(error) });
    result.message = "An error occur, please retry.";
  }
  return result;
}

export const API = {
  handleError,
  auth: authController,
  users: usersController,
};
