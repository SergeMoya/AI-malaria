import React, { useState, useRef } from 'react';
import { Box, Button, Card, Typography, CircularProgress } from '@mui/material';
import { motion } from 'framer-motion';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import axios from 'axios';

const DataUpload = ({ onAnalysisComplete, setLoading }) => {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState(null);
  const inputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file) => {
    setFile(file);
  };

  const handleSubmit = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      onAnalysisComplete(response.data);
    } catch (error) {
      console.error('Error during analysis:', error);
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ scale: 0.95, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <Card
        sx={{
          p: 4,
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          cursor: 'pointer',
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-4px)',
            boxShadow: '0 12px 40px 0 rgba(31, 38, 135, 0.2)',
          },
        }}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".csv"
          onChange={handleChange}
          style={{ display: 'none' }}
        />
        
        <CloudUploadIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
        <Typography variant="h6" gutterBottom>
          Déposez votre fichier CSV ici
        </Typography>
        <Typography variant="body2" color="text.secondary" align="center" sx={{ mb: 3 }}>
          ou cliquez pour sélectionner
        </Typography>
        
        <Button
          variant="contained"
          onClick={() => inputRef.current.click()}
          sx={{ mb: 2 }}
        >
          Sélectionner un fichier
        </Button>
        
        {file && (
          <Box sx={{ mt: 2, width: '100%' }}>
            <Typography variant="body2" sx={{ mb: 2 }}>
              Fichier sélectionné: {file.name}
            </Typography>
            <Button
              variant="contained"
              color="primary"
              fullWidth
              onClick={handleSubmit}
            >
              Lancer l'analyse
            </Button>
          </Box>
        )}
      </Card>
    </motion.div>
  );
};

export default DataUpload;
