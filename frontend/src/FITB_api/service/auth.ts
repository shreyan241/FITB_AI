import { Auth0TokenRequest } from '../requests/auth';
import { UserResponse } from '../responses/auth';
import { useUser } from '@auth0/nextjs-auth0/client';

const API_BASE_URL = process.env.NEXT_PUBLIC_FITB_URL;

export class AuthService {
  /**
   * Verifies an Auth0 token with our backend and returns user data
   * @param token The Auth0 access token
   * @returns User data from our backend
   */
  static async verifyAuth0Token(token: string): Promise<UserResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/v1/auth/auth0/verify`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ token } as Auth0TokenRequest),
      });

      if (!response.ok) {
        throw new Error(`Auth verification failed: ${response.statusText}`);
      }

      return await response.json() as UserResponse;
    } catch (error) {
      console.error('Error verifying Auth0 token:', error);
      throw error;
    }
  }

  /**
   * Helper method to get the current user's data using their Auth0 token
   * Note: This method should be used within a component that has access to the Auth0 context
   * @returns User data from our backend
   */
  static async getCurrentUser(accessToken: string): Promise<UserResponse> {
    try {
      if (!accessToken) {
        throw new Error('No access token available');
      }
      return await this.verifyAuth0Token(accessToken);
    } catch (error) {
      console.error('Error getting current user:', error);
      throw error;
    }
  }
} 