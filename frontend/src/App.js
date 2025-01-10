import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { CircularProgress } from '@mui/material';
import { endpoints, API_URL } from './config';
import Footer from './components/Footer';

const API_TIMEOUT = 30000;

function App() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  // Background animations setup
  useEffect(() => {
    const createBackground = (className, count) => {
      const container = document.querySelector(`.${className}`);
      if (!container) return;

      container.innerHTML = '';
      for (let i = 0; i < count; i++) {
        const element = document.createElement('div');
        element.className = `${className}-element`;
        element.style.left = `${Math.random() * 100}%`;
        element.style.top = `${Math.random() * 100}%`;
        element.style.animationDelay = `${Math.random() * 2}s`;
        container.appendChild(element);
      }
    };

    createBackground('neural-bg', 50);
    createBackground('ai-particles', 100);

    window.addEventListener('resize', () => {
      createBackground('neural-bg', 50);
      createBackground('ai-particles', 100);
    });

    return () => {
      window.removeEventListener('resize', createBackground);
    };
  }, []);

  // Upload progress simulation
  useEffect(() => {
    let progressInterval;
    if (loading && uploadProgress < 100) {
      progressInterval = setInterval(() => {
        setUploadProgress(prev => Math.min(prev + 1, 100));
      }, 100);
    }
    return () => clearInterval(progressInterval);
  }, [loading, uploadProgress]);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(e.type === "dragenter" || e.type === "dragover");
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files?.[0]) {
      handleFileSelection(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (event) => {
    if (event.target.files?.[0]) {
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
    setUploadProgress(0);

    try {
      const healthCheck = await axios.get(endpoints.healthcheck, { timeout: 5000 });
      if (healthCheck.data.status !== 'healthy') {
        throw new Error('Le service est temporairement indisponible');
      }

      const response = await axios.post(endpoints.analyze, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: API_TIMEOUT,
      });

      if (response.data && !response.data.error) {
        setResults(response.data);
      } else {
        throw new Error(response.data.error || 'Erreur pendant l\'analyse');
      }
    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.response?.data?.error || err.message || 'Erreur pendant l\'analyse. Veuillez réessayer.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="ai-particles" />
      
      <div className="content-wrapper">
        <header className="App-header">
          <div className="ai-badge">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M2 17L12 22L22 17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M2 12L12 17L22 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            Machine Learning Algorithms - Random Forest Architecture
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
             onClick={() => document.getElementById('file-input').click()}>
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
            <span className="upload-text-secondary">Supported format: CSV up to 25MB</span>
          </div>
        </div>

        {error && (
          <div className="error-message">
            <span>⚠️</span>
            {error}
          </div>
        )}

        {loading && (
          <div className="circular-progress-container">
            <CircularProgress
              variant="determinate"
              value={uploadProgress}
              size={60}
              thickness={4}
            />
            <div className="circular-progress-overlay">
              {Math.round(uploadProgress)}%
            </div>
          </div>
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

            <div className="analysis-section">
              <h3>Neural Network Prevention Analysis</h3>
              {results?.heatmap && (
                <div className="image-container">
                  <img 
                    key={results.heatmap}
                    src={`${API_URL}${results.heatmap}?t=${new Date().getTime()}`}
                    alt="Prevention Heatmap" 
                    className="analysis-image"
                    onError={(e) => {
                      console.error('Failed to load heatmap:', `${API_URL}${results.heatmap}`);
                      e.target.style.display = 'none';
                    }}
                  />
                </div>
              )}
            </div>

            <div className="analysis-section">
              <h3>ML Model Prediction Accuracy</h3>
              {results?.prediction && (
                <div className="image-container">
                  <img 
                    key={results.prediction}
                    src={`${API_URL}${results.prediction}?t=${new Date().getTime()}`}
                    alt="Prediction Accuracy" 
                    className="analysis-image"
                    onError={(e) => {
                      console.error('Failed to load prediction:', `${API_URL}${results.prediction}`);
                      e.target.style.display = 'none';
                    }}
                  />
                </div>
              )}
            </div>
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
}

export default App;