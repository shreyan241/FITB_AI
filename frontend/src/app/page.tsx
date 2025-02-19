'use client';

import { Box, Button } from '@mui/material';
import HeroSection from '@/components/landing/HeroSection';
import FeatureGrid from '@/components/landing/FeatureGrid';
import HowItWorks from '@/components/landing/HowItWorks';
import CTASection from '@/components/landing/CTASection';
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
        <Link href="/auth-test" passHref>
          <Button variant="contained" color="primary">
            Test Auth
          </Button>
        </Link>
      </Box>
      <HeroSection />
      <FeatureGrid />
      <HowItWorks />
      <CTASection />
    </Box>
  );
}
