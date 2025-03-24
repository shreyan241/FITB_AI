'use client';

import { Box, Button } from '@mui/material';
import HeroSection from '@/components/landing/HeroSection';
import Link from 'next/link';

export default function Home() {
  return (
    <Box
      component="main"
      sx={{
        minHeight: '100vh',
        background: 'transparent',
      }}
    >
      <Box sx={{ position: 'fixed', top: 80, right: 20, zIndex: 1000 }}>
        <Button 
          variant="contained" 
          color="primary"
          onClick={() => {
            window.location.href = "/api/auth/login";
          }}
        >
          Login
        </Button>
      </Box>
      <HeroSection />
    </Box>
  );
}
