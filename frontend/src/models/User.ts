export interface UserOut {
  username: string;
  password: string;
}

interface UserBase {
  email: string;
  username: string;
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

export interface UserToken {
  user: UserIn;
  token: Token;
}

export interface Msg {
  msg: string;
}
