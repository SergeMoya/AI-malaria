from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import traceback
from pathlib import Path
import logging
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Update CORS configuration to be more specific
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://ai-malaria-frontend-git-backup-main-sergemoyas-projects.vercel.app",
            "https://ai-malaria-frontend.vercel.app",
            "https://ai-malaria-frontend.onrender.com",
            "http://localhost:3000",  # For local development
            "http://127.0.0.1:3000"   # Alternative local development URL
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    allowed_origins = [
        "https://ai-malaria-frontend-git-backup-main-sergemoyas-projects.vercel.app",
        "https://ai-malaria-frontend.vercel.app",
        "https://ai-malaria-frontend.onrender.com",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    if origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Max-Age'] = '86400'  # 24 hours
    return response

# Update the tmp directory path to be absolute and within the app directory
tmp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp')
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

# Add root endpoint to match what's shown in the API response
@app.route('/')
def root():
    return jsonify({
        "endpoints": {
            "/api/analyze": "Analyze malaria data (POST)",
            "/api/healthcheck": "Check API health status"
        },
        "status": "online",
        "version": "1.0"
    })

def generate_heatmap():
    # Sample data for the heatmap
    data = np.random.rand(10, 10)  # Replace with your actual prevention data
    plt.figure(figsize=(10, 8))
    sns.heatmap(data, cmap='YlOrRd')
    plt.title('Carte de Chaleur de la Prévention')
    
    # Save to bytes
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def generate_prediction_accuracy():
    # Sample data for prediction accuracy
    x = np.linspace(0, 10, 100)
    y = 1 - np.exp(-x/2) + np.random.normal(0, 0.1, 100)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y)
    plt.title('Graphique de Précision des Prédictions')
    plt.xlabel('Temps')
    plt.ylabel('Précision')
    
    # Save to bytes
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

@app.route('/api/healthcheck')
def healthcheck():
    logger.info("Healthcheck endpoint called")
    return jsonify({"status": "healthy"}), 200

@app.route('/api/analyze', methods=['POST'])
def analyze():
    logger.info("Analyze endpoint called")
    try:
        if 'file' not in request.files:
            logger.error("No file provided in request")
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        if file.filename == '':
            logger.error("Empty filename received")
            return jsonify({"error": "No file selected"}), 400

        if not file.filename.endswith('.csv'):
            logger.error("Invalid file type")
            return jsonify({"error": "Only CSV files are allowed"}), 400

        logger.info(f"Processing file: {file.filename}")
        
        # Save the file temporarily
        temp_path = os.path.join(tmp_dir, 'temp_data.csv')
        file.save(temp_path)
        logger.info(f"File saved to: {temp_path}")

        # Generate visualizations
        try:
            heatmap = generate_heatmap()
            prediction_accuracy = generate_prediction_accuracy()
        except Exception as viz_error:
            logger.error(f"Visualization error: {str(viz_error)}")
            return jsonify({"error": "Error generating visualizations"}), 500

        return jsonify({
            "message": "Analyse complétée avec succès",
            "filename": file.filename,
            "status": "success",
            "heatmap": heatmap,
            "prediction_accuracy": prediction_accuracy
        }), 200

    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

# Log all incoming requests
@app.before_request
def log_request_info():
    logger.debug('Headers: %s', request.headers)
    logger.debug('Body: %s', request.get_data())
    logger.debug('URL: %s', request.url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
