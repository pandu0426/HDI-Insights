import os
import json
import joblib
import sqlite3
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_file
from utils import db_manager, pdf_generator

app = Flask(__name__)

# Constants for validation bounds
BOUNDS = {
    'Life_Expectancy': {'min': 20.0, 'max': 100.0, 'default': 70.0},
    'Expected_Schooling': {'min': 0.0, 'max': 22.0, 'default': 12.0},
    'Mean_Schooling': {'min': 0.0, 'max': 20.0, 'default': 8.0},
    'GNI_Per_Capita': {'min': 100.0, 'max': 150000.0, 'default': 15000.0}
}

# Global references for ML models
classifier = None
regressor = None
scaler = None
model_stats = None

def load_models():
    global classifier, regressor, scaler, model_stats
    models_dir = "models"
    try:
        classifier = joblib.load(os.path.join(models_dir, "hdi_classifier.joblib"))
        regressor = joblib.load(os.path.join(models_dir, "hdi_regressor.joblib"))
        scaler = joblib.load(os.path.join(models_dir, "scaler.joblib"))
        
        stats_path = os.path.join(models_dir, "model_comparison.json")
        if os.path.exists(stats_path):
            with open(stats_path, 'r') as f:
                model_stats = json.load(f)
        print("Models and statistics loaded successfully.")
    except Exception as e:
        print(f"Error loading models: {e}. Run train_model.py first.")

# Load models at startup
load_models()

def compute_prediction_details(life_exp, exp_school, mean_school, gni):
    """
    Core business logic helper that takes raw features, applies transformation,
    scales, predicts class + confidence + score, and computes explainable AI (XAI)
    and advisory insights.
    """
    if classifier is None or regressor is None or scaler is None:
        raise ValueError("ML Models are not initialized on the server.")
        
    # Preprocess
    log_gni = np.log(gni)
    raw_df = pd.DataFrame(
        [[life_exp, exp_school, mean_school, log_gni]], 
        columns=['Life_Expectancy', 'Expected_Schooling', 'Mean_Schooling', 'Log_GNI']
    )
    
    # Scale
    features_scaled = scaler.transform(raw_df)[0]
    
    # Predict continuous score
    hdi_score = float(regressor.predict([features_scaled])[0])
    hdi_score = float(np.clip(hdi_score, 0.0, 1.0))
    
    # Predict category and confidence
    probs = classifier.predict_proba([features_scaled])[0]
    pred_class_idx = int(np.argmax(probs))
    confidence = float(probs[pred_class_idx] * 100)
    
    class_names = ['Low', 'Medium', 'High', 'Very High']
    predicted_category = class_names[pred_class_idx]
    
    # Explainable AI: Feature Contributions
    # Contribution = Scaled Value * Feature Importance
    feature_keys = ['Life_Expectancy', 'Expected_Schooling', 'Mean_Schooling', 'Log_GNI']
    importances = model_stats.get('feature_importances', {}) if model_stats else {
        'Life_Expectancy': 0.12, 'Expected_Schooling': 0.01, 'Mean_Schooling': 0.01, 'Log_GNI': 0.86
    }
    
    contributions = {}
    for i, key in enumerate(feature_keys):
        contributions[key] = float(features_scaled[i] * importances.get(key, 0.25))
        
    most_influential = max(contributions, key=lambda k: abs(contributions[k]))
    most_influential_clean = most_influential.replace('_', ' ')
    
    # Positive / Weak Indicators
    # Compare raw features to world medians (obtained from train_model.py processed output or standard medians)
    medians = {
        'Life_Expectancy': 72.0,
        'Expected_Schooling': 13.0,
        'Mean_Schooling': 8.5,
        'GNI_Per_Capita': 12000.0
    }
    
    pos_indicators = []
    weak_indicators = []
    
    if life_exp >= medians['Life_Expectancy']:
        pos_indicators.append(f"High Life Expectancy ({life_exp:.1f} years)")
    else:
        weak_indicators.append(f"Lower Life Expectancy ({life_exp:.1f} years)")
        
    if exp_school >= medians['Expected_Schooling']:
        pos_indicators.append(f"Strong Expected Schooling ({exp_school:.1f} years)")
    else:
        weak_indicators.append(f"Limited Schooling Outlook ({exp_school:.1f} years)")
        
    if mean_school >= medians['Mean_Schooling']:
        pos_indicators.append(f"High Mean Schooling ({mean_school:.1f} years)")
    else:
        weak_indicators.append(f"Lower Adult Literacy Average ({mean_school:.1f} years)")
        
    if gni >= medians['GNI_Per_Capita']:
        pos_indicators.append(f"Strong Income per Capita (${gni:,.0f})")
    else:
        weak_indicators.append(f"Low National Income per Capita (${gni:,.0f})")
        
    # Generate Explanation Text
    direction = "positive" if contributions[most_influential] > 0 else "limiting"
    explanation_txt = (
        f"The model predicted a <b>{predicted_category} Human Development Index (HDI)</b> category "
        f"primarily driven by the {direction} effect of <b>{most_influential_clean}</b>. "
    )
    if weak_indicators:
        explanation_txt += f"The principal bottleneck dragging down performance is: {weak_indicators[0]}."
    else:
        explanation_txt += "All indicators exceed global median standards, leading to a high development projection."
        
    # Generate Advisor Recommendations
    recommendations = []
    if life_exp < 75.0:
        recommendations.append("Strengthen public healthcare investment, modernize sanitation systems, and expand prenatal/maternal care facilities.")
    else:
        recommendations.append("Enhance preventative health measures, invest in mental wellness, and subsidize geriatric support infrastructure.")
        
    if exp_school < 13.0:
        recommendations.append("Increase classroom construction, build rural transport paths, and eliminate early schooling tuition costs.")
    if mean_school < 9.0:
        recommendations.append("Launch adult literacy programs, expand digital literacy campaigns, and organize night schools for working adults.")
        
    if gni < 15000.0:
        recommendations.append("Diversify agrarian economies, support small enterprise microloans, and reduce regional income inequality.")
    else:
        recommendations.append("Boost funding for scientific research, incentivize technology startups, and strengthen vocational training partnerships.")
        
    # Restrict to top 3 recommendations
    recommendations = recommendations[:3]
    
    return {
        'prediction': round(hdi_score, 3),
        'category': predicted_category,
        'confidence': round(confidence, 1),
        'most_influential': most_influential_clean,
        'contributions': contributions,
        'pos_indicators': pos_indicators,
        'weak_indicators': weak_indicators,
        'explanation': explanation_txt,
        'recommendations': recommendations
    }

@app.route('/')
def home():
    # Pass parameters for rendering range inputs dynamically
    return render_template('index.html', bounds=BOUNDS)

@app.route('/predict', methods=['POST'])
def predict():
    if classifier is None:
        load_models()
        if classifier is None:
            return jsonify({'success': False, 'error': 'AI models are not loaded. Run train_model.py first.'}), 500
            
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Invalid request JSON payload.'}), 400
            
        errors = {}
        cleaned = {}
        for key, lim in BOUNDS.items():
            val = data.get(key)
            if val is None:
                errors[key] = "This field is required."
                continue
            try:
                val = float(val)
            except ValueError:
                errors[key] = "Value must be a valid number."
                continue
            if val < lim['min'] or val > lim['max']:
                errors[key] = f"Value must be between {lim['min']} and {lim['max']}."
            else:
                cleaned[key] = val
                
        if errors:
            return jsonify({'success': False, 'errors': errors}), 400
            
        country = data.get('Country', 'Custom')
        
        # Calculate
        results = compute_prediction_details(
            cleaned['Life_Expectancy'],
            cleaned['Expected_Schooling'],
            cleaned['Mean_Schooling'],
            cleaned['GNI_Per_Capita']
        )
        
        # Save to database
        db_manager.add_prediction(
            country=country,
            life_expectancy=cleaned['Life_Expectancy'],
            expected_schooling=cleaned['Expected_Schooling'],
            mean_schooling=cleaned['Mean_Schooling'],
            gni_per_capita=cleaned['GNI_Per_Capita'],
            predicted_category=results['category'],
            prediction_confidence=results['confidence'],
            hdi_score=results['prediction']
        )
        
        return jsonify({
            'success': True,
            'prediction': results['prediction'],
            'category': results['category'],
            'confidence': results['confidence'],
            'explanation': results['explanation'],
            'most_influential': results['most_influential'],
            'pos_indicators': results['pos_indicators'],
            'weak_indicators': results['weak_indicators'],
            'recommendations': results['recommendations'],
            'inputs': cleaned
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f"Prediction exception: {str(e)}"}), 500

@app.route('/compare', methods=['POST'])
def compare():
    try:
        data = request.get_json()
        if not data or 'country_a' not in data or 'country_b' not in data:
            return jsonify({'success': False, 'error': 'Comparison data missing.'}), 400
            
        profile_a = data['country_a']
        profile_b = data['country_b']
        
        pred_a = compute_prediction_details(
            float(profile_a['Life_Expectancy']),
            float(profile_a['Expected_Schooling']),
            float(profile_a['Mean_Schooling']),
            float(profile_a['GNI_Per_Capita'])
        )
        
        pred_b = compute_prediction_details(
            float(profile_b['Life_Expectancy']),
            float(profile_b['Expected_Schooling']),
            float(profile_b['Mean_Schooling']),
            float(profile_b['GNI_Per_Capita'])
        )
        
        return jsonify({
            'success': True,
            'country_a': {
                'name': profile_a.get('Name', 'Country A'),
                'inputs': profile_a,
                'prediction': pred_a['prediction'],
                'category': pred_a['category'],
                'confidence': pred_a['confidence']
            },
            'country_b': {
                'name': profile_b.get('Name', 'Country B'),
                'inputs': profile_b,
                'prediction': pred_b['prediction'],
                'category': pred_b['category'],
                'confidence': pred_b['confidence']
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    search = request.args.get('search')
    category = request.args.get('category')
    sort_by = request.args.get('sort_by', 'date_desc')
    
    records = db_manager.get_history(search=search, category=category, sort_by=sort_by)
    return jsonify({'success': True, 'records': records})

@app.route('/history/delete/<int:pred_id>', methods=['POST'])
def delete_history(pred_id):
    try:
        db_manager.delete_prediction(pred_id)
        return jsonify({'success': True, 'message': 'Record deleted successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/history/clear', methods=['POST'])
def clear_history():
    try:
        db_manager.clear_history()
        return jsonify({'success': True, 'message': 'History cleared successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/dataset', methods=['GET'])
def get_dataset():
    """Returns paginated, sorted, and filtered rows from the processed dataset + summary insights."""
    processed_path = "dataset/hdi_processed.csv"
    if not os.path.exists(processed_path):
        return jsonify({'success': False, 'error': 'Dataset has not been preprocessed yet.'}), 500
        
    try:
        df = pd.read_csv(processed_path)
        
        # Calculate summary statistics (Data Insights)
        total_countries = int(df['Country'].nunique())
        avg_life = float(df['Life_Expectancy'].mean())
        avg_hdi = float(df['HDI'].mean())
        median_gni = float(df['GNI_Per_Capita'].median())
        
        max_gni_idx = df['GNI_Per_Capita'].idxmax()
        max_gni_val = float(df.loc[max_gni_idx, 'GNI_Per_Capita'])
        max_gni_country = df.loc[max_gni_idx, 'Country']
        
        min_gni_idx = df['GNI_Per_Capita'].idxmin()
        min_gni_val = float(df.loc[min_gni_idx, 'GNI_Per_Capita'])
        min_gni_country = df.loc[min_gni_idx, 'Country']
        
        max_edu_idx = df['Mean_Schooling'].idxmax()
        max_edu_val = float(df.loc[max_edu_idx, 'Mean_Schooling'])
        max_edu_country = df.loc[max_edu_idx, 'Country']
        
        best_hdi_idx = df['HDI'].idxmax()
        best_hdi_val = float(df.loc[best_hdi_idx, 'HDI'])
        best_hdi_country = df.loc[best_hdi_idx, 'Country']
        
        worst_hdi_idx = df['HDI'].idxmin()
        worst_hdi_val = float(df.loc[worst_hdi_idx, 'HDI'])
        worst_hdi_country = df.loc[worst_hdi_idx, 'Country']
        
        insights = {
            'total_countries': total_countries,
            'average_life_expectancy': round(avg_life, 2),
            'average_hdi': round(avg_hdi, 3),
            'median_gni': round(median_gni, 2),
            'highest_gni': {'val': max_gni_val, 'country': max_gni_country},
            'lowest_gni': {'val': min_gni_val, 'country': min_gni_country},
            'highest_education': {'val': max_edu_val, 'country': max_edu_country},
            'best_indicators': {'val': best_hdi_val, 'country': best_hdi_country},
            'lowest_indicators': {'val': worst_hdi_val, 'country': worst_hdi_country}
        }
        
        # Filtering & Search in Table
        search_query = request.args.get('search', '').strip()
        if search_query:
            df = df[df['Country'].str.contains(search_query, case=False)]
            
        category_filter = request.args.get('category', '').strip()
        if category_filter:
            category_mapping = {'Low': 0, 'Medium': 1, 'High': 2, 'Very High': 3}
            if category_filter in category_mapping:
                df = df[df['HDI_Category'] == category_mapping[category_filter]]
                
        # Pagination
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 15))
        total_rows = len(df)
        total_pages = max(1, int(np.ceil(total_rows / per_page)))
        
        page = max(1, min(page, total_pages))
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        df_sliced = df.iloc[start_idx:end_idx].copy()
        
        # Replace missing/NaNs for JSON compliance
        df_sliced = df_sliced.replace({np.nan: None})
        rows_list = df_sliced.to_dict(orient='records')
        
        return jsonify({
            'success': True,
            'rows': rows_list,
            'pagination': {
                'current_page': page,
                'per_page': per_page,
                'total_pages': total_pages,
                'total_rows': total_rows
            },
            'insights': insights
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download_report', methods=['GET'])
def download_report():
    try:
        life_exp = float(request.args.get('Life_Expectancy', BOUNDS['Life_Expectancy']['default']))
        exp_school = float(request.args.get('Expected_Schooling', BOUNDS['Expected_Schooling']['default']))
        mean_school = float(request.args.get('Mean_Schooling', BOUNDS['Mean_Schooling']['default']))
        gni = float(request.args.get('GNI_Per_Capita', BOUNDS['GNI_Per_Capita']['default']))
        country = request.args.get('Country', 'Custom Socioeconomic Profile')
        
        # Run prediction
        res = compute_prediction_details(life_exp, exp_school, mean_school, gni)
        
        # Prep PDF payload
        pdf_data = {
            'country': country,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S") if 'datetime' not in globals() else '',
            'inputs': {
                'Life_Expectancy': life_exp,
                'Expected_Schooling': exp_school,
                'Mean_Schooling': mean_school,
                'GNI_Per_Capita': gni
            },
            'prediction': res['prediction'],
            'category': res['category'],
            'confidence': res['confidence'],
            'explanation': res['explanation'],
            'recommendations': res['recommendations'],
            'feature_importance': model_stats.get('feature_importances', {}) if model_stats else {}
        }
        
        pdf_bytes = pdf_generator.generate_pdf_report(pdf_data)
        
        # Make filename clean
        clean_country = "".join(x for x in country if x.isalnum() or x in (' ', '_', '-')).strip().replace(' ', '_')
        filename = f"HDI_Insight_Report_{clean_country}.pdf"
        
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return f"Error generating report: {str(e)}", 500

@app.route('/model_stats', methods=['GET'])
def get_model_stats():
    stats_path = os.path.join("models", "model_comparison.json")
    if os.path.exists(stats_path):
        try:
            with open(stats_path, 'r') as f:
                current_stats = json.load(f)
            return jsonify({'success': True, 'stats': current_stats})
        except Exception as e:
            return jsonify({'success': False, 'error': f"Failed to load stats: {str(e)}"}), 500
    return jsonify({'success': False, 'error': 'Stats not available.'}), 500

if __name__ == '__main__':
    # Start flask application
    app.run(debug=True, port=5000)
