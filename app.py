import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="CareerCompass PK",
    page_icon="🔼",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_confidence_model():
    try:
        # Load confidence model
        model_data = joblib.load('salary_prediction_confidence_model.pkl')
        
        # Load cleaned dataset for market intelligence
        df = pd.read_csv('cleaned_salary_data.csv')
        
        return model_data, df
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

def predict_salary_range(job_data, model_data):

    models = model_data['models']
    scaler = model_data['scaler']
    encoders = model_data['encoders']
    feature_names = model_data['feature_names']
    
    try:
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
        
        X = pd.DataFrame([feature_vector], columns=feature_names)
        X_scaled = scaler.transform(X)
        
        predictions = [model.predict(X_scaled)[0] for model in models]
        
        mean_pred = np.mean(predictions)
        std_pred = np.std(predictions)
        
        lower_bound = max(10000, mean_pred - 1.96 * std_pred)
        upper_bound = min(500000, mean_pred + 1.96 * std_pred)
        
        
        return {
            'prediction': mean_pred,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'uncertainty': std_pred,

        }
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return None

def create_salary_gauge(prediction_result, avg_salary):
    """Create a salary gauge visualization"""
    if not prediction_result:
        return None
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = prediction_result['prediction'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Salary Range Estimate"},
        delta = {'reference': avg_salary, 'valueformat': ',.0f'},
        gauge = {
            'axis': {'range': [None, 300000], 'tickformat': ',.0f'},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50000], 'color': "lightgray"},
                {'range': [50000, 100000], 'color': "gray"},
                {'range': [100000, 200000], 'color': "lightgreen"},
                {'range': [200000, 300000], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': prediction_result['prediction']
            }
        }
    ))
    
    fig.update_layout(height=400, font={'size': 14})
    return fig

def analyze_market_trends(df):
    """Analyze market trends from the dataset"""
    
    # Salary by experience
    exp_salary = df.groupby('experience_years')['salary_avg'].agg(['mean', 'count']).reset_index()
    exp_salary = exp_salary[exp_salary['count'] >= 5]  # Only show experience levels with enough data
    
    # Education level impact analysis
    education_salary = df.groupby('Minimum Education')['salary_avg'].agg(['mean', 'count']).reset_index()
    education_salary = education_salary[education_salary['count'] >= 10].sort_values('mean', ascending=False)
    
    # Salary by city (exclude neighborhoods like Johar Town, DHA) - Top 6 only
    excluded_areas = ['Johar Town', 'DHA']
    city_df = df[~df['city_grouped'].isin(excluded_areas)]
    city_salary = city_df.groupby('city_grouped')['salary_avg'].agg(['mean', 'count']).reset_index()
    city_salary = city_salary[city_salary['count'] >= 10].sort_values('mean', ascending=False).head(6)
    
    # Education impact (Bachelors vs Diploma)
    education_impact = df.groupby('Minimum Education')['salary_avg'].mean()
    education_premium = education_impact.get('Bachelors', 0) - education_impact.get('Diploma', 0) if 'Bachelors' in education_impact.index and 'Diploma' in education_impact.index else 0
    
    # Career level progression (include Department Head even with small count)
    career_salary = df.groupby('Career Level')['salary_avg'].agg(['mean', 'count']).reset_index()
    # Keep all career levels with at least 5 samples, or if it's Department Head
    career_salary = career_salary[
        (career_salary['count'] >= 5) | 
        (career_salary['Career Level'] == 'Department Head')
    ].sort_values('mean')
    
    return {
        'experience_trend': exp_salary,
        'education_comparison': education_salary,
        'city_comparison': city_salary,
        'education_premium': education_premium,
        'career_progression': career_salary
    }

def create_market_intelligence_charts(trends):
    """Create market intelligence visualizations"""
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Salary by Experience', 'Salary by Education Level', 'Top Cities by Salary', 'Career Level Progression'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Experience trend
    fig.add_trace(
        go.Scatter(x=trends['experience_trend']['experience_years'], 
                  y=trends['experience_trend']['mean'],
                  mode='lines+markers',
                  name='Avg Salary',
                  line=dict(color='blue', width=3)),
        row=1, col=1
    )
    
    # Education level comparison
    fig.add_trace(
        go.Bar(x=trends['education_comparison']['Minimum Education'], 
               y=trends['education_comparison']['mean'],
               name='Avg Salary',
               marker_color='lightblue'),
        row=1, col=2
    )
    
    # City comparison
    fig.add_trace(
        go.Bar(x=trends['city_comparison']['mean'], 
               y=trends['city_comparison']['city_grouped'],
               orientation='h',
               name='Avg Salary',
               marker_color='orange'),
        row=2, col=1
    )
    
    # Career progression
    fig.add_trace(
        go.Bar(x=trends['career_progression']['Career Level'], 
               y=trends['career_progression']['mean'],
               name='Avg Salary',
               marker_color='purple'),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(height=600, showlegend=False, title_text="Pakistan Job Market Intelligence")
    fig.update_xaxes(title_text="Years of Experience", row=1, col=1)
    fig.update_xaxes(title_text="Education Level", row=1, col=2)
    fig.update_xaxes(title_text="Average Salary (PKR)", row=2, col=1)
    fig.update_xaxes(title_text="Career Level", row=2, col=2)
    fig.update_yaxes(title_text="Salary (PKR)", row=1, col=1)
    fig.update_yaxes(title_text="Salary (PKR)", row=1, col=2)
    fig.update_yaxes(title_text="City", row=2, col=1)
    fig.update_yaxes(title_text="Salary (PKR)", row=2, col=2)
    
    return fig

def main():
    model_data, df = load_confidence_model()
    
    if model_data is None or df is None:
        st.error("Failed to load model or data. Please check if all files are present.")
        return
    
    # Header with new positioning
    st.title(" CareerCompass PK")
    st.markdown("###  Salary Range Estimator & Market Intelligence Dashboard")
    

    
    st.markdown("---")
    
    # Create tabs for different features
    tab1, tab2, tab3 = st.tabs([" Salary Range Estimator", " Market Intelligence", " Career Insights"])
    
    with tab1:
        st.subheader(" Estimate Your Salary Range")
        
        # Input form
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👤 Professional Profile")
            
            experience_years = st.slider(
                "Years of Experience", 
                min_value=0, 
                max_value=15, 
                value=3,
                help="Total years of professional experience"
            )
            
            
            education = st.selectbox(
                "Education Level",
                ['Matriculation/O-Level', 'Intermediate/A-Level', 'Diploma', 'Bachelors', 'Masters'],
                index=3,
                help="Highest education qualification"
            )
            
        
        with col2:
            st.markdown("####  Job Characteristics")
            
            city = st.selectbox(
                "City",
                ['Lahore', 'Karachi', 'Islamabad', 'Faisalabad', 'Rawalpindi', 'Other'],
                index=0,
                help="Job location"
            )
            
            functional_area = st.selectbox(
                "Functional Area",
                ['General', 'Software & Web Development', 'Engineering', 'Sales & Business Development', 
                 'Marketing', 'Operations', 'Accounts, Finance & Financial Services', 'Human Resources'],
                index=0,
                help="Department or functional area"
            )
            
        
        # Prediction button
        if st.button(" Estimate Salary Range", type="primary", use_container_width=True):
            # Auto-determine career level based on experience
            if experience_years <= 1:
                auto_career_level = "Intern/Student"
            elif experience_years <= 3:
                auto_career_level = "Entry Level"
            elif experience_years <= 8:
                auto_career_level = "Experienced Professional"
            else:
                auto_career_level = "Department Head"
            
            # Prepare job data
            job_data = {
                'experience_years': experience_years,
                'Career Level': auto_career_level,
                'Minimum Education': education,
                'city_grouped': city,
                'Functional Area': functional_area
            }
            
            # Make prediction
            result = predict_salary_range(job_data, model_data)
            
            if result:
                st.success(" Salary Range Estimated!")
                
                # Main results display
                col3, col4, col5 = st.columns([1, 2, 1])
                
                with col4:
                    st.metric(
                        label=" Estimated Salary Range",
                        value=f"PKR {result['lower_bound']:,.0f} - {result['upper_bound']:,.0f}",
                    )
                
                # Detailed breakdown - centered
                col_left, col6, col_right = st.columns([1, 2, 1])
                
                with col6:
                    st.info(f"""
                     Range Details:
                    • **Lower Bound**: PKR {result['lower_bound']:,.0f}
                    • **Expected**: PKR {result['prediction']:,.0f}
                    • **Upper Bound**: PKR {result['upper_bound']:,.0f}
                    • **Range Width**: PKR {result['upper_bound'] - result['lower_bound']:,.0f}
                    """)
                

                
                # Salary gauge
                avg_salary = df['salary_avg'].mean()
                gauge_fig = create_salary_gauge(result, avg_salary)
                if gauge_fig:
                    st.plotly_chart(gauge_fig, use_container_width=True)
    
    with tab2:
        st.subheader(" Pakistan Job Market Intelligence")
        
        # Analyze market trends
        trends = analyze_market_trends(df)
        
        # Key market insights
        col8, col9, col10, col11 = st.columns(4)
        
        with col8:
            avg_salary = df['salary_avg'].mean()
            st.metric("Average Salary", f"PKR {avg_salary:,.0f}", "Market Average")
        
        with col9:
            education_premium = trends['education_premium']
            st.metric("Bachelors Degree Premium", f"PKR {education_premium:,.0f}", "vs Diploma")
        
        with col10:
            top_city = trends['city_comparison'].iloc[0]
            st.metric("Highest Paying City", top_city['city_grouped'], f"PKR {top_city['mean']:,.0f}")
        
        with col11:
            exp_correlation = df['experience_years'].corr(df['salary_avg'])
            st.metric("Experience Impact", f"{exp_correlation:.2f}", "Correlation")
        
        # Market intelligence charts
        market_fig = create_market_intelligence_charts(trends)
        st.plotly_chart(market_fig, use_container_width=True)
        
        # Detailed insights
        st.markdown("####  Key Market Insights")
        
        col12, col13 = st.columns(2)
        
        with col12:
            st.markdown("""
             Experience Matters Most:
            • Strong correlation (0.47) between experience and salary
            • Each year of experience adds significant value
            • 5+ years experience typically doubles earning potential
            
             Location Premium:
            • Karachi offers highest average salaries
            • Major cities (Karachi, Islamabad, Lahore) pay 15-25% more
            • Remote work opportunities can bridge location gaps
            """)
        
        with col13:
            st.markdown(f"""
             Education Impact:
            • Bachelors degree adds PKR {education_premium:,.0f} premium over Diploma
            • Higher education correlates with better opportunities
            • Functional area matters more than degree level
            
             Career Progression:
            • Clear salary hierarchy across career levels
            • Department heads earn 3-4x more than entry level
            • Experience is the strongest predictor of salary growth
            """)
    
    with tab3:
        st.subheader(" Career Growth Insights")
        
        # Career growth simulator
        st.markdown("####  Salary Growth Simulator")
        
        # Base profile for comparison
        base_profile = {
            'experience_years': 2,
            'Career Level': 'Entry Level',  # 2 years = Entry Level
            'Minimum Education': 'Bachelors',
            'city_grouped': 'Lahore',
            'Functional Area': 'General'
        }
        
        base_result = predict_salary_range(base_profile, model_data)
        
        if base_result:
            st.info(f"**Base Profile**: 2 years experience, Bachelors, General area, Lahore → PKR {base_result['prediction']:,.0f}")
            
            # Growth scenarios
            scenarios = [
                ("Add 3 years experience", {**base_profile, 'experience_years': 5, 'Career Level': 'Experienced Professional'}),  # 5 years = Experienced
                ("Switch to Software Development", {**base_profile, 'Functional Area': 'Software & Web Development'}),
                ("Get Masters degree", {**base_profile, 'Minimum Education': 'Masters'}),
                ("Move to Karachi", {**base_profile, 'city_grouped': 'Karachi'}),
                ("Senior profile (5yr + Masters + Karachi)", {**base_profile, 'experience_years': 5, 'Minimum Education': 'Masters', 'city_grouped': 'Karachi', 'Career Level': 'Experienced Professional'})  # 5 years = Experienced
            ]
            
            growth_data = []
            for scenario_name, scenario_profile in scenarios:
                scenario_result = predict_salary_range(scenario_profile, model_data)
                if scenario_result:
                    increase = scenario_result['prediction'] - base_result['prediction']
                    increase_pct = (increase / base_result['prediction']) * 100
                    growth_data.append({
                        'Scenario': scenario_name,
                        'Salary': f"PKR {scenario_result['prediction']:,.0f}",
                        'Increase': f"PKR {increase:,.0f}",
                        'Growth': f"+{increase_pct:.1f}%"
                    })
            
            # Display growth scenarios
            growth_df = pd.DataFrame(growth_data)
            st.dataframe(growth_df, use_container_width=True)
            
            # Recommendations
            st.markdown("####  Career Growth Recommendations")
            
            col14, col15 = st.columns(2)
            
            with col14:
                st.success("""
                  High Impact Actions:
                  1. **Gain Experience**: Most reliable salary growth
                  2. **Choose Right Functional Area**: Software Development pays most
                  3. **Target Major Cities**: 15-25% salary boost
                  4. **Pursue Higher Education**: Masters degree advantage
                """)
            
            with col15:
                st.info("""
                 Long-term Strategy:
                1. **Build Expertise**: Specialize in high-demand areas
                2. **Develop Leadership**: Management skills for senior roles
                3. **Network Actively**: Connections open opportunities
                4. **Stay Updated**: Technology and market trends
                """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p> Powered by Machine Learning |  Based on Pakistan Job Market Data (2024)</p>
        <p><small>This tool provides estimates based on historical data. Actual salaries may vary based on company, negotiation, and market conditions.</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()