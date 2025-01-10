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

        # Create heatmap
        plt.figure(figsize=(10, 8))
        plt.style.use('default')
        
        # Create heatmap using matplotlib
        im = plt.imshow(correlation_matrix, cmap='RdYlBu_r')
        
        # Add colorbar
        plt.colorbar(im, label='Coefficient de corrélation')
        
        # Add labels with French translations
        french_labels = {
            'bed_nets': 'Moustiquaires',
            'antimalarial_medication': 'Médicaments',
            'malaria_incidence': 'Cas de Paludisme'
        }
        
        labels = [french_labels[col] for col in numeric_columns]
        plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
        plt.yticks(range(len(labels)), labels)
        
        # Add title
        plt.title('Carte de Chaleur de la Corrélation\nentre les Mesures de Prévention')
        
        # Add correlation values
        for i in range(len(correlation_matrix)):
            for j in range(len(correlation_matrix)):
                plt.text(j, i, f'{correlation_matrix.iloc[i, j]:.2f}',
                        ha='center', va='center', color='black')
        
        # Adjust layout
        plt.tight_layout()
        
        # Save plot
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
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
        X = df[['bed_nets', 'antimalarial_medication']]  # Features
        y = df['malaria_incidence']  # Target

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

        # Create prediction accuracy plot
        plt.figure(figsize=(12, 8))
        plt.style.use('default')
        
        # Plot actual vs predicted values
        plt.scatter(y_test, y_pred, alpha=0.5, label='Prédictions')
        
        # Add perfect prediction line
        min_val = min(y_test.min(), y_pred.min())
        max_val = max(y_test.max(), y_pred.max())
        plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Prédiction Parfaite')
        
        # Add labels and title
        plt.xlabel('Cas de Paludisme (Réels)')
        plt.ylabel('Cas de Paludisme (Prédits)')
        plt.title(f'Précision des Prédictions\nR² = {r2:.3f}, RMSE = {rmse:.3f}')
        
        # Add legend
        plt.legend()
        
        # Add grid
        plt.grid(True, alpha=0.3)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save plot
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()

    except Exception as e:
        raise Exception(f"Erreur lors de la création du graphique de prédiction: {str(e)}")