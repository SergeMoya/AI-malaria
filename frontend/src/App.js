import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import { motion } from 'framer-motion';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { CircularProgress } from '@mui/material';
import { endpoints } from './config';

// API configuration
const API_TIMEOUT = 30000; // 30 seconds

function App() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  // Neural network background animation
  useEffect(() => {
    const createNeuralBackground = () => {
      const bg = document.querySelector('.neural-bg');
      if (!bg) return;

      // Clear existing nodes
      bg.innerHTML = '';

      // Create nodes
      for (let i = 0; i < 50; i++) {
        const node = document.createElement('div');
        node.className = 'neural-node';
        node.style.left = `${Math.random() * 100}%`;
        node.style.top = `${Math.random() * 100}%`;
        node.style.animationDelay = `${Math.random() * 2}s`;
        bg.appendChild(node);
      }
    };

    createNeuralBackground();
    window.addEventListener('resize', createNeuralBackground);

    return () => {
      window.removeEventListener('resize', createNeuralBackground);
    };
  }, []);

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
      handleFileSelection(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (event) => {
    if (event.target.files && event.target.files[0]) {
      handleFileSelection(event.target.files[0]);
    }
  };

  const handleFileSelection = (selectedFile) => {
    if (!selectedFile.name.toLowerCase().endsWith('.csv')) {
      setError('Veuillez sélectionner un fichier CSV');
      return;
    }
    setFile(selectedFile);
    setError(null);
    // Automatically start analysis when file is selected
    handleSubmit(selectedFile);
  };

  const handleSubmit = async (selectedFile) => {
    const fileToAnalyze = selectedFile || file;
    if (!fileToAnalyze) {
      setError('Veuillez sélectionner un fichier');
      return;
    }

    const formData = new FormData();
    formData.append('file', fileToAnalyze);
    setLoading(true);
    setError(null);

    try {
      // First check if the API is healthy
      const healthCheck = await axios.get(endpoints.healthcheck, { timeout: 5000 });
      if (healthCheck.data.status !== 'healthy') {
        throw new Error('Le service est temporairement indisponible');
      }

      // Then send the file for analysis
      const response = await axios.post(endpoints.analyze, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: API_TIMEOUT,
      });

      if (response.data && !response.data.error) {
        setResults(response.data);
      } else {
        throw new Error(response.data.error || 'Erreur pendant l\'analyse');
      }
    } catch (err) {
      console.error('Analysis error:', err);
      setError(
        err.response?.data?.error || 
        err.message || 
        'Erreur pendant l\'analyse. Veuillez réessayer.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="neural-bg"></div>
      <div className="content">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          Analyse du Paludisme en Afrique
        </motion.h1>
        
        <motion.h2
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          Analyse prédictive et visualisation des données sur le paludisme
        </motion.h2>

        <motion.div
          className={`upload-container ${dragActive ? 'drag-active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <div className="upload-content">
            <CloudUploadIcon className="upload-icon" />
            <p>{file ? file.name : 'DatasetAfricaMalaria.csv'}</p>
            <input
              type="file"
              onChange={handleFileChange}
              accept=".csv"
              style={{ display: 'none' }}
              id="file-upload"
            />
            <label htmlFor="file-upload" className="upload-button">
              {file ? 'Changer de fichier' : 'Analyser les Données'}
            </label>
          </div>
        </motion.div>

        {error && (
          <motion.div 
            className="error-message"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            {error}
          </motion.div>
        )}
        
        {loading && (
          <motion.div 
            className="loading"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <CircularProgress />
            <p>Analyse en cours...</p>
          </motion.div>
        )}

        {results && !loading && (
          <motion.div 
            className="results"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <h3>Résultats de l'Analyse</h3>
            
            {results.heatmap && (
              <motion.div 
                className="visualization-card"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2 }}
              >
                <h4>Carte de Chaleur de la Prévention</h4>
                <img 
                  src={`data:image/png;base64,${results.heatmap}`} 
                  alt="Carte de chaleur de la prévention" 
                  className="visualization-image"
                />
              </motion.div>
            )}
            
            {results.prediction_accuracy && (
              <motion.div 
                className="visualization-card"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.4 }}
              >
                <h4>Graphique de Précision des Prédictions</h4>
                <img 
                  src={`data:image/png;base64,${results.prediction_accuracy}`} 
                  alt="Graphique de précision des prédictions" 
                  className="visualization-image"
                />
              </motion.div>
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
}

export default App;
