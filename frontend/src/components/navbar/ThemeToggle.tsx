'use client';

import { IconButton } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';

interface ThemeToggleProps {
  toggleTheme: () => void;
}

const ThemeToggle = ({ toggleTheme }: ThemeToggleProps) => {
  const theme = useTheme();

  return (
    <IconButton 
      onClick={toggleTheme} 
      sx={{ 
        color: theme.palette.mode === 'dark' ? '#ffd54f' : '#7c4dff',
        transition: 'transform 0.3s ease-in-out, background-color 0.3s ease-in-out',
        borderRadius: '12px',
        padding: '8px',
        '&:hover': {
          transform: 'rotate(90deg)',
          backgroundColor: theme.palette.mode === 'dark'
            ? 'rgba(255, 213, 79, 0.1)'
            : 'rgba(124, 77, 255, 0.1)',
        },
      }}
    >
      {theme.palette.mode === 'dark' ? (
        <Brightness7Icon sx={{ 
          transition: 'transform 0.3s ease-in-out',
          animation: 'fadeIn 0.3s ease-in-out',
          '@keyframes fadeIn': {
            '0%': {
              opacity: 0,
              transform: 'scale(0.8) rotate(-180deg)',
            },
            '100%': {
              opacity: 1,
              transform: 'scale(1) rotate(0)',
            },
          },
        }} />
      ) : (
        <Brightness4Icon sx={{ 
          transition: 'transform 0.3s ease-in-out',
          animation: 'fadeIn 0.3s ease-in-out',
          '@keyframes fadeIn': {
            '0%': {
              opacity: 0,
              transform: 'scale(0.8) rotate(180deg)',
            },
            '100%': {
              opacity: 1,
              transform: 'scale(1) rotate(0)',
            },
          },
        }} />
      )}
    </IconButton>
  );
};

export default ThemeToggle; 