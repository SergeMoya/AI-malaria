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
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Ensure tmp directory exists in the same directory as the script
tmp_dir = os.path.join(os.path.dirname(__file__), 'tmp')
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

        # Import analysis functions only when needed
        from .malaria_analysis_french import load_and_clean_data, create_prevention_heatmap, train_model_and_create_prediction_plot

        try:
            # Process the data
            df = load_and_clean_data(temp_path)
            
            # Create visualizations with unique filenames
            import time
            timestamp = int(time.time())
            
            heatmap_filename = f'prevention_heatmap_{timestamp}.png'
            prediction_filename = f'prediction_accuracy_{timestamp}.png'
            
            heatmap_path = os.path.join(tmp_dir, heatmap_filename)
            prediction_path = os.path.join(tmp_dir, prediction_filename)
            
            create_prevention_heatmap(df, heatmap_path)
            train_model_and_create_prediction_plot(df, prediction_path)
            
            return jsonify({
                'message': 'Analysis completed successfully',
                'heatmap': f'/api/image/{heatmap_filename}',
                'prediction': f'/api/image/{prediction_filename}'
            }), 200

        except Exception as e:
            print(f"Error in data processing: {str(e)}")
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500
        finally:
            # Clean up old files
            try:
                for f in os.listdir(tmp_dir):
                    if f.endswith('.png') and f not in [heatmap_filename, prediction_filename]:
                        try:
                            os.remove(os.path.join(tmp_dir, f))
                        except:
                            pass
            except:
                pass

    except Exception as e:
        print(f"Error in analyze_data: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/image/<filename>')
def serve_image(filename):
    try:
        print(f"Attempting to serve image: {filename}")
        image_path = os.path.join(tmp_dir, filename)
        print(f"Full image path: {image_path}")
        
        if not os.path.exists(image_path):
            print(f"Image not found at path: {image_path}")
            return jsonify({'error': f'Image not found: {filename}'}), 404
            
        print(f"Image exists, serving from: {image_path}")
        response = send_file(
            image_path,
            mimetype='image/png'
        )
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
        
    except Exception as e:
        print(f"Error serving image {filename}: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)