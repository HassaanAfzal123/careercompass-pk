# 🔼 CareerCompass PK

**Pakistan's Salary Intelligence & Career Planning Platform**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://career-pk.streamlit.app/)

## Overview

CareerCompass PK is an intelligent salary estimation and career planning tool designed specifically for Pakistan's job market. Using machine learning and real market data from job postings, it provides salary range estimates, market intelligence, and career growth insights.

### Key Features

- ** Salary Range Estimator**: Get realistic salary ranges based on your profile
- ** Market Intelligence Dashboard**: Analyze Pakistan's job market trends
- ** Career Growth Insights**: Discover high-impact career moves
- ** Location Analysis**: Compare salaries across Pakistani cities
- ** Education Impact**: Understand ROI of different education levels

##  Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python, Scikit-learn
- **ML Models**: Ensemble (Random Forest, Gradient Boosting, Extra Trees)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Deployment**: Streamlit Cloud

##  Architecture

```
CareerCompass PK/
├──  app.py                    # Main Streamlit application
├──  clean.py                 # Data cleaning utilities
├──  confidence_model.py      # ML model training
├──  cleaned_salary_data.csv  # Processed dataset
├──  salary_prediction_confidence_model.pkl  # Trained model
├──  requirements.txt         # Dependencies
└──  README.md               # Documentation
```

##  Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/careercompass-pk.git
   cd careercompass-pk
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** to `http://localhost:8501`



### Model Features
1. **Experience Years** (0-15) - Primary predictor
2. **Functional Area** - Department/industry type
3. **City** - Location with major city premiums
4. **Education Level** - Matriculation to Masters
5. **Career Level** - Auto-determined from experience
6. **Derived Features** - Experience², Education numeric, City flags

### Validation
- **Train/Test Split**: 80/20
- **Cross-Validation**: 5-fold CV
- **Ensemble Approach**: Multiple models for robustness
- **Confidence Intervals**: Uncertainty quantification


### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/careercompass-pk.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Start development server
streamlit run app.py
```

