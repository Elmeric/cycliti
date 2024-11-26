export interface ApiResponse<T> {
  success: boolean;
  content: T;
  status: number;
  message: string;
}
