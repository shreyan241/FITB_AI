'use client';

import React from 'react';
import {
  Toolbar,
  Typography,
  Box,
  useTheme,
} from '@mui/material';
import Link from 'next/link';
import Image from 'next/image';
import ScrollAppBar from './ScrollAppBar';
import ThemeToggle from './ThemeToggle';
import { useTheme as useAppTheme } from '@/providers/theme';

const LandingNavbar = () => {
  const theme = useTheme();
  const { toggleTheme } = useAppTheme();

  return (
    <ScrollAppBar>
      <Toolbar>
        {/* Logo and Text Container */}
        <Box 
          sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: 1,
            flexGrow: 1 // This makes the logo container take up available space
          }}
        >
          <Image
            src="/icon48.png"
            alt="Fries in the Bag AI Logo"
            width={32}
            height={32}
            style={{ 
              objectFit: 'contain',
              marginRight: '8px',
            }}
          />
          <Typography 
            variant="h6" 
            component="div" 
            sx={{ 
              fontWeight: 600,
              color: 'inherit',
            }}
          >
            <Link href="/" passHref style={{ textDecoration: 'none', color: 'inherit' }}>
              FITB AI
            </Link>
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <ThemeToggle toggleTheme={toggleTheme} />
        </Box>
      </Toolbar>
    </ScrollAppBar>
  );
};

export default LandingNavbar; 