from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
from malaria_analysis_french import load_and_clean_data, create_prevention_heatmap, train_model_and_create_prediction_plot

app = Flask(__name__, static_folder='static')
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists('static'):
    os.makedirs('static')

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

    # Process the data
    df = load_and_clean_data(filepath)
    if df is None:
        return jsonify({'error': 'Error loading data'}), 500

    # Generate visualizations
    heatmap_path = 'prevention_effectiveness_heatmap_fr.png'
    prediction_path = 'prediction_accuracy_plot_fr.png'

    create_prevention_heatmap(df, os.path.join('static', heatmap_path))
    r2, rmse = train_model_and_create_prediction_plot(df, os.path.join('static', prediction_path))

    return jsonify({
        'success': True,
        'metrics': {
            'r2': float(r2) if r2 is not None else None,
            'rmse': float(rmse) if rmse is not None else None
        },
        'visualizations': {
            'heatmap': f'/static/{heatmap_path}',
            'prediction': f'/static/{prediction_path}'
        }
    })

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
