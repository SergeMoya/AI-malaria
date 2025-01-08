import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import { motion } from 'framer-motion';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import BarChartIcon from '@mui/icons-material/BarChart';
import AutoGraphIcon from '@mui/icons-material/AutoGraph';
import PsychologyIcon from '@mui/icons-material/Psychology';
import BiotechIcon from '@mui/icons-material/Biotech';
import { CircularProgress } from '@mui/material';

// API configuration
const API_URL = process.env.REACT_APP_API_URL || 'https://ai-malaria-backend.onrender.com/api';
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
  };

  const handleSubmit = async () => {
    if (!file) {
      setError('Veuillez sélectionner un fichier');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    setLoading(true);
    setError(null);

    try {
      // First check if the API is healthy
      const healthCheck = await axios.get(`${API_URL}/healthcheck`, { timeout: 5000 });
      if (healthCheck.data.status !== 'healthy') {
        throw new Error('Le service est temporairement indisponible');
      }

      // Proceed with file upload
      const response = await axios.post(`${API_URL}/analyze`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: API_TIMEOUT
      });

      if (response.data.success) {
        setResults({
          heatmap: response.data.heatmap,
          prediction_plot: response.data.prediction_plot
        });
      } else {
        throw new Error(response.data.error || 'Erreur lors de l\'analyse');
      }
    } catch (err) {
      console.error('Analysis error:', err);
      setError(
        err.response?.data?.error || 
        err.message || 
        'Erreur lors de l\'analyse. Veuillez réessayer.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="neural-bg"></div>
      
      <motion.div
        className="content-wrapper"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <header className="App-header">
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            Analyse du Paludisme en Afrique
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="subtitle"
          >
            Analyse prédictive et visualisation des données sur le paludisme
          </motion.p>
        </header>

        <main>
          <section className="upload-section">
            <div
              className={`drop-zone ${dragActive ? 'active' : ''}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <CloudUploadIcon className="upload-icon" />
              <input
                type="file"
                onChange={handleFileChange}
                accept=".csv"
                className="file-input"
              />
              <p className="upload-text">
                {file ? file.name : "Glissez-déposez votre fichier CSV ou cliquez pour sélectionner"}
              </p>
              {error && <p className="error-message">{error}</p>}
              <button
                onClick={handleSubmit}
                className="analyze-button"
                disabled={!file || loading}
              >
                {loading ? (
                  <CircularProgress size={24} color="inherit" />
                ) : (
                  "Analyser les Données"
                )}
              </button>
            </div>
          </section>

          {results && (
            <motion.section
              className="results-section"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <div className="visualization-grid">
                <motion.div
                  className="visualization-card"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.2 }}
                >
                  <h3 className="viz-title">Carte de Chaleur de la Prévention</h3>
                  {results.heatmap && (
                    <motion.img 
                      src={results.heatmap} 
                      alt="Heatmap" 
                      className="viz-image"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.3 }}
                    />
                  )}
                </motion.div>

                <motion.div
                  className="visualization-card"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.4 }}
                >
                  <h3 className="viz-title">Graphique de Précision des Prédictions</h3>
                  {results.prediction_plot && (
                    <motion.img 
                      src={results.prediction_plot} 
                      alt="Prediction Plot" 
                      className="viz-image"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.5 }}
                    />
                  )}
                </motion.div>
              </div>
            </motion.section>
          )}
        </main>
      </motion.div>
    </div>
  );
}

export default App;
