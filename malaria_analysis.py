import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import os

def load_and_clean_data(file_path):
    """
    Load and clean the malaria dataset.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Cleaned dataset
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Print column names for debugging
        print("\nOriginal column names:")
        for col in df.columns:
            print(f"'{col}'")
        
        # Rename columns to make them more manageable
        df = df.rename(columns={
            'Country Name': 'country',
            'Incidence of malaria (per 1,000 population at risk)': 'malaria_incidence',
            'Use of insecticide-treated bed nets (% of under-5 population)': 'bed_nets_usage',
            'Children with fever receiving antimalarial drugs (% of children under age 5 with fever)': 'antimalarial_treatment'
        })
        
        # Basic cleaning
        # Drop rows where malaria incidence is missing
        df = df.dropna(subset=['malaria_incidence'])
        
        # Keep only essential columns
        columns_to_keep = ['country', 'Year', 'malaria_incidence', 'bed_nets_usage', 'antimalarial_treatment']
        df = df[columns_to_keep]
        
        # Fill missing values in prevention measures with the mean for that country
        prevention_columns = ['bed_nets_usage', 'antimalarial_treatment']
        for col in prevention_columns:
            df[col] = df.groupby('country')[col].transform(lambda x: x.fillna(x.mean()))
        
        # If there are still NaN values after group mean filling, fill with overall mean
        df[prevention_columns] = df[prevention_columns].fillna(df[prevention_columns].mean())
        
        # Remove any remaining rows with NaN values
        df = df.dropna()
        
        print("\nData Processing Summary:")
        print(f"Number of countries: {df['country'].nunique()}")
        print(f"Year range: {df['Year'].min()} - {df['Year'].max()}")
        print(f"Total number of records: {len(df)}")
        print("\nPreview of cleaned data:")
        print(df.head())
        print("\nData statistics:")
        print(df.describe())
        
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None

def create_prevention_heatmap(df, output_path):
    """
    Create a heatmap showing the correlation between prevention measures and malaria incidence.
    
    Args:
        df (pd.DataFrame): Input dataset
        output_path (str): Path to save the heatmap
    """
    try:
        # Calculate average values by country
        country_stats = df.groupby('country').agg({
            'malaria_incidence': 'mean',
            'bed_nets_usage': 'mean',
            'antimalarial_treatment': 'mean'
        }).round(2)
        
        # Create correlation matrix focusing on prevention measures vs incidence
        prevention_measures = ['bed_nets_usage', 'antimalarial_treatment']
        correlation_matrix = pd.DataFrame(index=['malaria_incidence'])
        
        for measure in prevention_measures:
            correlation_matrix[measure] = country_stats['malaria_incidence'].corr(country_stats[measure])
        
        # Create heatmap
        plt.figure(figsize=(10, 4))
        sns.heatmap(correlation_matrix, 
                    cmap='RdBu_r',
                    center=0,
                    annot=True,
                    fmt='.2f',
                    cbar_kws={'label': 'Correlation Coefficient'})
        
        plt.title('Correlation between Prevention Measures and Malaria Incidence')
        plt.tight_layout()
        
        # Save plot
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print("\nCorrelation Analysis:")
        print("Correlation between prevention measures and malaria incidence:")
        print(correlation_matrix)
        
        # Also calculate correlation between prevention measures themselves
        prevention_correlation = country_stats[prevention_measures].corr()
        print("\nCorrelation between prevention measures:")
        print(prevention_correlation)
        
    except Exception as e:
        print(f"Error creating heatmap: {str(e)}")

def train_model_and_create_prediction_plot(df, output_path):
    """
    Train a RandomForest model and create prediction accuracy plot.
    
    Args:
        df (pd.DataFrame): Input dataset
        output_path (str): Path to save the prediction plot
    """
    try:
        # Prepare features and target
        X = df[['bed_nets_usage', 'antimalarial_treatment']]
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
        
        # Create prediction plot
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test, y_pred, alpha=0.5)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        
        plt.xlabel('Actual Malaria Incidence')
        plt.ylabel('Predicted Malaria Incidence')
        plt.title('Prediction Accuracy Plot')
        
        # Add metrics to plot using plain text
        plt.text(0.05, 0.95, f'R-squared = {r2:.3f}\nRMSE = {rmse:.3f}',
                transform=plt.gca().transAxes,
                bbox=dict(facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        
        # Save plot
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print("\nModel Performance Metrics:")
        print(f"R-squared Score: {r2:.3f}")
        print(f"RMSE: {rmse:.3f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': ['Bed Nets Usage', 'Antimalarial Treatment'],
            'importance': model.feature_importances_
        })
        print("\nFeature Importance:")
        print(feature_importance.sort_values('importance', ascending=False))
        
        return r2, rmse
        
    except Exception as e:
        print(f"Error in model training and prediction plot: {str(e)}")
        return None, None

def main():
    """
    Main function to run the malaria analysis pipeline.
    """
    # Create output directory if it doesn't exist
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    # File paths
    data_path = 'data/DatasetAfricaMalaria.csv'
    heatmap_path = os.path.join(output_dir, 'prevention_effectiveness_heatmap.png')
    prediction_path = os.path.join(output_dir, 'prediction_accuracy_plot.png')
    
    print("Starting Malaria Prevention Analysis...")
    
    # Load and clean data
    df = load_and_clean_data(data_path)
    if df is None:
        return
    
    print("\nCreating visualizations...")
    
    # Create visualizations
    create_prevention_heatmap(df, heatmap_path)
    r2, rmse = train_model_and_create_prediction_plot(df, prediction_path)
    
    if r2 is not None and rmse is not None:
        print(f"\nAnalysis complete. Results saved in '{output_dir}' directory")

if __name__ == "__main__":
    main()
