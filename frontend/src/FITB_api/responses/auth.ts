export interface UserResponse {
  id: number;
  email: string;
  first_name?: string;
  last_name?: string;
  is_verified: boolean;
  auth0_id: string;
}

export interface TokenResponse {
  token: string;
}

export interface MessageResponse {
  message: string;
}

export interface TokenMessageResponse extends MessageResponse {
  token: string;
} 