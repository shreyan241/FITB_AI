'use client';

import { Box, Container, Typography, Button, useTheme } from '@mui/material';
import { motion } from 'framer-motion';
import RocketLaunchIcon from '@mui/icons-material/RocketLaunch';

const CTASection = () => {
  const theme = useTheme();

  return (
    <Box
      component="section"
      sx={{
        py: { xs: 8, sm: 12 },
        background: theme.palette.mode === 'dark'
          ? 'linear-gradient(45deg, #1a1a1a 0%, #0a0a0a 100%)'
          : 'linear-gradient(45deg, #f8fafc 0%, #ffffff 100%)',
        borderTop: '1px solid',
        borderColor: theme.palette.mode === 'dark'
          ? 'rgba(255, 255, 255, 0.1)'
          : 'rgba(0, 0, 0, 0.1)',
      }}
    >
      <Container maxWidth="md">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          viewport={{ once: true }}
        >
          <Box
            sx={{
              textAlign: 'center',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 4,
            }}
          >
            <RocketLaunchIcon
              sx={{
                fontSize: 56,
                color: theme.palette.primary.main,
                mb: 2,
              }}
            />
            <Typography
              variant="h2"
              sx={{
                fontSize: { xs: '2rem', sm: '2.5rem', md: '3rem' },
                mb: 2,
                color: theme.palette.text.primary,
              }}
            >
              Ready to Streamline Your Job Search?
            </Typography>
            <Typography
              variant="h3"
              sx={{
                fontSize: { xs: '1.25rem', sm: '1.5rem' },
                maxWidth: '600px',
                mb: 4,
                color: theme.palette.text.secondary,
              }}
            >
              Join thousands of job seekers who are landing their dream jobs faster with Fries in the Bag AI.
            </Typography>
            <Box
              sx={{
                display: 'flex',
                gap: 2,
                flexDirection: { xs: 'column', sm: 'row' },
                alignItems: 'center',
                justifyContent: 'center',
                width: '100%',
              }}
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
                Get Started Now
              </Button>
              <Button
                variant="outlined"
                size="large"
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
                Learn More
              </Button>
            </Box>
          </Box>
        </motion.div>
      </Container>
    </Box>
  );
};

export default CTASection; 