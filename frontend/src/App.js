import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import { motion } from 'framer-motion';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import BarChartIcon from '@mui/icons-material/BarChart';
import { CircularProgress } from '@mui/material';

function App() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);

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
      });
      setResults(response.data);
    } catch (err) {
      setError('Erreur lors de l\'analyse: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <header>
          <BarChartIcon className="header-icon" />
          <h1>Analyse du Paludisme</h1>
          <p className="subtitle">Analyse avancée des données sur le paludisme en Afrique</p>
        </header>

        <div 
          className="upload-section"
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
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
            <div className="selected-file">
              <p>Fichier sélectionné: {file.name}</p>
              <button 
                onClick={handleSubmit}
                className="analyze-button"
                disabled={loading}
              >
                {loading ? (
                  <><CircularProgress size={20} color="inherit" style={{ marginRight: '10px' }} /> Analyse en cours...</>
                ) : (
                  'Analyser les données'
                )}
              </button>
            </div>
          )}
        </div>

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
            <h2 className="results-title">Résultats de l'analyse</h2>
            
            <div className="metrics">
              <motion.div
                whileHover={{ scale: 1.05 }}
                className="metric-card"
              >
                <h3 className="metric-title">Score R²</h3>
                <p className="metric-value">{results.metrics.r2.toFixed(3)}</p>
                <span className="metric-description">Coefficient de détermination</span>
              </motion.div>
              
              <motion.div
                whileHover={{ scale: 1.05 }}
                className="metric-card"
              >
                <h3 className="metric-title">RMSE</h3>
                <p className="metric-value">{results.metrics.rmse.toFixed(3)}</p>
                <span className="metric-description">Erreur quadratique moyenne</span>
              </motion.div>
            </div>

            <div className="visualizations">
              <motion.div
                whileHover={{ scale: 1.02 }}
                className="viz-card"
              >
                <h3 className="viz-title">Carte de Chaleur de la Prévention</h3>
                <img 
                  src={`http://localhost:5000${results.visualizations.heatmap}`} 
                  alt="Heatmap" 
                  className="viz-image" 
                />
              </motion.div>
              
              <motion.div
                whileHover={{ scale: 1.02 }}
                className="viz-card"
              >
                <h3 className="viz-title">Graphique de Précision des Prédictions</h3>
                <img 
                  src={`http://localhost:5000${results.visualizations.prediction}`} 
                  alt="Prediction Plot" 
                  className="viz-image" 
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
