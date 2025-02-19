'use client';

import { useUser } from '@auth0/nextjs-auth0/client';
import { useEffect, useState } from 'react';
import { Box, Container, Typography, Button, Paper, CircularProgress } from '@mui/material';
import { AuthService } from '@/FITB_api/service/auth';
import { UserResponse } from '@/FITB_api/responses/auth';

export default function AuthTestPage() {
  const { user, error: auth0Error, isLoading } = useUser();
  const [backendUser, setBackendUser] = useState<UserResponse | null>(null);
  const [backendError, setBackendError] = useState<string | null>(null);
  const [isVerifying, setIsVerifying] = useState(false);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [tokenError, setTokenError] = useState<string | null>(null);

  useEffect(() => {
    const verifyWithBackend = async () => {
      if (user?.sub) {
        setIsVerifying(true);
        setBackendError(null);
        setTokenError(null);
        try {
          // Get access token
          const tokenResponse = await fetch('/api/auth/token');
          if (!tokenResponse.ok) {
            throw new Error('Failed to get access token');
          }
          const { accessToken: token } = await tokenResponse.json();
          setAccessToken(token);
          
          // Verify with backend
          const userData = await AuthService.getCurrentUser(token);
          setBackendUser(userData);
        } catch (error) {
          if (error instanceof Error) {
            if (error.message.includes('access token')) {
              setTokenError(error.message);
            } else {
              setBackendError(error.message);
            }
          } else {
            setBackendError('Failed to verify with backend');
          }
          setBackendUser(null);
        } finally {
          setIsVerifying(false);
        }
      } else {
        setBackendUser(null);
        setAccessToken(null);
        setTokenError(null);
      }
    };

    verifyWithBackend();
  }, [user]);

  if (isLoading) {
    return (
      <Container>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="md">
      <Box py={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          Auth Test Page
        </Typography>

        {/* Auth0 Status */}
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Auth0 Status
          </Typography>
          {auth0Error ? (
            <Typography color="error">Auth0 Error: {auth0Error.message}</Typography>
          ) : user ? (
            <>
              <Typography>✅ Authenticated with Auth0</Typography>
              <Box component="pre" sx={{ mt: 2, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
                {JSON.stringify(user, null, 2)}
              </Box>
            </>
          ) : (
            <Typography>❌ Not authenticated with Auth0</Typography>
          )}
          <Box mt={2}>
            <Button
              variant="contained"
              color="primary"
              href={user ? '/api/auth/logout' : '/api/auth/login'}
            >
              {user ? 'Logout' : 'Login'}
            </Button>
          </Box>
        </Paper>

        {/* Access Token Status */}
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Access Token
          </Typography>
          {tokenError ? (
            <Typography color="error">Token Error: {tokenError}</Typography>
          ) : accessToken ? (
            <>
              <Typography>✅ Access Token Retrieved</Typography>
              <Box component="pre" sx={{ mt: 2, p: 2, bgcolor: 'grey.100', borderRadius: 1, wordWrap: 'break-word' }}>
                {accessToken}
              </Box>
            </>
          ) : user ? (
            <Typography>❌ No access token available</Typography>
          ) : (
            <Typography>Please login first</Typography>
          )}
        </Paper>

        {/* Backend Status */}
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Backend Status
          </Typography>
          {isVerifying ? (
            <Box display="flex" alignItems="center" gap={2}>
              <CircularProgress size={20} />
              <Typography>Verifying with backend...</Typography>
            </Box>
          ) : backendError ? (
            <Typography color="error">Backend Error: {backendError}</Typography>
          ) : backendUser ? (
            <>
              <Typography>✅ Verified with backend</Typography>
              <Box component="pre" sx={{ mt: 2, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
                {JSON.stringify(backendUser, null, 2)}
              </Box>
            </>
          ) : user ? (
            <Typography>❌ Not verified with backend</Typography>
          ) : (
            <Typography>Please login first</Typography>
          )}
        </Paper>
      </Box>
    </Container>
  );
} 