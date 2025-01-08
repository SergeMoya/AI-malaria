from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from ..malaria_analysis_french import load_and_clean_data, get_prevention_data, train_model_and_get_predictions

app = Flask(__name__)
CORS(app)

# Ensure upload directory exists
UPLOAD_FOLDER = '/tmp'  # Use /tmp for Vercel
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, 'DatasetAfricaMalaria.csv')
    file.save(filepath)

    try:
        # Process the data
        df = load_and_clean_data(filepath)
        if df is None:
            return jsonify({'error': 'Error loading data'}), 500

        # Get analysis data
        prevention_data = get_prevention_data(df)
        prediction_data = train_model_and_get_predictions(df)

        # Clean up the uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({
            'success': True,
            'prevention_data': prevention_data,
            'prediction_data': prediction_data
        })
    except Exception as e:
        # Clean up the uploaded file in case of error
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})
