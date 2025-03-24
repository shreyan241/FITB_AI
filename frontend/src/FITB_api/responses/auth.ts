export interface UserResponse {
  id: number;
  email: string;
  first_name?: string;
  last_name?: string;
  is_verified: boolean;
  auth0_id: string;
}