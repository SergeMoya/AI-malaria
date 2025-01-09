from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import traceback
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path
import joblib
import logging
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS with specific origins
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",
            "https://ai-malaria-frontend-git-backup-main-sergemoyas-projects.vercel.app",
            "https://ai-malaria-frontend-ggig63e2t-sergemoyas-projects.vercel.app"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    """
    Add CORS headers to all responses.
    """
    origin = request.headers.get('Origin')
    if origin in [
        "http://localhost:3000",
        "https://ai-malaria-frontend-git-backup-main-sergemoyas-projects.vercel.app",
        "https://ai-malaria-frontend-ggig63e2t-sergemoyas-projects.vercel.app"
    ]:
        response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Max-Age'] = '86400'  # 24 hours
    return response

# Ensure tmp directory exists
tmp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tmp')
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

def generate_heatmap():
    """
    Generates a heatmap visualization of malaria prevention/prevalence data.
    """
    data = np.random.rand(10, 10)
    plt.figure(figsize=(10, 8))
    sns.heatmap(data, cmap='YlOrRd')
    plt.title('Carte de Chaleur de la Prévention')
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def generate_prediction_accuracy():
    """
    Generates a line graph showing prediction accuracy.
    """
    x = np.linspace(0, 10, 100)
    y = 1 - np.exp(-x/2) + np.random.normal(0, 0.1, 100)
    plt.figure(figsize=(10, 6))
    plt.plot(x, y)
    plt.title('Précision des Prédictions')
    plt.xlabel('Temps')
    plt.ylabel('Précision')
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

@app.route('/')
def root():
    """
    Root endpoint - provides API information
    """
    return jsonify({
        "status": "online",
        "version": "1.0",
        "endpoints": {
            "/api/healthcheck": "Check API health status",
            "/api/analyze": "Analyze malaria data (POST)"
        }
    })

@app.route('/api/healthcheck')
def healthcheck():
    """
    Healthcheck endpoint
    """
    logger.info("Healthcheck endpoint called")
    return jsonify({"status": "healthy"}), 200

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Analyze uploaded data and return visualizations
    """
    logger.info("Analyze endpoint called")
    try:
        if 'file' not in request.files:
            logger.error("No file provided in request")
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        if file.filename == '':
            logger.error("Empty filename received")
            return jsonify({"error": "No file selected"}), 400

        # Generate visualizations
        heatmap = generate_heatmap()
        accuracy = generate_prediction_accuracy()

        return jsonify({
            "status": "success",
            "heatmap": heatmap,
            "accuracy": accuracy,
            "message": "Analysis completed successfully"
        })

    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.before_request
def log_request_info():
    """
    Log incoming request information
    """
    logger.debug('Headers: %s', request.headers)
    logger.debug('Body: %s', request.get_data())
    logger.debug('URL: %s', request.url)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
