import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg before importing pyplot
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import os

# Set matplotlib to use French locale and proper encoding
import locale
import sys
import codecs

# Set up UTF-8 encoding for console output
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

# Try to set French locale, fall back to English if not available
try:
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'fr_FR')
    except locale.Error:
        pass  # Fall back to default locale

def load_and_clean_data(file_path):
    """
    Charge et nettoie le jeu de données sur le paludisme.
    
    Args:
        file_path (str): Chemin vers le fichier CSV
        
    Returns:
        pd.DataFrame: Jeu de données nettoyé
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Rename columns for easier access
        column_mapping = {
            'Country Name': 'country',
            'Use of insecticide-treated bed nets (% of under-5 population)': 'bed_nets',
            'Children with fever receiving antimalarial drugs (% of children under age 5 with fever)': 'antimalarial_medication',
            'Incidence of malaria (per 1,000 population at risk)': 'malaria_incidence'
        }
        
        # Verify required columns exist
        missing_columns = [col for col in column_mapping.keys() if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Colonnes manquantes dans le fichier: {', '.join(missing_columns)}")
        
        # Rename columns
        df = df.rename(columns=column_mapping)
        
        # Select only needed columns
        df = df[['country', 'bed_nets', 'antimalarial_medication', 'malaria_incidence']]
        
        # Remove any rows with missing values
        df = df.dropna()
        
        return df
    except Exception as e:
        raise Exception(f"Erreur lors du chargement des données: {str(e)}")

def create_prevention_heatmap(df, output_path):
    """
    Crée une carte de chaleur montrant l'efficacité des mesures de prévention par pays.
    
    Args:
        df (pd.DataFrame): Jeu de données
        output_path (str): Chemin pour sauvegarder la carte de chaleur
    """
    try:
        # Select only numeric columns for correlation
        numeric_columns = ['bed_nets', 'antimalarial_medication', 'malaria_incidence']
        correlation_matrix = df[numeric_columns].corr()

        # Create figure with specified size
        plt.figure(figsize=(12, 10))
        
        # Create heatmap using seaborn for better styling
        sns.heatmap(correlation_matrix, 
                   annot=True,  # Show correlation values
                   fmt='.2f',   # Format to 2 decimal places
                   cmap='RdYlBu_r',  # Red-Yellow-Blue colormap
                   square=True,  # Make cells square
                   cbar_kws={'label': 'Coefficient de corrélation'})
        
        # French translations for labels
        french_labels = {
            'bed_nets': 'Moustiquaires',
            'antimalarial_medication': 'Médicaments',
            'malaria_incidence': 'Cas de Paludisme'
        }
        
        # Update labels
        plt.xticks(np.arange(len(french_labels)) + 0.5, [french_labels[col] for col in numeric_columns], rotation=0)
        plt.yticks(np.arange(len(french_labels)) + 0.5, [french_labels[col] for col in numeric_columns], rotation=0)
        
        # Add title
        plt.title('Carte de Chaleur de la Corrélation\nentre les Mesures de Prévention', 
                 pad=20, fontsize=14, fontweight='bold')
        
        # Adjust layout
        plt.tight_layout()
        
        # Save figure
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
    except Exception as e:
        raise Exception(f"Erreur lors de la création de la carte de chaleur: {str(e)}")

def train_model_and_create_prediction_plot(df, output_path):
    """
    Entraîne un modèle RandomForest et crée un graphique de précision des prédictions.
    
    Args:
        df (pd.DataFrame): Jeu de données
        output_path (str): Chemin pour sauvegarder le graphique
    """
    try:
        # Prepare features and target
        X = df[['bed_nets', 'antimalarial_medication']]
        y = df['malaria_incidence']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        # Create figure
        plt.figure(figsize=(12, 8))
        
        # Create scatter plot
        plt.scatter(y_test, y_pred, alpha=0.5, color='#3498db', label='Prédictions')
        
        # Add perfect prediction line
        max_val = max(max(y_test), max(y_pred))
        min_val = min(min(y_test), min(y_pred))
        plt.plot([min_val, max_val], [min_val, max_val], '--', color='#e74c3c', 
                label='Prédiction Parfaite', linewidth=2)
        
        # Customize plot
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xlabel('Cas de Paludisme (Réels)', fontsize=12)
        plt.ylabel('Cas de Paludisme (Prédits)', fontsize=12)
        plt.title(f'Précision des Prédictions\nR² = {r2:.3f}, RMSE = {rmse:.3f}', 
                 pad=20, fontsize=14, fontweight='bold')
        
        # Add legend
        plt.legend(fontsize=10)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save figure with high resolution
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
    except Exception as e:
        raise Exception(f"Erreur lors de la création du graphique de prédiction: {str(e)}")
