from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

app = Flask(__name__)
CORS(app)

def load_and_clean_data(data):
    try:
        # Convert the uploaded file data directly to a DataFrame
        df = pd.read_csv(data)
        
        # Your existing data cleaning logic
        columns_to_drop = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']
        df = df.drop(columns=columns_to_drop)
        df = df.melt(id_vars=[], var_name='Year', value_name='Value')
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        df = df.dropna()
        return df
    except Exception as e:
        print(f"Error in load_and_clean_data: {str(e)}")
        return None

def train_model_and_get_predictions(df):
    try:
        # Prepare features and target
        X = df[['Year']].values
        y = df['Value'].values
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        
        # Generate future predictions
        future_years = np.array([[year] for year in range(2024, 2031)])
        future_predictions = model.predict(future_years)
        
        return {
            'accuracy': accuracy,
            'future_predictions': [
                {'year': int(year[0]), 'prediction': float(pred)}
                for year, pred in zip(future_years, future_predictions)
            ]
        }
    except Exception as e:
        print(f"Error in train_model_and_get_predictions: {str(e)}")
        return None

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Process the data directly from the uploaded file
        df = load_and_clean_data(file)
        if df is None:
            return jsonify({'error': 'Error loading data'}), 500

        # Get predictions
        results = train_model_and_get_predictions(df)
        if results is None:
            return jsonify({'error': 'Error making predictions'}), 500

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

# For local development
if __name__ == '__main__':
    app.run(debug=True)
