'use client';

import { Box, Container } from '@mui/material';
import HeroSection from '@/components/landing/HeroSection';
import FeatureGrid from '@/components/landing/FeatureGrid';
import HowItWorks from '@/components/landing/HowItWorks';
import CTASection from '@/components/landing/CTASection';
import ProfileClient from './profile-client';
export default function Home() {
  return (
    <Box
      component="main"
      sx={{
        minHeight: '100vh',
        background: 'transparent',
      }}
    >
      <a href="/api/auth/login">Login</a>
      <a href="/api/auth/logout">Logout</a>
      <ProfileClient />
      <HeroSection />
      <FeatureGrid />
      <HowItWorks />
      <CTASection />
    </Box>
  );
}
