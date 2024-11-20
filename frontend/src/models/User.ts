export interface UserOut {
  username: string;
  password: string;
}

interface UserBase {
  email: string;
  username: string;
  is_active: boolean;
  is_superuser: boolean;
}

export interface UserCreate extends UserBase {
  password: string;
}

export interface UserUpdate {
  email?: string;
  username?: string;
  password?: string;
  name?: string;
  city?: string;
  birthdate?: string;
  gender?: number;
  photo_path?: string;
  preferred_language?: string;
  access_type?: number;
}

export interface UserIn extends UserBase {
  id: number;
  // email: string;
  // username: string;
  // is_active: boolean;
  // is_superuser: boolean;
  name: string;
  city: string;
  birthdate: string;
  gender: number;
  photo_path: string;
  preferred_language: string;
  access_type: number;
}

export interface Token {
  access_token: string;
  token_type: string;
}
