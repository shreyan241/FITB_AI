'use client';

import { Box, Container, Grid, Typography, useTheme } from '@mui/material';
import { motion } from 'framer-motion';
import AutomationIcon from '@mui/icons-material/AutoFixHigh';
import OptimizationIcon from '@mui/icons-material/TrendingUp';
import TrackingIcon from '@mui/icons-material/QueryStats';
import AIIcon from '@mui/icons-material/Psychology';

const features = [
  {
    icon: AutomationIcon,
    title: 'Automated Applications',
    description: 'Save time with intelligent form filling and automated job application submissions across multiple platforms.',
  },
  {
    icon: OptimizationIcon,
    title: 'Resume Optimization',
    description: 'AI-powered resume enhancement to match job requirements and increase your chances of getting noticed.',
  },
  {
    icon: TrackingIcon,
    title: 'Application Tracking',
    description: 'Keep track of all your applications, deadlines, and follow-ups in one centralized dashboard.',
  },
  {
    icon: AIIcon,
    title: 'Smart Recommendations',
    description: 'Get personalized job recommendations based on your skills, experience, and preferences.',
  },
];

const FeatureGrid = () => {
  const theme = useTheme();

  return (
    <Box
      component="section"
      sx={{
        py: { xs: 8, sm: 12 },
        background: theme.palette.mode === 'dark'
          ? 'linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%)'
          : 'linear-gradient(180deg, #f8fafc 0%, #ffffff 100%)',
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
              color: theme.palette.text.primary,
            }}
          >
            Features that Make the Difference
          </Typography>
        </motion.div>

        <Grid container spacing={4}>
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <Grid item xs={12} sm={6} md={3} key={feature.title}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  viewport={{ once: true }}
                >
                  <Box
                    component={motion.div}
                    whileHover={{ y: -8 }}
                    sx={{
                      p: 4,
                      height: '100%',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      textAlign: 'center',
                      borderRadius: '16px',
                      background: theme.palette.mode === 'dark'
                        ? 'rgba(255, 255, 255, 0.05)'
                        : 'rgba(0, 0, 0, 0.02)',
                      boxShadow: theme.palette.mode === 'dark'
                        ? '0 4px 20px rgba(0, 0, 0, 0.2)'
                        : '0 4px 20px rgba(0, 0, 0, 0.05)',
                    }}
                  >
                    <Icon
                      sx={{
                        fontSize: 48,
                        mb: 2,
                        color: theme.palette.primary.main,
                      }}
                    />
                    <Typography
                      variant="h6"
                      sx={{
                        mb: 2,
                        color: theme.palette.text.primary,
                      }}
                    >
                      {feature.title}
                    </Typography>
                    <Typography
                      variant="body1"
                      sx={{
                        lineHeight: 1.6,
                        color: theme.palette.text.secondary,
                      }}
                    >
                      {feature.description}
                    </Typography>
                  </Box>
                </motion.div>
              </Grid>
            );
          })}
        </Grid>
      </Container>
    </Box>
  );
};

export default FeatureGrid; 