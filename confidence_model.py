import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import matplotlib.pyplot as plt
from clean import load_and_clean_data, clean_salary, clean_experience, clean_categorical_features, extract_location_features, extract_skills_features, encode_categorical_features

def create_confidence_model():
    """
    Create a model that provides confidence intervals and uncertainty estimates
    """
    print("🎯 CREATING CONFIDENCE-AWARE SALARY MODEL")
    print("=" * 60)
    
    # Load cleaned dataset directly
    print("📊 Loading cleaned dataset...")
    df = pd.read_csv('cleaned_salary_data.csv')
    
    # Create encoders for categorical features
    from sklearn.preprocessing import LabelEncoder
    encoders = {}
    categorical_features = ['Career Level', 'Functional Area', 'city_grouped', 'Minimum Education']
    
    for feature in categorical_features:
        if feature in df.columns:
            le = LabelEncoder()
            df[f'{feature}_encoded'] = le.fit_transform(df[feature].fillna('Unknown'))
            encoders[feature] = le
    
    # Use core objective features only (removed subjective skill assessments)
    features = [
        'experience_years',
        'Career Level_encoded', 'Functional Area_encoded', 'city_grouped_encoded', 
        'Minimum Education_encoded'
    ]
    
    # Add derived features
    tier1_cities = ['Karachi', 'Islamabad', 'Lahore']
    df['is_top_city'] = df['city_grouped'].apply(lambda x: 1 if x in tier1_cities else 0)
    df['experience_squared'] = df['experience_years'] ** 2
    # Removed skills_experience interaction since we removed skills_count
    
    education_mapping = {'Matriculation/O-Level': 1, 'Intermediate/A-Level': 2, 'Diploma': 3, 'Bachelors': 4, 'Masters': 5}
    df['education_numeric'] = df['Minimum Education'].map(education_mapping).fillna(3)
    
    final_features = features + ['is_top_city', 'experience_squared', 'education_numeric']
    
    # Prepare data
    X = df[final_features].dropna()
    y = df.loc[X.index, 'salary_avg']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train ensemble for confidence intervals
    print("🌳 Training ensemble models for confidence estimation...")
    
    models = []
    predictions_train = []
    predictions_test = []
    
    # Train multiple models with different random states
    for i in range(10):
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=8,
            random_state=42 + i  # Different random state for each model
        )
        model.fit(X_train_scaled, y_train)
        models.append(model)
        
        predictions_train.append(model.predict(X_train_scaled))
        predictions_test.append(model.predict(X_test_scaled))
    
    # Calculate ensemble statistics
    train_preds = np.array(predictions_train)
    test_preds = np.array(predictions_test)
    
    # Mean predictions
    train_mean = np.mean(train_preds, axis=0)
    test_mean = np.mean(test_preds, axis=0)
    
    # Standard deviation (uncertainty)
    train_std = np.std(train_preds, axis=0)
    test_std = np.std(test_preds, axis=0)
    
    # Confidence intervals (95%)
    train_lower = train_mean - 1.96 * train_std
    train_upper = train_mean + 1.96 * train_std
    test_lower = test_mean - 1.96 * test_std
    test_upper = test_mean + 1.96 * test_std
    
    # Evaluate performance
    test_mae = mean_absolute_error(y_test, test_mean)
    test_r2 = r2_score(y_test, test_mean)
    
    # Calculate coverage (how often actual values fall within confidence intervals)
    coverage = np.mean((y_test >= test_lower) & (y_test <= test_upper)) * 100
    
    print(f"\n📊 CONFIDENCE MODEL RESULTS:")
    print(f"   Test MAE: PKR {test_mae:,.0f}")
    print(f"   Test R²: {test_r2:.3f}")
    print(f"   95% Confidence Coverage: {coverage:.1f}%")
    print(f"   Average Confidence Width: PKR {np.mean(test_upper - test_lower):,.0f}")
    
    # Analyze uncertainty patterns
    print(f"\n🔍 UNCERTAINTY ANALYSIS:")
    
    # Uncertainty by salary range
    salary_ranges = ['Low (10-50K)', 'Mid (50-100K)', 'High (100K+)']
    for i, range_name in enumerate(salary_ranges):
        if i == 0:
            mask = (y_test >= 10000) & (y_test < 50000)
        elif i == 1:
            mask = (y_test >= 50000) & (y_test < 100000)
        else:
            mask = y_test >= 100000
        
        if np.sum(mask) > 0:
            avg_uncertainty = np.mean(test_std[mask])
            print(f"   {range_name}: ±{avg_uncertainty:,.0f} PKR uncertainty")
    
    # Save the ensemble model
    model_data = {
        'models': models,
        'scaler': scaler,
        'encoders': encoders,
        'feature_names': final_features,
        'test_mae': test_mae,
        'test_r2': test_r2,
        'coverage': coverage
    }
    
    joblib.dump(model_data, 'salary_prediction_confidence_model.pkl')
    print(f"\n💾 Saved confidence model")
    
    return model_data

def predict_with_confidence(job_data, model_data):
    """
    Make predictions with confidence intervals
    """
    models = model_data['models']
    scaler = model_data['scaler']
    encoders = model_data['encoders']
    feature_names = model_data['feature_names']
    
    # Create feature vector (objective features only)
    feature_vector = [
        job_data['experience_years'],
        encoders['Career Level'].transform([job_data['Career Level']])[0],
        encoders['Functional Area'].transform([job_data['Functional Area']])[0],
        encoders['city_grouped'].transform([job_data['city_grouped']])[0],
        encoders['Minimum Education'].transform([job_data['Minimum Education']])[0],
        1 if job_data['city_grouped'] in ['Karachi', 'Islamabad', 'Lahore'] else 0,
        job_data['experience_years'] ** 2,
        4 if job_data['Minimum Education'] == 'Bachelors' else 5
    ]
    
    # Scale features
    X = pd.DataFrame([feature_vector], columns=feature_names)
    X_scaled = scaler.transform(X)
    
    # Get predictions from all models
    predictions = [model.predict(X_scaled)[0] for model in models]
    
    # Calculate statistics
    mean_pred = np.mean(predictions)
    std_pred = np.std(predictions)
    
    # 95% confidence interval
    lower_bound = mean_pred - 1.96 * std_pred
    upper_bound = mean_pred + 1.96 * std_pred
    
    # Confidence level based on uncertainty
    if std_pred < 15000:
        confidence = "High"
    elif std_pred < 25000:
        confidence = "Medium"
    else:
        confidence = "Low"
    
    return {
        'prediction': mean_pred,
        'lower_bound': max(10000, lower_bound),  # Minimum salary floor
        'upper_bound': min(500000, upper_bound),  # Maximum salary cap
        'uncertainty': std_pred,
        'confidence': confidence
    }

def demo_confidence_predictions():
    """
    Demonstrate confidence predictions
    """
    print(f"\n🧪 CONFIDENCE PREDICTION DEMO")
    print("=" * 50)
    
    # Load model
    model_data = joblib.load('salary_prediction_confidence_model.pkl')
    
    # Test cases
    test_cases = [
        {
            'name': 'Fresh Graduate',
            'experience_years': 0, 'skills_count': 3, 'has_technical_skills': 0,
            'Career Level': 'Entry Level', 'Minimum Education': 'Bachelors',
            'city_grouped': 'Lahore', 'Functional Area': 'General'
        },
        {
            'name': 'Mid-Level Tech',
            'experience_years': 4, 'skills_count': 6, 'has_technical_skills': 1,
            'Career Level': 'Experienced Professional', 'Minimum Education': 'Bachelors',
            'city_grouped': 'Karachi', 'Functional Area': 'Software & Web Development'
        },
        {
            'name': 'Senior Professional',
            'experience_years': 8, 'skills_count': 10, 'has_technical_skills': 1,
            'Career Level': 'Experienced Professional', 'Minimum Education': 'Masters',
            'city_grouped': 'Islamabad', 'Functional Area': 'Engineering'
        }
    ]
    
    for case in test_cases:
        result = predict_with_confidence(case, model_data)
        
        print(f"\n📊 {case['name']}:")
        print(f"   Predicted Salary: PKR {result['prediction']:,.0f}")
        print(f"   Confidence Range: PKR {result['lower_bound']:,.0f} - {result['upper_bound']:,.0f}")
        print(f"   Uncertainty: ±{result['uncertainty']:,.0f} PKR")
        print(f"   Confidence Level: {result['confidence']}")

if __name__ == "__main__":
    # Create confidence model
    model_data = create_confidence_model()
    
    # Demo predictions
    demo_confidence_predictions()
