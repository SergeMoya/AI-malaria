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
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",
            "https://ai-malaria.onrender.com",
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Ensure tmp directory exists
tmp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tmp')
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

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

        logger.info(f"Processing file: {file.filename}")
        
        # Save the file temporarily
        temp_path = os.path.join(tmp_dir, 'temp_data.csv')
        file.save(temp_path)
        logger.info(f"File saved to: {temp_path}")

        # Generate visualizations
        heatmap = generate_heatmap()
        prediction_accuracy = generate_prediction_accuracy()

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
