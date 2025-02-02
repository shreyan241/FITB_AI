'use client';

import { Box, Container } from '@mui/material';
import HeroSection from '@/components/landing/HeroSection';
import FeatureGrid from '@/components/landing/FeatureGrid';
import HowItWorks from '@/components/landing/HowItWorks';
import CTASection from '@/components/landing/CTASection';

export default function Home() {
  return (
    <Box
      component="main"
      sx={{
        minHeight: '100vh',
        background: 'transparent',
      }}
    >
      <HeroSection />
      <FeatureGrid />
      <HowItWorks />
      <CTASection />
    </Box>
  );
}
