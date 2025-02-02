'use client';

import { Box, Container, Typography, useTheme, Stack } from '@mui/material';
import { motion } from 'framer-motion';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SearchIcon from '@mui/icons-material/Search';
import AutomodeIcon from '@mui/icons-material/Automode';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

const steps = [
  {
    icon: AccountCircleIcon,
    title: 'Create Your Profile',
    description: 'Sign up and create your professional profile with your resume and preferences.',
  },
  {
    icon: SearchIcon,
    title: 'Find Opportunities',
    description: 'Browse through AI-curated job listings that match your skills and experience.',
  },
  {
    icon: AutomodeIcon,
    title: 'Automated Applications',
    description: 'Let our AI assistant handle the application process while you focus on what matters.',
  },
  {
    icon: CheckCircleIcon,
    title: 'Track Progress',
    description: 'Monitor your applications and get notifications for updates and interviews.',
  },
];

const HowItWorks = () => {
  const theme = useTheme();

  return (
    <Box
      component="section"
      id="how-it-works"
      sx={{
        py: { xs: 8, sm: 12 },
        background: theme.palette.mode === 'dark'
          ? '#0a0a0a'
          : '#ffffff',
        transition: 'all 0.3s ease-in-out',
      }}
    >
      <Container maxWidth="lg">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          viewport={{ once: true }}
        >
          <Typography
            variant="h2"
            align="center"
            sx={{
              mb: 8,
              fontSize: { xs: '2rem', sm: '2.5rem', md: '3rem' },
              fontWeight: 700,
              color: theme.palette.text.primary,
            }}
          >
            How It Works
          </Typography>
        </motion.div>

        <Stack
          direction={{ xs: 'column', md: 'row' }}
          spacing={{ xs: 4, md: 2 }}
          alignItems="stretch"
        >
          {steps.map((step, index) => {
            const Icon = step.icon;
            return (
              <motion.div
                key={step.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                style={{ flex: 1 }}
              >
                <Box
                  sx={{
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    textAlign: 'center',
                    position: 'relative',
                    '&::after': {
                      content: '""',
                      position: 'absolute',
                      top: '40px',
                      right: { xs: '50%', md: '-10%' },
                      width: { xs: '2px', md: '20%' },
                      height: { xs: '40px', md: '2px' },
                      background: theme.palette.mode === 'dark'
                        ? 'rgba(255, 255, 255, 0.1)'
                        : 'rgba(0, 0, 0, 0.1)',
                      display: index === steps.length - 1 ? 'none' : 'block',
                      transition: 'background-color 0.3s ease-in-out',
                    },
                  }}
                >
                  <Box
                    sx={{
                      width: 80,
                      height: 80,
                      borderRadius: '50%',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      mb: 3,
                      background: theme.palette.mode === 'dark'
                        ? 'rgba(255, 255, 255, 0.05)'
                        : 'rgba(0, 0, 0, 0.02)',
                      border: '2px solid',
                      borderColor: theme.palette.primary.main,
                      transition: 'all 0.3s ease-in-out',
                    }}
                  >
                    <Icon
                      sx={{
                        fontSize: 40,
                        color: theme.palette.primary.main,
                        transition: 'color 0.3s ease-in-out',
                      }}
                    />
                  </Box>
                  <Typography
                    variant="h6"
                    sx={{
                      mb: 2,
                      fontWeight: 600,
                      color: theme.palette.text.primary,
                      transition: 'color 0.3s ease-in-out',
                    }}
                  >
                    {step.title}
                  </Typography>
                  <Typography
                    variant="body1"
                    sx={{
                      color: theme.palette.text.secondary,
                      lineHeight: 1.6,
                      transition: 'color 0.3s ease-in-out',
                    }}
                  >
                    {step.description}
                  </Typography>
                </Box>
              </motion.div>
            );
          })}
        </Stack>
      </Container>
    </Box>
  );
};

export default HowItWorks; 