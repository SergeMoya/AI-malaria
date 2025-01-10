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
import time

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import the analysis module (using absolute import)
from malaria_analysis_french import load_and_clean_data, create_prevention_heatmap, train_model_and_create_prediction_plot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Ensure tmp directory exists
tmp_dir = os.path.join(os.path.dirname(__file__), 'tmp')
os.makedirs(tmp_dir, exist_ok=True)

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
            "analyze": "/api/analyze",
            "demo": "/api/demo"
        }
    }), 200

@app.route('/api/healthcheck')
def healthcheck():
    return jsonify({"status": "healthy", "version": "1.0.0"}), 200

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    try:
        # Add detailed logging
        app.logger.info("Starting analysis request")
        
        if 'file' not in request.files:
            app.logger.error("No file in request")
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            app.logger.error("Empty filename")
            return jsonify({'error': 'No file selected'}), 400

        # Create tmp directory if it doesn't exist
        os.makedirs(tmp_dir, exist_ok=True)
        app.logger.info(f"Temporary directory confirmed at: {tmp_dir}")

        # Save the file temporarily
        temp_path = os.path.join(tmp_dir, 'temp_data.csv')
        file.save(temp_path)
        app.logger.info(f"File saved temporarily at: {temp_path}")

        try:
            # Process the data
            app.logger.info("Loading and cleaning data")
            df = load_and_clean_data(temp_path)
            
            # Create visualizations with unique filenames
            timestamp = int(time.time())
            
            heatmap_filename = f'prevention_heatmap_{timestamp}.png'
            prediction_filename = f'prediction_accuracy_{timestamp}.png'
            
            heatmap_path = os.path.join(tmp_dir, heatmap_filename)
            prediction_path = os.path.join(tmp_dir, prediction_filename)
            
            app.logger.info("Creating heatmap")
            create_prevention_heatmap(df, heatmap_path)
            app.logger.info("Creating prediction plot")
            train_model_and_create_prediction_plot(df, prediction_path)
            
            app.logger.info("Analysis completed successfully")
            return jsonify({
                'message': 'Analysis completed successfully',
                'heatmap': f'/api/image/{heatmap_filename}',
                'prediction': f'/api/image/{prediction_filename}'
            }), 200

        except Exception as e:
            app.logger.error(f"Error in data processing: {str(e)}")
            app.logger.error(traceback.format_exc())
            return jsonify({
                'error': 'Error processing data',
                'details': str(e),
                'trace': traceback.format_exc()
            }), 500
        finally:
            # Clean up old files
            try:
                for f in os.listdir(tmp_dir):
                    if f.endswith('.csv') or (f.endswith('.png') and f != heatmap_filename and f != prediction_filename):
                        os.remove(os.path.join(tmp_dir, f))
            except Exception as cleanup_error:
                app.logger.error(f"Error during cleanup: {str(cleanup_error)}")

    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({
            'error': 'Unexpected error occurred',
            'details': str(e),
            'trace': traceback.format_exc()
        }), 500

@app.route('/api/demo', methods=['GET'])
def demo_analysis():
    try:
        app.logger.info("Starting demo analysis")
        
        # Path to the demo dataset
        demo_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'DatasetAfricaMalaria.csv')
        
        if not os.path.exists(demo_file):
            app.logger.error(f"Demo file not found at: {demo_file}")
            return jsonify({'error': 'Demo file not found'}), 404

        app.logger.info(f"Using demo file from: {demo_file}")

        try:
            # Process the data using existing functions
            app.logger.info("Loading and cleaning demo data")
            df = load_and_clean_data(demo_file)
            
            # Create visualizations with unique filenames
            timestamp = int(time.time())
            heatmap_filename = f'prevention_heatmap_{timestamp}.png'
            prediction_filename = f'prediction_accuracy_{timestamp}.png'
            
            heatmap_path = os.path.join(tmp_dir, heatmap_filename)
            prediction_path = os.path.join(tmp_dir, prediction_filename)
            
            app.logger.info("Creating prevention heatmap")
            create_prevention_heatmap(df, heatmap_path)
            
            app.logger.info("Training model and creating prediction plot")
            train_model_and_create_prediction_plot(df, prediction_path)
            
            # Return the results
            return jsonify({
                'message': 'Demo analysis completed successfully',
                'heatmap': f'/api/image/{heatmap_filename}',
                'prediction': f'/api/image/{prediction_filename}'
            }), 200
            
        except Exception as e:
            app.logger.error(f"Error processing demo data: {str(e)}")
            return jsonify({'error': f'Error processing demo data: {str(e)}'}), 500
            
    except Exception as e:
        app.logger.error(f"Demo analysis error: {str(e)}\n{traceback.format_exc()}")
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