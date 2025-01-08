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

app = Flask(__name__)
CORS(app)

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

@app.route('/')
def root():
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
    return jsonify({"status": "healthy", "version": "1.0.0"}), 200

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

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
        
        return jsonify({
            'message': 'Analysis completed successfully',
            'heatmap': '/api/image/prevention_heatmap.png',
            'prediction': '/api/image/prediction_accuracy.png',
            'results': final_results.to_dict(orient='records')
        }), 200

    except Exception as e:
        print(f"Error processing data: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
