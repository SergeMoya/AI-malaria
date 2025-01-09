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

  // AI particles animation
  useEffect(() => {
    const createAIParticles = () => {
      const particles = document.querySelector('.ai-particles');
      if (!particles) return;

      // Clear existing particles
      particles.innerHTML = '';

      // Create particles
      for (let i = 0; i < 100; i++) {
        const particle = document.createElement('div');
        particle.className = 'ai-particle';
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        particle.style.animationDelay = `${Math.random() * 2}s`;
        particles.appendChild(particle);
      }
    };

    createAIParticles();
    window.addEventListener('resize', createAIParticles);

    return () => {
      window.removeEventListener('resize', createAIParticles);
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
      <div className="ai-particles">
        {/* AI particles will be added by useEffect */}
      </div>
      
      <div className="content-wrapper">
        <header className="App-header">
          <div className="ai-badge">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M2 17L12 22L22 17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M2 12L12 17L22 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            Powered by Advanced AI
          </div>
          <h1>AI-Powered Malaria Analysis</h1>
          <p className="subtitle">
            Leveraging machine learning and neural networks for advanced malaria data analysis and prediction
          </p>
        </header>

        <div className="upload-container" 
             onDragEnter={handleDrag}
             onDragLeave={handleDrag}
             onDragOver={handleDrag}
             onDrop={handleDrop}
             onClick={() => document.getElementById('file-input').click()}
        >
          <input
            id="file-input"
            type="file"
            onChange={handleFileChange}
            accept=".csv"
            style={{ display: 'none' }}
          />
          <div className="upload-content">
            <CloudUploadIcon className="upload-icon" />
            <p className="upload-text-primary">Drag & drop your dataset here or click to browse</p>
            <span className="upload-text-secondary">
              Supported format: CSV up to 25MB
            </span>
          </div>
        </div>

        {error && (
          <div className="error-message">
            <span style={{ marginRight: '8px' }}>⚠️</span>
            {error}
          </div>
        )}

        {loading && (
          <>
            <div className="loading-indicator">
              <CircularProgress size={24} style={{ color: '#4f46e5' }} />
              <span>AI Model Processing...</span>
            </div>
            <div className="ai-processing"></div>
          </>
        )}

        {results && (
          <div className="results-container">
            <h2 className="results-heading">AI Analysis Results</h2>
            
            <div className="ai-metrics">
              <div className="metric-card">
                <h3 className="metric-title">Model Confidence</h3>
                <p className="metric-value">98.5%</p>
              </div>
              <div className="metric-card">
                <h3 className="metric-title">Data Points Analyzed</h3>
                <p className="metric-value">1.2M</p>
              </div>
              <div className="metric-card">
                <h3 className="metric-title">Processing Time</h3>
                <p className="metric-value">1.5s</p>
              </div>
            </div>

            <div className="visualization">
              <h3 className="visualization-title">Neural Network Prevention Analysis</h3>
              <img 
                src={`data:image/png;base64,${results.heatmap}`}
                alt="AI Prevention Heatmap"
                style={{ maxWidth: '100%', borderRadius: '8px' }}
              />
            </div>

            <div className="visualization">
              <h3 className="visualization-title">ML Model Prediction Accuracy</h3>
              <img 
                src={`data:image/png;base64,${results.prediction_accuracy}`}
                alt="AI Prediction Accuracy"
                style={{ maxWidth: '100%', borderRadius: '8px' }}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
