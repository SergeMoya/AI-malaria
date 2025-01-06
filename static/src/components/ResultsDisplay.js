import React from 'react';
import { Card, Grid, Typography, Box } from '@mui/material';
import { motion } from 'framer-motion';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import BarChartIcon from '@mui/icons-material/BarChart';

const MetricCard = ({ title, value, icon }) => (
  <motion.div
    initial={{ scale: 0.95, opacity: 0 }}
    animate={{ scale: 1, opacity: 1 }}
    transition={{ duration: 0.3 }}
  >
    <Card
      sx={{
        p: 3,
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: '0 12px 40px 0 rgba(31, 38, 135, 0.2)',
        },
      }}
    >
      <Box
        sx={{
          width: 60,
          height: 60,
          borderRadius: '50%',
          backgroundColor: 'primary.light',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          mb: 2,
        }}
      >
        {icon}
      </Box>
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      <Typography variant="h4" color="primary.main">
        {value.toFixed(3)}
      </Typography>
    </Card>
  </motion.div>
);

const ResultsDisplay = ({ metrics }) => {
  return (
    <motion.div
      initial={{ y: 20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5, delay: 0.4 }}
    >
      <Card sx={{ p: 4 }}>
        <Typography variant="h5" gutterBottom sx={{ mb: 4 }}>
          Résultats de l'Analyse
        </Typography>

        <Grid container spacing={4}>
          <Grid item xs={12} md={6}>
            <MetricCard
              title="Score R²"
              value={metrics.r2}
              icon={<TrendingUpIcon sx={{ color: 'white', fontSize: 30 }} />}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <MetricCard
              title="RMSE"
              value={metrics.rmse}
              icon={<BarChartIcon sx={{ color: 'white', fontSize: 30 }} />}
            />
          </Grid>
        </Grid>
      </Card>
    </motion.div>
  );
};

export default ResultsDisplay;
