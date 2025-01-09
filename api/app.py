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

"""
Malaria Analysis API

This Flask application provides an API for analyzing malaria-related data and generating
visualizations. It accepts CSV data files containing malaria statistics and returns
visual analytics including heat maps of prevention/prevalence and prediction accuracy graphs.

Key Features:
- File upload and processing of malaria-related CSV data
- Generation of heat maps showing malaria prevention/prevalence patterns
- Prediction accuracy visualization
- CORS support for cross-origin requests
- Detailed request logging
- Healthcheck endpoint for monitoring
- Temporary file storage for processing
"""

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

@app.after_request
def after_request(response):
    """
    Add CORS headers to all responses.
    
    Args:
        response: The Flask response object
        
    Returns:
        Response object with CORS headers added
    """
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    header['Access-Control-Allow-Headers'] = 'Content-Type'
    header['Access-Control-Max-Age'] = '86400'  # 24 hours
    return response

# Ensure tmp directory exists for file processing
tmp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tmp')
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

def generate_heatmap():
    """
    Generates a heatmap visualization of malaria prevention/prevalence data.
    Currently using sample data - should be replaced with actual data processing.
    
    Returns:
        str: Base64 encoded PNG image of the heatmap
    """
    # Sample data for the heatmap
    data = np.random.rand(10, 10)  # Replace with actual malaria prevention/prevalence data
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
    """
    Generates a line graph showing the accuracy of malaria prediction models over time.
    Currently using sample data - should be replaced with actual prediction metrics.
    
    Returns:
        str: Base64 encoded PNG image of the prediction accuracy graph
    """
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
    """
    Healthcheck endpoint for monitoring API status.
    
    Returns:
        JSON response with API status
    """
    logger.info("Healthcheck endpoint called")
    return jsonify({"status": "healthy"}), 200

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Endpoint for analyzing uploaded malaria data files.
    Expects a CSV file upload containing malaria-related statistics.
    
    Returns:
        JSON containing:
        - Generated heatmap visualization
        - Prediction accuracy graph
        - Processing status and messages
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

@app.before_request
def log_request_info():
    """
    Log all incoming requests for debugging and monitoring purposes.
    """
    logger.debug('Headers: %s', request.headers)
    logger.debug('Body: %s', request.get_data())
    logger.debug('URL: %s', request.url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
