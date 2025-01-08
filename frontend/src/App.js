import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';
import { motion } from 'framer-motion';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import BarChartIcon from '@mui/icons-material/BarChart';
import AutoGraphIcon from '@mui/icons-material/AutoGraph';
import PsychologyIcon from '@mui/icons-material/Psychology';
import BiotechIcon from '@mui/icons-material/Biotech';
import { CircularProgress } from '@mui/material';
import Chart from 'chart.js/auto';

function App() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const preventionChartRef = useRef(null);
  const predictionChartRef = useRef(null);

  useEffect(() => {
    if (results) {
      // Create Prevention Chart
      if (preventionChartRef.current) {
        const ctx = preventionChartRef.current.getContext('2d');
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: results.prevention_data.map(d => d.prevention_method),
            datasets: [{
              label: 'Correlation avec les cas confirmés',
              data: results.prevention_data.map(d => d.correlation),
              backgroundColor: 'rgba(54, 162, 235, 0.6)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      }

      // Create Prediction Chart
      if (predictionChartRef.current) {
        const ctx = predictionChartRef.current.getContext('2d');
        new Chart(ctx, {
          type: 'scatter',
          data: {
            datasets: [{
              label: 'Prédictions vs Réalité',
              data: results.prediction_data.actual.map((actual, i) => ({
                x: actual,
                y: results.prediction_data.predicted[i]
              })),
              backgroundColor: 'rgba(255, 99, 132, 0.6)'
            }]
          },
          options: {
            responsive: true,
            scales: {
              x: {
                title: {
                  display: true,
                  text: 'Valeurs Réelles'
                }
              },
              y: {
                title: {
                  display: true,
                  text: 'Valeurs Prédites'
                }
              }
            }
          }
        });
      }
    }
  }, [results]);

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
      const API_URL = process.env.NODE_ENV === 'production' 
        ? 'https://your-vercel-backend-url.vercel.app/api/analyze'
        : 'http://localhost:8000/api/analyze';
        
      const response = await axios.post(API_URL, formData, {
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
                  <div className="processing-animation">
                    <div className="processing-circle"></div>
                    <div className="processing-inner"></div>
                  </div>
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
          <div className="results-container">
            <div className="metrics-container">
              <div className="metric">
                <h4>Score R²</h4>
                <p>{results.prediction_data.metrics.r2.toFixed(3)}</p>
              </div>
              <div className="metric">
                <h4>RMSE</h4>
                <p>{results.prediction_data.metrics.rmse.toFixed(3)}</p>
              </div>
            </div>

            <div className="visualizations">
              <motion.div 
                className="viz-card"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
              >
                <h3 className="viz-title">Corrélation des Méthodes de Prévention</h3>
                <canvas ref={preventionChartRef} className="viz-canvas" />
              </motion.div>

              <motion.div 
                className="viz-card"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 }}
              >
                <h3 className="viz-title">Précision des Prédictions</h3>
                <canvas ref={predictionChartRef} className="viz-canvas" />
              </motion.div>
            </div>
          </div>
        )}
      </motion.div>
    </div>
  );
}

export default App;
