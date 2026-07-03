import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for premium plots
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'figure.titlesize': 18
})

def inspect_dataset(df):
    """Prints basic inspection info of the dataset."""
    print("=" * 60)
    print("DATASET INSPECTION")
    print("=" * 60)
    print(f"Dataset Shape: {df.shape}")
    print("\nData Info:")
    print(df.info())
    print("\nMissing Values Count:")
    missing = df.isnull().sum()
    print(missing[missing > 0])
    print("\nBasic Summary Statistics:")
    print(df.describe().T)
    print("=" * 60 + "\n")

def handle_missing_values(df):
    """Handles missing values: drops target nulls, imputes features using country-specific medians."""
    print("=" * 60)
    print("HANDLING MISSING VALUES")
    print("=" * 60)
    
    # 1. Drop rows where target variable (HDI) is missing
    initial_len = len(df)
    df = df.dropna(subset=['HDI']).copy()
    dropped_target = initial_len - len(df)
    print(f"Dropped {dropped_target} rows because the target variable (HDI) was missing.")
    
    # 2. Impute features using country-specific medians (since values evolve chronologically per country)
    features = ['Life_Expectancy', 'Expected_Schooling', 'Mean_Schooling', 'GNI_Per_Capita']
    for col in features:
        # Group by country and fill missing values with country-specific median
        df[col] = df.groupby('Country')[col].transform(lambda x: x.fillna(x.median()))
        
        # If there are any remaining null values (e.g., country has all NaNs, which is not the case here but is good practice)
        remaining_nulls = df[col].isnull().sum()
        if remaining_nulls > 0:
            global_median = df[col].median()
            df[col] = df[col].fillna(global_median)
            print(f"Imputed {remaining_nulls} remaining missing values in '{col}' with global median.")
            
    print("All missing values handled successfully.")
    print(df.isnull().sum())
    print("=" * 60 + "\n")
    return df

def preprocess_features(df):
    """Performs transformations, e.g., log transform on GNI per Capita to handle skewness."""
    print("=" * 60)
    print("DATA PREPROCESSING")
    print("=" * 60)
    
    # Check skewness of GNI
    gni_skew = df['GNI_Per_Capita'].skew()
    print(f"GNI per Capita original skewness: {gni_skew:.3f}")
    
    # Apply natural log transformation to normalize GNI per Capita
    df['Log_GNI'] = np.log(df['GNI_Per_Capita'])
    log_gni_skew = df['Log_GNI'].skew()
    print(f"Log GNI per Capita transformed skewness: {log_gni_skew:.3f}")
    print("Added 'Log_GNI' feature.")
    print("=" * 60 + "\n")
    return df

def perform_feature_selection(df):
    """Analyzes linear correlation between features and HDI to guide feature selection."""
    print("=" * 60)
    print("FEATURE SELECTION ANALYSIS")
    print("=" * 60)
    
    # Correlation with target HDI
    corr_matrix = df.select_dtypes(include=[np.number]).corr()
    hdi_corr = corr_matrix['HDI'].sort_values(ascending=False)
    print("Correlation of numerical features with target variable (HDI):")
    print(hdi_corr)
    
    # Selected features for training later
    selected_features = ['Life_Expectancy', 'Expected_Schooling', 'Mean_Schooling', 'Log_GNI']
    print(f"\nSelected Features for prediction: {selected_features}")
    print("We select 'Log_GNI' instead of 'GNI_Per_Capita' to benefit linear algorithms and reduce leverage of outliers.")
    print("=" * 60 + "\n")
    return selected_features

def generate_eda_plots(df, reports_dir):
    """Generates and saves premium visualizations to the reports directory."""
    print("=" * 60)
    print("GENERATING EXPLORATORY DATA ANALYSIS PLOTS")
    print("=" * 60)
    
    # 1. Correlation Heatmap
    plt.figure(figsize=(10, 8))
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()
    
    sns.heatmap(
        corr, 
        annot=True, 
        cmap='coolwarm', 
        fmt=".3f", 
        linewidths=.5, 
        vmin=-1, 
        vmax=1, 
        cbar_kws={'label': 'Correlation Coefficient'}
    )
    plt.title('Correlation Matrix of HDI Indicators', pad=20)
    plt.tight_layout()
    heatmap_path = os.path.join(reports_dir, 'correlation_heatmap.png')
    plt.savefig(heatmap_path, dpi=300)
    plt.close()
    print(f"Saved correlation heatmap to: {heatmap_path}")
    
    # 2. Scatter Plots
    # Scatter 1: Life Expectancy vs HDI
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x='Life_Expectancy', y='HDI', alpha=0.5, hue='HDI', palette='viridis')
    plt.title('Life Expectancy at Birth vs Human Development Index')
    plt.xlabel('Life Expectancy (Years)')
    plt.ylabel('HDI')
    plt.tight_layout()
    scatter_le_path = os.path.join(reports_dir, 'scatter_life_expectancy.png')
    plt.savefig(scatter_le_path, dpi=300)
    plt.close()
    
    # Scatter 2: GNI per Capita vs HDI (Log scale vs Raw comparison in a subplot)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Raw GNI
    sns.scatterplot(ax=axes[0], data=df, x='GNI_Per_Capita', y='HDI', alpha=0.5, color='teal')
    axes[0].set_title('Raw GNI per Capita vs HDI')
    axes[0].set_xlabel('GNI per Capita (PPP $)')
    axes[0].set_ylabel('HDI')
    
    # Log GNI
    sns.scatterplot(ax=axes[1], data=df, x='Log_GNI', y='HDI', alpha=0.5, color='coral')
    axes[1].set_title('Log-Transformed GNI per Capita vs HDI')
    axes[1].set_xlabel('Log GNI per Capita')
    axes[1].set_ylabel('HDI')
    
    plt.suptitle('GNI per Capita Relationship with HDI', y=1.02)
    plt.tight_layout()
    scatter_gni_path = os.path.join(reports_dir, 'scatter_gni_comparison.png')
    plt.savefig(scatter_gni_path, dpi=300)
    plt.close()
    
    # Scatter 3: Schooling indicators vs HDI
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    sns.scatterplot(ax=axes[0], data=df, x='Expected_Schooling', y='HDI', alpha=0.5, color='mediumpurple')
    axes[0].set_title('Expected Years of Schooling vs HDI')
    axes[0].set_xlabel('Expected Schooling (Years)')
    axes[0].set_ylabel('HDI')
    
    sns.scatterplot(ax=axes[1], data=df, x='Mean_Schooling', y='HDI', alpha=0.5, color='darkorange')
    axes[1].set_title('Mean Years of Schooling vs HDI')
    axes[1].set_xlabel('Mean Schooling (Years)')
    axes[1].set_ylabel('HDI')
    
    plt.suptitle('Education Indicators Relationship with HDI', y=1.02)
    plt.tight_layout()
    scatter_edu_path = os.path.join(reports_dir, 'scatter_education_comparison.png')
    plt.savefig(scatter_edu_path, dpi=300)
    plt.close()
    print(f"Saved scatter plots comparison graphs to: {reports_dir}")
    
    # 3. Distribution Plots
    # HDI target distribution
    plt.figure(figsize=(8, 6))
    sns.histplot(df['HDI'], kde=True, color='blue', bins=30)
    plt.title('Distribution of Human Development Index (HDI)')
    plt.xlabel('HDI Score')
    plt.ylabel('Count')
    plt.tight_layout()
    dist_hdi_path = os.path.join(reports_dir, 'distribution_hdi.png')
    plt.savefig(dist_hdi_path, dpi=300)
    plt.close()
    
    # GNI transformation distribution comparison
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    sns.histplot(data=df, x='GNI_Per_Capita', ax=axes[0], kde=True, color='teal', bins=30)
    axes[0].set_title('Skewed Distribution of Raw GNI')
    axes[0].set_xlabel('GNI per Capita (PPP $)')
    
    sns.histplot(data=df, x='Log_GNI', ax=axes[1], kde=True, color='coral', bins=30)
    axes[1].set_title('Normalized Distribution of Log-GNI')
    axes[1].set_xlabel('Log GNI per Capita')
    
    plt.suptitle('Effect of Log-Transformation on GNI Distribution', y=1.02)
    plt.tight_layout()
    dist_gni_path = os.path.join(reports_dir, 'distribution_gni_transformation.png')
    plt.savefig(dist_gni_path, dpi=300)
    plt.close()
    print(f"Saved feature distribution graphs to: {reports_dir}")
    print("=" * 60 + "\n")

def main():
    raw_data_path = "data/raw/hdi_dataset.csv"
    processed_data_path = "data/processed/hdi_processed.csv"
    reports_dir = "reports"
    
    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)
    
    # 1. Load the dataset
    print(f"Loading dataset from: {raw_data_path}")
    df = pd.read_csv(raw_data_path)
    
    # 2. Inspect the dataset
    inspect_dataset(df)
    
    # 3. Handle missing values
    df_clean = handle_missing_values(df)
    
    # 4. Preprocess features (e.g. log transform)
    df_preprocessed = preprocess_features(df_clean)
    
    # 5. Feature selection analysis
    selected_features = perform_feature_selection(df_preprocessed)
    
    # 6. Generate exploratory plots
    generate_eda_plots(df_preprocessed, reports_dir)
    
    # 7. Save processed dataset
    df_preprocessed.to_csv(processed_data_path, index=False)
    print(f"Successfully processed dataset. Shape: {df_preprocessed.shape}")
    print(f"Saved processed dataset to: {processed_data_path}")

if __name__ == "__main__":
    main()
