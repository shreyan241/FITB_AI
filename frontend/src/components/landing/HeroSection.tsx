'use client';

import { Box, Container, Typography, Button, useTheme } from '@mui/material';
import { motion } from 'framer-motion';

const HeroSection = () => {
  const theme = useTheme();

  return (
    <Box
      sx={{
        width: '100%',
        background: theme.palette.mode === 'dark' ? '#0a0a0a' : '#ffffff',
        transition: 'background-color 0.3s ease-in-out',
      }}
    >
      <Container maxWidth="lg">
        <Box
          sx={{
            pt: { xs: 8, sm: 12, md: 16 },
            pb: { xs: 8, sm: 12 },
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            textAlign: 'center',
            gap: 4,
            color: theme.palette.text.primary,
          }}
        >
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Typography
              variant="h1"
              sx={{
                fontSize: { xs: '2.5rem', sm: '3.5rem', md: '4rem' },
                mb: 2,
                color: theme.palette.text.primary,
              }}
            >
              Fries in the Bag AI
            </Typography>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Typography
              variant="h2"
              sx={{
                fontSize: { xs: '1.25rem', sm: '1.5rem', md: '1.75rem' },
                maxWidth: '800px',
                mx: 'auto',
                lineHeight: 1.6,
                color: theme.palette.text.secondary,
              }}
            >
              Your AI-powered job application assistant. Let us help you land your dream job
              with automated application processes and intelligent resume optimization.
            </Typography>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}
          >
            <Button
              variant="contained"
              size="large"
              sx={{
                minWidth: { xs: '100%', sm: '200px' },
                bgcolor: theme.palette.primary.main,
                color: theme.palette.primary.contrastText,
                '&:hover': {
                  bgcolor: theme.palette.primary.dark,
                },
              }}
            >
              Start Applying
            </Button>
            <Button
              variant="outlined"
              size="large"
              component="a"
              href="#how-it-works"
              sx={{
                minWidth: { xs: '100%', sm: '200px' },
                borderColor: theme.palette.mode === 'dark' ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.2)',
                color: theme.palette.text.primary,
                '&:hover': {
                  borderColor: theme.palette.mode === 'dark' ? 'rgba(255, 255, 255, 0.3)' : 'rgba(0, 0, 0, 0.3)',
                  bgcolor: theme.palette.mode === 'dark' ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)',
                },
              }}
            >
              How It Works
            </Button>
          </motion.div>
        </Box>
      </Container>
    </Box>
  );
};

export default HeroSection; 