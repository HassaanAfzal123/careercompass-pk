# 🔼 CareerCompass PK

**Pakistan's Premier Salary Intelligence & Career Planning Platform**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## 🚀 Overview

CareerCompass PK is an intelligent salary estimation and career planning tool designed specifically for Pakistan's job market. Using machine learning and real market data from 742+ job postings, it provides salary range estimates, market intelligence, and career growth insights.

### ✨ Key Features

- **🎯 Salary Range Estimator**: Get realistic salary ranges based on your profile
- **📊 Market Intelligence Dashboard**: Analyze Pakistan's job market trends
- **💡 Career Growth Insights**: Discover high-impact career moves
- **🏙️ Location Analysis**: Compare salaries across Pakistani cities
- **🎓 Education Impact**: Understand ROI of different education levels

## 🎯 What Makes It Different

### Honest & Transparent
- **Salary Ranges** instead of false precision
- **Clear limitations** displayed upfront
- **Confidence indicators** for predictions
- **Real market data** from Pakistan (2024)

### Objective & Reliable
- **No subjective assessments** (removed skill self-ratings)
- **Verifiable inputs only** (experience, education, location)
- **Data-driven insights** from actual job postings
- **Focus on actionable factors**

## 📊 Model Performance

- **Test Accuracy**: ±36K PKR Mean Absolute Error
- **R² Score**: 0.21 (realistic for salary prediction)
- **Dataset**: 742 job postings from Pakistan
- **Features**: 8 objective, verifiable factors

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python, Scikit-learn
- **ML Models**: Ensemble (Random Forest, Gradient Boosting, Extra Trees)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Deployment**: Streamlit Cloud

## 🏗️ Architecture

```
📁 CareerCompass PK/
├── 🎯 app.py                    # Main Streamlit application
├── 🧹 clean.py                 # Data cleaning utilities
├── 🤖 confidence_model.py      # ML model training
├── 📊 cleaned_salary_data.csv  # Processed dataset
├── 🎯 salary_prediction_confidence_model.pkl  # Trained model
├── 📋 requirements.txt         # Dependencies
└── 📖 README.md               # Documentation
```

## 🚀 Quick Start

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

### Streamlit Cloud Deployment

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy from your forked repository

## 📈 Features Deep Dive

### 🎯 Salary Range Estimator
- **Input**: Experience, Education, City, Functional Area
- **Output**: Salary range with confidence bounds
- **Auto-Career Mapping**: Experience automatically determines career level
- **Market Context**: Compare against Pakistan market average

### 📊 Market Intelligence
- **Experience Trends**: Salary growth by years of experience
- **Education Impact**: ROI analysis of different degrees
- **City Comparison**: Top 6 highest-paying cities
- **Career Progression**: Salary hierarchy across levels

### 💡 Career Growth Simulator
- **Scenario Analysis**: Compare different career paths
- **Growth Recommendations**: High-impact actions
- **Long-term Strategy**: Career planning guidance

## 🎯 Use Cases

### For Job Seekers
- **Salary Negotiation**: Know your market value
- **Career Planning**: Identify high-impact moves
- **Location Decisions**: Compare city premiums
- **Education ROI**: Evaluate degree investments

### For Employers
- **Compensation Benchmarking**: Set competitive salaries
- **Market Intelligence**: Understand talent costs
- **Hiring Strategy**: Budget for different roles

### For Career Counselors
- **Data-Driven Advice**: Evidence-based recommendations
- **Market Trends**: Current job market insights
- **Education Guidance**: ROI of different qualifications

## 📊 Data & Methodology

### Dataset
- **Source**: RozeePK job postings (2024)
- **Size**: 742 cleaned job records
- **Coverage**: Major Pakistani cities and industries
- **Quality**: Extensive cleaning and validation

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

## 🔮 Future Enhancements

### Short Term
- [ ] Industry-specific models
- [ ] Company size factor
- [ ] Benefits analysis
- [ ] Mobile optimization

### Long Term
- [ ] Real-time data updates
- [ ] AI-powered career recommendations
- [ ] Skill gap analysis
- [ ] Salary negotiation simulator

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Data Source**: RozeePK for job market data
- **ML Libraries**: Scikit-learn, Pandas, NumPy
- **Visualization**: Plotly for interactive charts
- **Deployment**: Streamlit for easy web deployment

## 📞 Contact

- **Developer**: [Your Name]
- **Email**: [your.email@example.com]
- **LinkedIn**: [Your LinkedIn Profile]
- **GitHub**: [Your GitHub Profile]

## 🔗 Links

- **Live App**: [CareerCompass PK](https://your-app-url.streamlit.app)
- **GitHub**: [Repository](https://github.com/yourusername/careercompass-pk)
- **Documentation**: [Wiki](https://github.com/yourusername/careercompass-pk/wiki)

---

**Made with ❤️ for Pakistan's job market**

*Empowering career decisions with data-driven insights*
