import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
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
        locale.setlocale(locale.LC_ALL, 'fra_fra')
    except locale.Error:
        print("Warning: French locale not available, using system default")

# Enable French characters in matplotlib
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']

def load_and_clean_data(file_path):
    """
    Charge et nettoie le jeu de données sur le paludisme.
    
    Args:
        file_path (str): Chemin vers le fichier CSV
        
    Returns:
        pd.DataFrame: Jeu de données nettoyé
    """
    try:
        df = pd.read_csv(file_path)
        # Assuming the same data cleaning steps as the original
        return df
    except Exception as e:
        print(f"Erreur lors du chargement des données: {str(e)}")
        return None

def create_prevention_heatmap(df, output_path):
    """
    Crée une carte de chaleur montrant l'efficacité des mesures de prévention par pays.
    
    Args:
        df (pd.DataFrame): Jeu de données
        output_path (str): Chemin pour sauvegarder la carte de chaleur
    """
    try:
        # Calculate average malaria incidence and prevention measures by country
        country_stats = df.groupby('Country Name').agg({
            'Incidence of malaria (per 1,000 population at risk)': 'mean',
            'Use of insecticide-treated bed nets (% of under-5 population)': 'mean',
            'Children with fever receiving antimalarial drugs (% of children under age 5 with fever)': 'mean'
        }).round(2)
        
        # Rename columns for better display
        country_stats.columns = [
            'Incidence du Paludisme',
            'Utilisation de Moustiquaires',
            'Traitement Antipaludique'
        ]
        
        # Calculate correlations
        prevention_correlation = country_stats.corr()
        
        # Create heatmap
        plt.figure(figsize=(12, 10))
        sns.heatmap(prevention_correlation, 
                    cmap='RdBu_r',
                    center=0,
                    annot=True,
                    fmt='.2f',
                    cbar_kws={'label': 'Coefficient de Corrélation'})
        
        plt.title('Corrélation entre les Mesures de Prévention du Paludisme', pad=20)
        plt.tight_layout()
        
        # Save plot with high DPI for publication
        plt.savefig(output_path, dpi=600, bbox_inches='tight')
        plt.close()
        
        print("\nAnalyse de Corrélation:")
        print(prevention_correlation)
        
    except Exception as e:
        print(f"Erreur lors de la création de la carte de chaleur: {str(e)}")

def train_model_and_create_prediction_plot(df, output_path):
    """
    Entraîne un modèle RandomForest et crée un graphique de précision des prédictions.
    
    Args:
        df (pd.DataFrame): Jeu de données
        output_path (str): Chemin pour sauvegarder le graphique
    """
    try:
        # Prepare features and target
        X = df[[
            'Use of insecticide-treated bed nets (% of under-5 population)',
            'Children with fever receiving antimalarial drugs (% of children under age 5 with fever)'
        ]].fillna(0)  # Replace NaN with 0 for this analysis
        y = df['Incidence of malaria (per 1,000 population at risk)'].fillna(0)
        
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
        
        # Create prediction plot
        plt.figure(figsize=(12, 8))
        plt.scatter(y_test, y_pred, alpha=0.5)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        
        plt.xlabel('Incidence Réelle du Paludisme\n(pour 1000 habitants à risque)')
        plt.ylabel('Incidence Prédite du Paludisme\n(pour 1000 habitants à risque)')
        plt.title('Précision des Prédictions du Modèle', pad=20)
        
        # Add metrics to plot in French
        plt.text(0.05, 0.95, f'R² = {r2:.3f}\nRMSE = {rmse:.3f}',
                transform=plt.gca().transAxes,
                bbox=dict(facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        
        # Save plot with high DPI for publication
        plt.savefig(output_path, dpi=600, bbox_inches='tight')
        plt.close()
        
        print("\nMétriques de Performance du Modèle:")
        print(f"Score R²: {r2:.3f}")
        print(f"RMSE: {rmse:.3f}")
        
        # Feature importance with French labels
        feature_importance = pd.DataFrame({
            'caractéristique': ['Utilisation de Moustiquaires', 'Traitement Antipaludique'],
            'importance': model.feature_importances_
        })
        print("\nImportance des Caractéristiques:")
        print(feature_importance.sort_values('importance', ascending=False))
        
        return r2, rmse
        
    except Exception as e:
        print(f"Erreur dans l'entraînement du modèle et le graphique de prédiction: {str(e)}")
        return None, None

def main():
    """
    Fonction principale pour exécuter l'analyse du paludisme.
    """
    # Setup paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "data", "DatasetAfricaMalaria.csv")
    output_dir = current_dir
    
    heatmap_path = os.path.join(output_dir, "prevention_effectiveness_heatmap_fr.png")
    prediction_path = os.path.join(output_dir, "prediction_accuracy_plot_fr.png")
    
    print("Démarrage de l'Analyse de la Prévention du Paludisme...")
    
    # Load and clean data
    df = load_and_clean_data(data_path)
    if df is None:
        return
    
    print("\nCréation des visualisations...")
    
    # Create visualizations
    create_prevention_heatmap(df, heatmap_path)
    r2, rmse = train_model_and_create_prediction_plot(df, prediction_path)
    
    if r2 is not None and rmse is not None:
        print(f"\nAnalyse terminée. Résultats sauvegardés dans le répertoire '{output_dir}'")

if __name__ == "__main__":
    main()
