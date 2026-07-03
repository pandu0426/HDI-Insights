import os
import time
import json
import tempfile
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

def clean_and_preprocess(raw_data_path):
    """
    Cleans the dataset by:
    - Handling missing values (country median, then global median)
    - Removing duplicate records
    - Detecting outliers using IQR
    """
    print("--- Data Preprocessing ---")
    df = pd.read_csv(raw_data_path)
    print(f"Original shape: {df.shape}")
    
    # 1. Remove duplicate records
    initial_rows = len(df)
    df = df.drop_duplicates().copy()
    duplicates_removed = initial_rows - len(df)
    if duplicates_removed > 0:
        print(f"Removed {duplicates_removed} duplicate records.")
        
    # 2. Drop rows where target variable (HDI) is missing
    df = df.dropna(subset=['HDI']).copy()
    print(f"Shape after dropping missing targets: {df.shape}")
    
    # 3. Impute missing values in features
    features = ['Life_Expectancy', 'Expected_Schooling', 'Mean_Schooling', 'GNI_Per_Capita']
    for col in features:
        # Group by country and fill missing values with country-specific median
        df[col] = df.groupby('Country')[col].transform(lambda x: x.fillna(x.median()))
        
        # If there are any remaining null values (e.g., country has all NaNs)
        remaining_nulls = df[col].isnull().sum()
        if remaining_nulls > 0:
            global_median = df[col].median()
            df[col] = df[col].fillna(global_median)
            print(f"Imputed {remaining_nulls} remaining missing values in '{col}' with global median.")
            
    # 4. Outlier Detection using IQR method
    print("\n--- Outlier Detection ---")
    outlier_stats = {}
    for col in features:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outlier_stats[col] = {
            'count': int(len(outliers)),
            'lower_bound': float(lower_bound),
            'upper_bound': float(upper_bound)
        }
        print(f"'{col}': found {len(outliers)} outliers outside range [{lower_bound:.2f}, {upper_bound:.2f}]")
        
    # Define target HDI categories
    # Low: < 0.550, Medium: 0.550-0.699, High: 0.700-0.799, Very High: >= 0.800
    def categorize_hdi(val):
        if val >= 0.800:
            return 3  # "Very High"
        elif val >= 0.700:
            return 2  # "High"
        elif val >= 0.550:
            return 1  # "Medium"
        else:
            return 0  # "Low"
            
    df['HDI_Category'] = df['HDI'].apply(categorize_hdi)
    
    # Save the processed dataset
    processed_path = "dataset/hdi_processed.csv"
    df.to_csv(processed_path, index=False)
    print(f"Saved preprocessed data to {processed_path}")
    
    return df, outlier_stats

def train_and_evaluate():
    raw_data_path = "dataset/hdi_dataset.csv"
    df, outlier_stats = clean_and_preprocess(raw_data_path)
    
    # Preprocess features: use log transform on GNI
    df['Log_GNI'] = np.log(df['GNI_Per_Capita'])
    
    features = ['Life_Expectancy', 'Expected_Schooling', 'Mean_Schooling', 'Log_GNI']
    X = df[features]
    y_class = df['HDI_Category']
    y_reg = df['HDI']
    
    # Split the dataset
    X_train, X_test, y_train_class, y_test_class = train_test_split(
        X, y_class, test_size=0.25, random_state=42, stratify=y_class
    )
    _, _, y_train_reg, y_test_reg = train_test_split(
        X, y_reg, test_size=0.25, random_state=42, stratify=y_class
    )
    
    train_size = int(X_train.shape[0])
    test_size = int(X_test.shape[0])
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save Scaler
    models_dir = "models"
    os.makedirs(models_dir, exist_ok=True)
    joblib.dump(scaler, os.path.join(models_dir, "scaler.joblib"))
    print(f"Scaler saved to {os.path.join(models_dir, 'scaler.joblib')}")
    
    # Define models
    classifiers = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Support Vector Machine': SVC(probability=True, random_state=42),
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5)
    }
    
    results = {}
    best_f1 = 0
    best_model_name = ""
    best_classifier_model = None
    
    class_names = ['Low', 'Medium', 'High', 'Very High']
    
    for name, clf in classifiers.items():
        print(f"\nTraining {name}...")
        
        # Measure training speed
        t0 = time.perf_counter()
        clf.fit(X_train_scaled, y_train_class)
        t_train = time.perf_counter() - t0
        
        # Measure prediction speed
        t0 = time.perf_counter()
        preds = clf.predict(X_test_scaled)
        t_pred = time.perf_counter() - t0
        
        # Calculate metrics
        acc = accuracy_score(y_test_class, preds)
        precision, recall, f1, _ = precision_recall_fscore_support(y_test_class, preds, average='weighted')
        cm = confusion_matrix(y_test_class, preds)
        
        # Measure file size using temp file
        with tempfile.NamedTemporaryFile(suffix='.joblib', delete=False) as tmp:
            joblib.dump(clf, tmp.name)
            tmp_name = tmp.name
        file_size_kb = os.path.getsize(tmp_name) / 1024.0
        try:
            os.unlink(tmp_name)
        except Exception:
            pass
            
        results[name] = {
            'accuracy': float(acc),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'confusion_matrix': cm.tolist(),
            'training_time_s': float(t_train),
            'prediction_time_s': float(t_pred),
            'file_size_kb': float(file_size_kb)
        }
        
        print(f" -> Accuracy: {acc:.4f} | F1-Score: {f1:.4f} | Train Time: {t_train:.4f}s | Size: {file_size_kb:.1f} KB")
        
        # Check if this is the best model
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_classifier_model = clf
            
    print(f"\n==========================================")
    print(f"Best Classifier Model: {best_model_name} (F1: {best_f1:.4f})")
    print(f"==========================================")
    
    # Save the best classifier
    classifier_path = os.path.join(models_dir, "hdi_classifier.joblib")
    joblib.dump(best_classifier_model, classifier_path)
    print(f"Best classifier saved to {classifier_path}")
    
    # Train the regressor
    print("\nTraining companion Random Forest Regressor for continuous HDI predictions...")
    regressor = RandomForestRegressor(n_estimators=100, random_state=42)
    regressor.fit(X_train_scaled, y_train_reg)
    
    # Save the regressor
    regressor_path = os.path.join(models_dir, "hdi_regressor.joblib")
    joblib.dump(regressor, regressor_path)
    print(f"Regressor saved to {regressor_path}")
    
    # Extract feature importances
    importances = {}
    if hasattr(best_classifier_model, 'feature_importances_'):
        importances_vals = best_classifier_model.feature_importances_
    else:
        importances_vals = regressor.feature_importances_
        
    for feat, imp in zip(features, importances_vals):
        importances[feat] = float(imp)
        
    # Get best model file size
    best_file_size_kb = results[best_model_name]['file_size_kb']
    
    # Write model statistics and comparison parameters to JSON
    comparison_data = {
        'best_model': best_model_name,
        'features': features,
        'feature_importances': importances,
        'outlier_stats': outlier_stats,
        'models': results,
        'class_names': class_names,
        'dataset_sizes': {
            'train_size': train_size,
            'test_size': test_size,
            'total_size': train_size + test_size
        },
        'best_model_size_kb': best_file_size_kb
    }
    
    stats_path = os.path.join(models_dir, "model_comparison.json")
    with open(stats_path, 'w') as f:
        json.dump(comparison_data, f, indent=4)
    print(f"Comparison metrics written to {stats_path}")

if __name__ == "__main__":
    train_and_evaluate()
