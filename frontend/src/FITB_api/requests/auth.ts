export interface Auth0TokenRequest {
  token: string;
}

export interface UserRegistrationRequest {
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
} 