# XplainLab

**Transparent ML decisions for Loan Eligibility & Student Eligibility**

XplainLab is an interactive Streamlit application that provides explainable AI predictions for loan eligibility and student eligibility using multiple machine learning algorithms. The application emphasizes transparency by showing not just the predictions, but also the reasoning behind them.

## 🎯 Features

- **User Authentication**: Secure login system to manage user sessions
- **Multiple ML Algorithms**: Choose from Decision Tree, K-Nearest Neighbors (KNN), or Logistic Regression
- **Two Prediction Domains**:
  - Loan Eligibility: Predict if a loan applicant is eligible
  - Student Eligibility: Predict if a student meets eligibility criteria
- **Explanation Modes**:
  - Beginner Mode: Simplified explanations
  - Expert Mode: Detailed technical explanations
- **Explainability Features**: Understand why predictions are made with visual explanations and decision rules
- **Data Visualization**: Graphs and charts to visualize model behavior and predictions

## 📋 Project Structure

```
XplainLab/
├── app.py                          # Main Streamlit application entry point
├── requirement.txt                 # Python dependencies
├── README.md                       # This file
│
├── lib/                            # Library modules
│   ├── __init__.py
│   ├── auth.py                     # Authentication and session management
│   ├── data.py                     # Data loading and preprocessing
│   ├── models.py                   # ML model training and prediction
│   ├── ui.py                       # UI components and styling
│   └── __pycache__/
│
└── pages/                          # Streamlit multi-page app pages
    ├── 1_Login.py                  # User login page
    ├── 2_Choose_Dataset_Algorithm.py  # Dataset and algorithm selection
    ├── 3_Loan_Applicant.py         # Loan eligibility prediction form
    ├── 4_Student_Eligibility.py    # Student eligibility prediction form
    └── 5_About.py                  # About page
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd XplainLab
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```

## 📦 Dependencies

The project requires the following Python packages:

- **streamlit** (>=1.30) - Web application framework
- **pandas** (>=2.0) - Data manipulation and analysis
- **numpy** (>=1.24) - Numerical computing
- **scikit-learn** (>=1.3) - Machine learning library
- **matplotlib** (>=3.7) - Data visualization
- **seaborn** (>=0.13) - Statistical data visualization

See `requirement.txt` for exact versions.

## 🏃 Running the Application

Start the Streamlit application with:

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Using a Specific Port

```bash
streamlit run app.py --server.port 8080
```

## 📖 Usage Guide

### 1. **Login** (`1_Login.py`)
   - Enter your full name, email, and contact number
   - Select your role: "Loan Applicant" or "Student"
   - Accept Terms & Conditions
   - Click "Login" to proceed

### 2. **Choose Dataset & Algorithm** (`2_Choose_Dataset_Algorithm.py`)
   - Select a dataset:
     - **Loan Eligibility**: Predict loan approval
     - **Student Eligibility**: Predict student eligibility
   - Choose an ML algorithm:
     - Decision Tree
     - K-Nearest Neighbors (KNN)
     - Logistic Regression
   - Select explanation mode:
     - Beginner: Simple explanations
     - Expert: Technical details
   - Click "Submit" to proceed

### 3. **Enter Application Details**
   - **Loan Applicant** (`3_Loan_Applicant.py`): Fill in loan application details
   - **Student Eligibility** (`4_Student_Eligibility.py`): Fill in student information

### 4. **View Results**
   - Get prediction result (Eligible/Not Eligible)
   - See explanation of why the prediction was made
   - View visualizations and decision rules
   - Understand model decision factors

## 🔐 Authentication

The application uses Streamlit's session state for authentication:
- User login credentials are stored in session state
- Session persists during the browsing session
- All pages after login verify authentication status

## 🤖 Machine Learning Models

### Supported Algorithms

1. **Decision Tree**
   - Interpretable tree-based model
   - Shows decision rules clearly
   - Easy to understand for beginners

2. **K-Nearest Neighbors (KNN)**
   - Instance-based learning algorithm
   - Finds similar cases in training data
   - Good for explaining based on similar examples

3. **Logistic Regression**
   - Probabilistic classification model
   - Provides probability scores
   - Suitable for risk assessment

### Data Processing Pipeline

- **Numeric Features**: Imputed with median values and scaled to standard normal distribution
- **Categorical Features**: Imputed with most frequent values and one-hot encoded
- **Train-Test Split**: 80-20 split for model evaluation

## 🎨 UI/UX Features

- Clean, modern dark-themed interface
- Sidebar navigation for easy page switching
- User information card in sidebar
- Form validation and error messages
- Success/info notification messages
- Responsive design

## 📝 Pages Overview

| Page | Purpose | File |
|------|---------|------|
| Login | User authentication | `1_Login.py` |
| Choose Dataset & Algorithm | Model configuration | `2_Choose_Dataset_Algorithm.py` |
| Loan Applicant | Loan eligibility form | `3_Loan_Applicant.py` |
| Student Eligibility | Student eligibility form | `4_Student_Eligibility.py` |
| About | Project information | `5_About.py` |

## 🔄 Navigation Flow

```
app.py (Home)
  ↓
1_Login.py (User logs in)
  ↓
2_Choose_Dataset_Algorithm.py (Select dataset & algorithm)
  ↓
3_Loan_Applicant.py OR 4_Student_Eligibility.py (Make prediction)
  ↓
View Results & Explanations
```

## 🐛 Troubleshooting

### Port Already in Use
If port 8501 is already in use, specify a different port:
```bash
streamlit run app.py --server.port 8502
```

### Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirement.txt
```

### Session State Issues
Clear Streamlit cache if experiencing session state problems:
- Click the ⚙️ settings icon in Streamlit
- Select "Clear cache"

## 📧 Support & Feedback

For issues, questions, or feedback, please reach out to the development team.

## 📄 License

This project is an educational tool for demonstrating explainable AI concepts.

**Important**: This is a demo educational system. Do not enter real sensitive financial data.

## 👨‍💻 Development

### Project Modules

- **auth.py**: Handles authentication, session management, and page navigation
- **data.py**: Loads and manages loan/student datasets
- **models.py**: Implements ML model training, prediction, and SHAP-based explanations
- **ui.py**: Provides reusable UI components and styling functions

### Adding New Features

To extend the application:
1. Add new page in `pages/` directory
2. Follow naming convention: `X_PageName.py`
3. Import necessary components from `lib/`
4. Add sidebar navigation link if needed

## 🎓 Educational Value

This application serves as a learning resource for:
- Machine Learning fundamentals
- Model explainability and interpretability
- Streamlit web application development
- User authentication in web apps
- Data preprocessing and feature engineering

---

**Made with ❤️ using Streamlit**
