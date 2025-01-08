from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import traceback
import sys
from pathlib import Path

# Import from the same directory
from .malaria_analysis_french import load_and_clean_data, create_prevention_heatmap, train_model_and_create_prediction_plot

app = Flask(__name__)
CORS(app)

# Edge Function configuration
app.config['EDGE_FUNCTION'] = True

# Ensure tmp directory exists
tmp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tmp')
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

@app.route('/api/healthcheck')
def healthcheck():
    return jsonify({"status": "healthy", "version": "1.0.0"}), 200

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    try:
        # Get the uploaded file from the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Save the file temporarily
        temp_path = os.path.join(tmp_dir, 'temp_data.csv')
        file.save(temp_path)

        # Process the data
        df = load_and_clean_data(temp_path)
        
        # Create visualizations
        heatmap_path = os.path.join(tmp_dir, 'prevention_heatmap.png')
        create_prevention_heatmap(df, heatmap_path)
        
        prediction_path = os.path.join(tmp_dir, 'prediction_accuracy.png')
        train_model_and_create_prediction_plot(df, prediction_path)
        
        return jsonify({
            'message': 'Analysis completed successfully',
            'heatmap': '/api/image/prevention_heatmap.png',
            'prediction': '/api/image/prediction_accuracy.png'
        }), 200

    except Exception as e:
        print(f"Error processing data: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/image/<filename>')
def serve_image(filename):
    try:
        return send_file(
            os.path.join(tmp_dir, filename),
            mimetype='image/png'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# For local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5328)
