import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

def load_and_preprocess_data(file_path):
    """Load and preprocess training data"""
    df = pd.read_csv(file_path)
    
    # Handle missing values
    df = df.fillna(df.mean())
    
    # Separate features and target
    X = df.drop(['target'], axis=1)
    y = df['target']
    
    return X, y

def train_growth_model(X, y):
    """Train vegetation growth prediction model"""
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Growth Model Performance:")
    print(f"MSE: {mse:.4f}")
    print(f"R2 Score: {r2:.4f}")
    
    return model, scaler

def train_water_model(X, y):
    """Train water usage optimization model"""
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Water Model Performance:")
    print(f"MSE: {mse:.4f}")
    print(f"R2 Score: {r2:.4f}")
    
    return model, scaler

def save_models(models, scalers, output_dir):
    """Save trained models and scalers"""
    os.makedirs(output_dir, exist_ok=True)
    
    joblib.dump(models['growth'], os.path.join(output_dir, 'growth_model.joblib'))
    joblib.dump(models['water'], os.path.join(output_dir, 'water_model.joblib'))
    joblib.dump(scalers['growth'], os.path.join(output_dir, 'growth_scaler.joblib'))
    joblib.dump(scalers['water'], os.path.join(output_dir, 'water_scaler.joblib'))

def main():
    # Load data
    growth_data_path = 'ai/data/growth_data.csv'
    water_data_path = 'ai/data/water_data.csv'
    
    X_growth, y_growth = load_and_preprocess_data(growth_data_path)
    X_water, y_water = load_and_preprocess_data(water_data_path)
    
    # Train models
    growth_model, growth_scaler = train_growth_model(X_growth, y_growth)
    water_model, water_scaler = train_water_model(X_water, y_water)
    
    # Save models
    models = {
        'growth': growth_model,
        'water': water_model
    }
    
    scalers = {
        'growth': growth_scaler,
        'water': water_scaler
    }
    
    save_models(models, scalers, 'ai/models')

if __name__ == "__main__":
    main() 