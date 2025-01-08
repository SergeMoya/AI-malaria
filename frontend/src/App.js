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
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
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
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
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
      const response = await axios.post('http://localhost:5000/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: API_TIMEOUT
      });

      if (response.data.success) {
        setResults({
          heatmap: `${API_URL}/image/${response.data.heatmap}`,
          prediction_plot: `${API_URL}/image/${response.data.prediction_plot}`
        });
      } else {
        throw new Error(response.data.error || 'Erreur lors de l\'analyse');
      }
    } catch (err) {
      setError('Erreur lors de l\'analyse: ' + err.message);
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
        transition={{ duration: 0.8 }}
      >
        <header className="header-container">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <PsychologyIcon className="header-icon" />
          </motion.div>
          
          <h1>Analyse IA du Paludisme</h1>
          <p className="subtitle">Analyse avancée des données sur le paludisme en Afrique utilisant l'Intelligence Artificielle</p>
          
          <div className="model-info">
            <motion.div
              className="ai-badge"
              whileHover={{ scale: 1.05 }}
            >
              <AutoGraphIcon sx={{ fontSize: 16, marginRight: 1 }} />
              Régression Avancée
            </motion.div>
            <motion.div
              className="ai-badge"
              whileHover={{ scale: 1.05 }}
            >
              <BiotechIcon sx={{ fontSize: 16, marginRight: 1 }} />
              Analyse Prédictive
            </motion.div>
          </div>
        </header>

        <motion.div 
          className="upload-section"
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          whileHover={{ scale: 1.02 }}
        >
          <CloudUploadIcon className="upload-icon" />
          <h3 className="upload-text">Déposez votre fichier CSV ici</h3>
          <p className="or-text">ou</p>
          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            className="file-input"
            id="file-input"
          />
          <label htmlFor="file-input" className="file-button">
            Sélectionner un fichier
          </label>
          
          {file && (
            <motion.div 
              className="selected-file"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <p>Fichier sélectionné: {file.name}</p>
              <button 
                onClick={handleSubmit}
                className="analyze-button"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <div className="processing-animation">
                      <div className="processing-circle"></div>
                      <div className="processing-inner"></div>
                    </div>
                    Analyse IA en cours...
                  </>
                ) : (
                  'Lancer l\'analyse IA'
                )}
              </button>
            </motion.div>
          )}
        </motion.div>

        {error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="error-message"
          >
            {error}
          </motion.div>
        )}

        {results && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="results-section"
          >
            <h2 className="results-title">Résultats de l'Analyse IA</h2>
            
            <div className="metrics">
              <motion.div
                whileHover={{ scale: 1.05 }}
                className="metric-card"
              >
                <div className="model-accuracy">Précision du Modèle</div>
                <h3 className="metric-title">Score R²</h3>
                <p className="metric-value">{results.metrics.r2.toFixed(3)}</p>
                <span className="metric-description">Coefficient de détermination du modèle IA</span>
              </motion.div>
              
              <motion.div
                whileHover={{ scale: 1.05 }}
                className="metric-card"
              >
                <div className="model-accuracy">Erreur de Prédiction</div>
                <h3 className="metric-title">RMSE</h3>
                <p className="metric-value">{results.metrics.rmse.toFixed(3)}</p>
                <span className="metric-description">Erreur quadratique moyenne des prédictions</span>
              </motion.div>
            </div>

            <div className="visualizations">
              <motion.div
                whileHover={{ scale: 1.02 }}
                className="viz-card"
              >
                <h3 className="viz-title">Carte de Chaleur de la Prévention</h3>
                <motion.img 
                  src={`http://localhost:5000${results.visualizations.heatmap}`} 
                  alt="Heatmap" 
                  className="viz-image"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.5 }}
                />
              </motion.div>
              
              <motion.div
                whileHover={{ scale: 1.02 }}
                className="viz-card"
              >
                <h3 className="viz-title">Graphique de Précision des Prédictions</h3>
                <motion.img 
                  src={`http://localhost:5000${results.visualizations.prediction}`} 
                  alt="Prediction Plot" 
                  className="viz-image"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.5 }}
                />
              </motion.div>
            </div>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
}

export default App;
