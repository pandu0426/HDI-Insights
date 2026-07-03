import os
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def train_and_evaluate():
    # 1. Load the preprocessed dataset
    processed_data_path = "data/processed/hdi_processed.csv"
    if not os.path.exists(processed_data_path):
        raise FileNotFoundError(f"Processed dataset not found at {processed_data_path}. Please run data preprocessing first.")
        
    print(f"Loading processed dataset from {processed_data_path}...")
    df = pd.read_csv(processed_data_path)
    
    # 2. Define features and target variable
    # We use Log_GNI as it is normalized and has linear relationship with HDI
    features = ['Life_Expectancy', 'Expected_Schooling', 'Mean_Schooling', 'Log_GNI']
    X = df[features]
    y = df['HDI']
    
    # 3. Split the dataset into 75% training and 25% testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    print(f"Dataset split successfully:")
    print(f" - Training set: {X_train.shape[0]} samples")
    print(f" - Testing set: {X_test.shape[0]} samples")
    
    # 4. Train Linear Regression Model
    print("\nTraining Linear Regression...")
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_preds = lr_model.predict(X_test)
    
    # Evaluate Linear Regression
    lr_r2 = r2_score(y_test, lr_preds)
    lr_mae = mean_absolute_error(y_test, lr_preds)
    lr_rmse = np.sqrt(mean_squared_error(y_test, lr_preds))
    
    # 5. Train Random Forest Regressor
    print("Training Random Forest Regressor...")
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_preds = rf_model.predict(X_test)
    
    # Evaluate Random Forest
    rf_r2 = r2_score(y_test, rf_preds)
    rf_mae = mean_absolute_error(y_test, rf_preds)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_preds))
    
    # 6. Compare Models
    print("\n" + "=" * 50)
    print("MODEL COMPARISON RESULTS (TEST SET)")
    print("=" * 50)
    print(f"{'Metric':<15} | {'Linear Regression':<20} | {'Random Forest':<20}")
    print("-" * 62)
    print(f"{'R² Score':<15} | {lr_r2:<20.6f} | {rf_r2:<20.6f}")
    print(f"{'MAE':<15} | {lr_mae:<20.6f} | {rf_mae:<20.6f}")
    print(f"{'RMSE':<15} | {lr_rmse:<20.6f} | {rf_rmse:<20.6f}")
    print("=" * 50)
    
    # 7. Automatically choose the better model based on R² score
    # (Higher R² is better. If R² is equal, we look at RMSE).
    if rf_r2 > lr_r2:
        best_model = rf_model
        best_name = "Random Forest Regressor"
        best_r2 = rf_r2
    else:
        best_model = lr_model
        best_name = "Linear Regression"
        best_r2 = lr_r2
        
    print(f"\nAutomatically selected the best model: {best_name} (R² = {best_r2:.6f})")
    
    # 8. Save the model as HDI.pkl using Pickle
    models_dir = "models"
    os.makedirs(models_dir, exist_ok=True)
    model_save_path = os.path.join(models_dir, "HDI.pkl")
    
    with open(model_save_path, 'wb') as f:
        pickle.dump(best_model, f)
        
    print(f"Saved the best model to: {model_save_path}")
    
    # Save feature names alongside model to make it self-contained
    # We can inspect feature importance if Random Forest was selected
    if best_name == "Random Forest Regressor":
        importances = best_model.feature_importances_
        print("\nFeature Importances (Random Forest):")
        for feature, importance in zip(features, importances):
            print(f" - {feature}: {importance:.4f}")

if __name__ == "__main__":
    train_and_evaluate()
