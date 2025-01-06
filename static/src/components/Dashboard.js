import React, { useState } from 'react';
import { Box, Container, Grid, Typography, Paper } from '@mui/material';
import { motion } from 'framer-motion';
import DataUpload from './DataUpload';
import VisualizationPanel from './VisualizationPanel';
import ResultsDisplay from './ResultsDisplay';

const Dashboard = () => {
  const [analysisResults, setAnalysisResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalysisComplete = (results) => {
    setAnalysisResults(results);
    setLoading(false);
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <Typography variant="h3" component="h1" gutterBottom sx={{ mb: 4, color: 'primary.main' }}>
          Analyse du Paludisme
        </Typography>

        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <DataUpload onAnalysisComplete={handleAnalysisComplete} setLoading={setLoading} />
          </Grid>
          
          {analysisResults && (
            <>
              <Grid item xs={12} md={8}>
                <VisualizationPanel visualizations={analysisResults.visualizations} />
              </Grid>
              <Grid item xs={12}>
                <ResultsDisplay metrics={analysisResults.metrics} />
              </Grid>
            </>
          )}
        </Grid>
      </motion.div>
    </Container>
  );
};

export default Dashboard;
