import React, { useState } from 'react';
import { Card, Box, Tabs, Tab, Typography } from '@mui/material';
import { motion } from 'framer-motion';

const VisualizationPanel = ({ visualizations }) => {
  const [activeTab, setActiveTab] = useState(0);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  return (
    <motion.div
      initial={{ scale: 0.95, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.3, delay: 0.2 }}
    >
      <Card sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
          Visualisations
        </Typography>

        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
          <Tabs value={activeTab} onChange={handleTabChange}>
            <Tab label="Carte de Chaleur" />
            <Tab label="Précision des Prédictions" />
          </Tabs>
        </Box>

        <Box sx={{ mt: 2 }}>
          {activeTab === 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
            >
              <img 
                src={visualizations.heatmap} 
                alt="Carte de chaleur" 
                style={{ width: '100%', borderRadius: '8px' }}
              />
            </motion.div>
          )}
          {activeTab === 1 && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
            >
              <img 
                src={visualizations.prediction} 
                alt="Graphique de prédiction" 
                style={{ width: '100%', borderRadius: '8px' }}
              />
            </motion.div>
          )}
        </Box>
      </Card>
    </motion.div>
  );
};

export default VisualizationPanel;
