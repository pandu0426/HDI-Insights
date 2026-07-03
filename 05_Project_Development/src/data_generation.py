import os
import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)

def generate_hdi_dataset(num_countries=150, start_year=2003, end_year=2022):
    years = list(range(start_year, end_year + 1))
    num_years = len(years)
    
    # Generate list of country names/placeholders
    country_templates = [
        ("Very High", ["Alandia", "Belgique", "Canada", "Danemark", "Estonia", "Finland", "Germany", "Honshu", "Iceland", "Japan", "Krypton", "Luxembourg", "Netherlands", "Norway", "Oman", "Portugal", "Qatar", "Sweden", "Switzerland", "United Kingdom", "United States", "Singapore", "Australia", "New Zealand", "Ireland", "Austria"]),
        ("High", ["Argentina", "Bulgaria", "Chile", "Croatia", "Greece", "Hungary", "Iran", "Kazakhstan", "Malaysia", "Mexico", "Panama", "Romania", "Seychelles", "Turkey", "Uruguay", "Venezuela", "Costa Rica", "Mauritius", "Georgia", "Albania", "Sri Lanka", "Ukraine", "Brazil", "China"]),
        ("Medium", ["Bolivia", "Egypt", "El Salvador", "Gabon", "India", "Indonesia", "Iraq", "Kyrgyzstan", "Morocco", "Nicaragua", "Palestine", "Philippines", "South Africa", "Tajikistan", "Vietnam", "Honduras", "Guatemala", "Bangladesh", "Nepal", "Pakistan", "Cambodia", "Myanmar"]),
        ("Low", ["Angola", "Benin", "Burundi", "Chad", "Eritrea", "Ethiopia", "Gambia", "Guinea", "Haiti", "Lesotho", "Madagascar", "Malawi", "Mali", "Mozambique", "Niger", "Rwanda", "Senegal", "Sierra Leone", "Sudan", "Togo", "Uganda", "Yemen", "Zambia", "Zimbabwe"])
    ]
    
    data = []
    
    for category, countries in country_templates:
        for country in countries:
            # Base values for this country
            if category == "Very High":
                base_life = np.random.uniform(77, 83)
                base_exp_school = np.random.uniform(14, 17)
                base_mean_school = np.random.uniform(11, 13)
                base_gni = np.random.uniform(32000, 65000)
            elif category == "High":
                base_life = np.random.uniform(71, 77)
                base_exp_school = np.random.uniform(12, 14.5)
                base_mean_school = np.random.uniform(8.5, 11)
                base_gni = np.random.uniform(13000, 28000)
            elif category == "Medium":
                base_life = np.random.uniform(63, 71)
                base_exp_school = np.random.uniform(9.5, 12.5)
                base_mean_school = np.random.uniform(5.5, 8.5)
                base_gni = np.random.uniform(4000, 12000)
            else: # Low
                base_life = np.random.uniform(51, 62)
                base_exp_school = np.random.uniform(6.5, 10.0)
                base_mean_school = np.random.uniform(2.5, 6.0)
                base_gni = np.random.uniform(600000 / 1000, 3500) # GNI between 600 and 3500
                
            # Random annual growth rates
            gni_growth = np.random.uniform(0.015, 0.04) # 1.5% to 4% growth
            life_growth = np.random.uniform(0.1, 0.3)     # 0.1 to 0.3 years per year
            school_growth = np.random.uniform(0.05, 0.15) # school years growth per year
            
            for i, year in enumerate(years):
                # Calculate indicators with positive trends and some year-on-year fluctuation
                fluctuation = np.random.normal(0, 0.05) # small random fluctuation
                
                life_exp = base_life + (i * life_growth) + (fluctuation * 2)
                exp_school = base_exp_school + (i * school_growth) + fluctuation
                mean_school = base_mean_school + (i * (school_growth * 0.8)) + (fluctuation * 0.5)
                gni = base_gni * ((1 + gni_growth) ** i) + (fluctuation * 200)
                
                # Clip values to realistic UNDP bounds
                life_exp = np.clip(life_exp, 20, 85)
                exp_school = np.clip(exp_school, 0, 18)
                mean_school = np.clip(mean_school, 0, 15)
                gni = np.clip(gni, 100, 75000)
                
                # Compute official UNDP HDI formula
                # 1. Health Index
                le_index = (life_exp - 20) / (85 - 20)
                
                # 2. Education Index
                mys_index = mean_school / 15
                eys_index = exp_school / 18
                edu_index = (mys_index + eys_index) / 2
                
                # 3. Income Index
                income_index = (np.log(gni) - np.log(100)) / (np.log(75000) - np.log(100))
                
                # 4. HDI (Geometric Mean)
                # HDI can be slightly perturbed by a tiny noise to make model fitting non-trivial
                hdi = (le_index * edu_index * income_index) ** (1/3)
                hdi = np.clip(hdi, 0.0, 1.0)
                
                data.append({
                    "Country": country,
                    "Year": year,
                    "Life_Expectancy": round(life_exp, 1),
                    "Expected_Schooling": round(exp_school, 1),
                    "Mean_Schooling": round(mean_school, 1),
                    "GNI_Per_Capita": round(gni, 1),
                    "HDI": round(hdi, 3)
                })
                
    df = pd.DataFrame(data)
    
    # Introduce random missing values (NaNs) in ~3% of the cells for features to practice handling them
    mask_life = np.random.rand(*df['Life_Expectancy'].shape) < 0.02
    mask_exp = np.random.rand(*df['Expected_Schooling'].shape) < 0.03
    mask_mean = np.random.rand(*df['Mean_Schooling'].shape) < 0.03
    mask_gni = np.random.rand(*df['GNI_Per_Capita'].shape) < 0.04
    mask_hdi = np.random.rand(*df['HDI'].shape) < 0.01
    
    df.loc[mask_life, 'Life_Expectancy'] = np.nan
    df.loc[mask_exp, 'Expected_Schooling'] = np.nan
    df.loc[mask_mean, 'Mean_Schooling'] = np.nan
    df.loc[mask_gni, 'GNI_Per_Capita'] = np.nan
    df.loc[mask_hdi, 'HDI'] = np.nan
    
    return df

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    df = generate_hdi_dataset()
    df.to_csv("data/raw/hdi_dataset.csv", index=False)
    print(f"Generated raw dataset with shape {df.shape} and saved to 'data/raw/hdi_dataset.csv'")
    print(df.isnull().sum())
