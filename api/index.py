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
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Only CSV files are supported'}), 400

        # Save file temporarily
        temp_path = os.path.join(tmp_dir, 'uploaded_data.csv')
        file.save(temp_path)

        try:
            # Load and process data
            df = load_and_clean_data(temp_path)
            
            # Generate visualizations
            heatmap_path = os.path.join(tmp_dir, 'prevention_heatmap.png')
            prediction_path = os.path.join(tmp_dir, 'prediction_accuracy_plot_fr.png')
            
            create_prevention_heatmap(df, heatmap_path)
            train_model_and_create_prediction_plot(df, prediction_path)
            
            return jsonify({
                'success': True,
                'heatmap': 'prevention_heatmap.png',
                'prediction_plot': 'prediction_accuracy_plot_fr.png'
            })

        except Exception as e:
            print("Error processing data:", str(e))
            traceback.print_exc()
            return jsonify({'error': f'Error processing data: {str(e)}'}), 500

        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    except Exception as e:
        print("Error in analyze_data:", str(e))
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/image/<filename>')
def serve_image(filename):
    try:
        image_path = os.path.join(tmp_dir, filename)
        if not os.path.exists(image_path):
            return jsonify({'error': 'Image not found'}), 404
        return send_file(image_path, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5328)
