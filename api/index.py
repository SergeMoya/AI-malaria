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
CORS(app)

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    """
    Add CORS headers to all responses.
    """
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    header['Access-Control-Allow-Headers'] = 'Content-Type'
    header['Access-Control-Max-Age'] = '86400'  # 24 hours
    return response

# Ensure tmp directory exists
tmp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tmp')
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

# Global variables for caching
_model = None
_scaler = None
_data = None

def init_model():
    global _model
    if _model is None:
        _model = RandomForestClassifier(n_estimators=100, random_state=42)

def get_model():
    global _model
    if _model is None:
        model_path = os.path.join(os.path.dirname(__file__), 'model', 'malaria_model.joblib')
        if os.path.exists(model_path):
            _model = joblib.load(model_path)
    return _model

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

@app.route('/api/')
def api_root():
    return jsonify({
        "message": "Welcome to Malaria Detection API",
        "version": "1.0.0",
        "endpoints": {
            "healthcheck": "/api/healthcheck",
            "analyze": "/api/analyze"
        }
    }), 200

@app.route('/api/healthcheck')
def healthcheck():
    """
    Healthcheck endpoint
    """
    logger.info("Healthcheck endpoint called")
    return jsonify({"status": "healthy"}), 200

def analyze_data(file):
    try:
        # Save the file temporarily
        temp_path = os.path.join(tmp_dir, 'temp_data.csv')
        file.save(temp_path)

        # Read data efficiently
        df = pd.read_csv(temp_path, low_memory=True)
        
        # Process data in chunks if needed
        chunk_size = 1000
        results = []
        
        for i in range(0, len(df), chunk_size):
            chunk = df[i:i + chunk_size]
            # Process chunk
            processed_chunk = process_chunk(chunk)
            results.append(processed_chunk)
        
        # Combine results
        final_results = pd.concat(results) if len(results) > 1 else results[0]
        
        # Import analysis functions only when needed
        from .malaria_analysis_french import load_and_clean_data, create_prevention_heatmap, train_model_and_create_prediction_plot

        # Process the data
        df = load_and_clean_data(temp_path)
        
        # Create visualizations
        heatmap_path = os.path.join(tmp_dir, 'prevention_heatmap.png')
        create_prevention_heatmap(df, heatmap_path)
        
        prediction_path = os.path.join(tmp_dir, 'prediction_accuracy.png')
        train_model_and_create_prediction_plot(df, prediction_path)
        
        # Save the model for future use
        model_dir = os.path.join(os.path.dirname(__file__), 'model')
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        
        return {
            'message': 'Analysis completed successfully',
            'heatmap': '/api/image/prevention_heatmap.png',
            'prediction': '/api/image/prediction_accuracy.png',
            'results': final_results.to_dict(orient='records')
        }

    except Exception as e:
        print(f"Error processing data: {str(e)}")
        traceback.print_exc()
        return {"error": str(e)}

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

        # Process the file and get results
        results = analyze_data(file)
        return jsonify(results), 200

    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

def process_chunk(chunk):
    # Initialize model if needed
    init_model()
    
    # Process chunk efficiently
    chunk = chunk.copy()
    
    # Your processing logic here
    # Make sure to use efficient operations
    # Avoid unnecessary copies
    # Use inplace operations where possible
    
    return chunk

@app.route('/api/image/<filename>')
def serve_image(filename):
    try:
        return send_file(
            os.path.join(tmp_dir, filename),
            mimetype='image/png'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
