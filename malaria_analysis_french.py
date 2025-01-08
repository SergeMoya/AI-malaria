import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import os

def load_and_clean_data(filepath):
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def get_prevention_data(df):
    # Calculate correlation between prevention methods and malaria cases
    prevention_columns = [
        'Use of insecticide-treated bed nets (% of under-5 population)',
        'Children with fever receiving antimalarial drugs (% of children under age 5 with'
    ]
    cases_column = 'Incidence of malaria (per 1,000 population at risk)'
    
    correlation_data = []
    for col in prevention_columns:
        if col in df.columns:
            correlation = df[col].corr(df[cases_column])
            correlation_data.append({
                'prevention_method': col,
                'correlation': correlation if not pd.isna(correlation) else 0
            })
    
    return correlation_data

def train_model_and_get_predictions(df):
    # Use Year as feature and malaria incidence as target
    X = df[['Year']].values
    y = df['Incidence of malaria (per 1,000 population at risk)'].values
    
    # Remove any rows where y is NaN
    mask = ~np.isnan(y)
    X = X[mask]
    y = y[mask]
    
    if len(X) == 0 or len(y) == 0:
        return {
            'actual': [],
            'predicted': [],
            'years': [],
            'metrics': {
                'r2': 0,
                'rmse': 0
            }
        }
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    prediction_data = {
        'actual': y_test.tolist(),
        'predicted': y_pred.tolist(),
        'years': X_test.flatten().tolist(),
        'metrics': {
            'r2': float(r2),
            'rmse': float(rmse)
        }
    }
    
    return prediction_data

def main():
    """
    Fonction principale pour exécuter l'analyse du paludisme.
    """
    # Setup paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "data", "DatasetAfricaMalaria.csv")
    output_dir = current_dir
    
    print("Démarrage de l'Analyse de la Prévention du Paludisme...")
    
    # Load and clean data
    df = load_and_clean_data(data_path)
    if df is None:
        return
    
    print("\nCréation des données...")
    
    # Create data
    prevention_data = get_prevention_data(df)
    prediction_data = train_model_and_get_predictions(df)
    
    print("\nDonnées créées avec succès.")
    print("Données de prévention :")
    print(prevention_data)
    print("Données de prédiction :")
    print(prediction_data)

if __name__ == "__main__":
    main()
