'use client';

import { useState, useEffect } from 'react';
import { AppBar, AppBarProps } from '@mui/material';
import { useTheme } from '@mui/material/styles';

interface ScrollAppBarProps extends AppBarProps {}

const ScrollAppBar = ({ children, ...props }: ScrollAppBarProps) => {
  const theme = useTheme();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      const isScrolled = window.scrollY > 20;
      setScrolled(isScrolled);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <AppBar
      position="fixed"
      elevation={0}
      className={scrolled ? 'scrolled' : ''}
      sx={{
        background: theme.palette.mode === 'dark'
          ? scrolled
            ? 'rgba(10, 10, 10, 0.8)'
            : 'rgba(10, 10, 10, 0.5)'
          : 'white',
        backdropFilter: 'blur(10px)',
        boxShadow: theme.palette.mode === 'dark'
          ? scrolled
            ? '0 4px 30px rgba(0, 0, 0, 0.5)'
            : 'none'
          : '0 1px 3px rgba(0, 0, 0, 0.05)',
        borderBottom: '1px solid',
        borderColor: theme.palette.mode === 'dark'
          ? 'rgba(255, 255, 255, 0.1)'
          : 'rgba(0, 0, 0, 0.1)',
        color: theme.palette.mode === 'dark'
          ? theme.palette.common.white
          : theme.palette.common.black,
        transition: 'all 0.3s ease-in-out',
      }}
      {...props}
    >
      {children}
    </AppBar>
  );
};

export default ScrollAppBar; 