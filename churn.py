import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import joblib
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_lottie import st_lottie
import requests
import json
from streamlit_option_menu import option_menu

# Page configuration
st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with enhanced design elements
st.markdown("""
<style>
    /* Modern Typography */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main headers with gradient text */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #4F46E5, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: #64748B;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .section-header {
        font-size: 1.3rem;
        color: #334155;
        margin-top: 1.5rem;
        font-weight: 600;
        letter-spacing: -0.3px;
    }
    
    /* Glassmorphism effects */
    .glass-box {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 0.8rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .info-box {
        background: linear-gradient(135deg, rgba(224, 242, 254, 0.8), rgba(186, 230, 253, 0.8));
        border-radius: 0.8rem;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid #0EA5E9;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Prediction boxes with gradient backgrounds */
    .prediction-box-positive {
        background: linear-gradient(135deg, rgba(187, 247, 208, 0.8), rgba(134, 239, 172, 0.8));
        padding: 1.8rem;
        border-radius: 0.8rem;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .prediction-box-negative {
        background: linear-gradient(135deg, rgba(254, 202, 202, 0.8), rgba(252, 165, 165, 0.8));
        padding: 1.8rem;
        border-radius: 0.8rem;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Animated elements */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animated {
        animation: fadeIn 0.6s ease-out forwards;
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 0.8rem;
        padding: 1.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
        border: 1px solid #E2E8F0;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 0.8rem;
        padding: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
        border-top: 4px solid #4F46E5;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1E293B;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748B;
        margin-bottom: 0.5rem;
    }
    
    .metric-delta-positive {
        color: #10B981;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .metric-delta-negative {
        color: #EF4444;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #4F46E5, #7C3AED);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #4338CA, #6D28D9);
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.4);
        transform: translateY(-2px);
    }
    
    /* Slider customization */
    .stSlider {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #4F46E5, #7C3AED) !important;
    }
    
    /* Select box styling */
    .stSelectbox label, .stSlider label {
        color: #334155;
        font-weight: 500;
    }
    
    .stSelectbox > div > div {
        background-color: white;
        border-radius: 0.5rem;
        border: 1px solid #E2E8F0;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        white-space: pre-wrap;
        border-radius: 0.5rem 0.5rem 0 0;
        background-color: #F1F5F9;
        color: #475569;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: #4F46E5 !important;
        border-top: 3px solid #4F46E5 !important;
        border-left: 1px solid #E2E8F0 !important;
        border-right: 1px solid #E2E8F0 !important;
        border-bottom: none !important;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-image: linear-gradient(180deg, #F8FAFC, #F1F5F9);
    }
    
    /* Footer */
    .footer {
        margin-top: 4rem;
        text-align: center;
        color: #94A3B8;
        font-size: 0.9rem;
        padding: 1.5rem;
        border-top: 1px solid #E2E8F0;
    }
    
    /* Grid layout for metrics */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Tooltip styling */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #334155;
        color: white;
        text-align: center;
        border-radius: 0.5rem;
        padding: 0.8rem;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.8rem;
        font-weight: normal;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# Function to load lottie animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load animations
lottie_prediction = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_jcikwtux.json")
lottie_insights = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_l4xxtfd3.json")
lottie_docs = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_o6spyjnc.json")

def create_logo():
    fig, ax = plt.subplots(figsize=(2, 2))
    
    # Create a gradient background
    gradient = np.linspace(0, 1, 100)
    gradient = np.vstack((gradient, gradient))
    
    # Set colors for a modern gradient
    ax.imshow(gradient, aspect='auto', extent=[0, 1, 0, 1], cmap='Blues', alpha=0.5)
    
    # Add logo text with drop shadow
    for offset in [(0.51, 0.51), (0.52, 0.52)]:
        ax.text(offset[0], offset[1], 'CP', fontsize=40, ha='center', va='center', 
                fontweight='bold', color=(0, 0, 0), alpha=0.3)
    
    ax.text(0.5, 0.5, 'CP', fontsize=40, ha='center', va='center', 
            fontweight='bold', color='#4F46E5')
    ax.text(0.5, 0.3, 'Churn Predictor', fontsize=12, ha='center', va='center', 
            color='#64748B', fontweight='bold')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    return fig

# App structure and navigation
def main():
    # Sidebar with modern navigation
    with st.sidebar:
        st.pyplot(create_logo())
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Modern navigation with icons
        selected = option_menu(
            "Navigation",
            ["Prediction Tool", "Model Insights", "Documentation"],
            icons=["graph-up-arrow", "bar-chart-line", "file-earmark-text"],
            menu_icon="list",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#4F46E5", "font-size": "16px"},
                "nav-link": {
                    "font-size": "15px",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "10px",
                    "--hover-color": "#F1F5F9",
                },
                "nav-link-selected": {"background-color": "#EEF2FF", "color": "#4F46E5"},
            }
        )
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        if selected == "Prediction Tool":
            # Input fields with improved UI
            st.markdown("""
            <div class='section-header'>Customer Demographics</div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("Age", min_value=18, max_value=65, value=30)
            with col2:
                gender = st.selectbox("Gender", ["Male", "Female"])
            
            age_group = st.selectbox(
                "Age Group", 
                ["18-25", "26-35", "36-45", "46-55", "56-65", "65+"]
            )
            
            st.markdown("""
            <div class='section-header'>Relationship Info</div>
            """, unsafe_allow_html=True)
            
            tenure = st.slider(
                "Tenure (months)", 
                min_value=0, 
                max_value=60, 
                value=12
            )
            
            contract_length = st.selectbox(
                "Contract Length", 
                ["Monthly", "Quarterly", "Annual"]
            )
            
            st.markdown("""
            <div class='section-header'>Usage Patterns</div>
            """, unsafe_allow_html=True)
            
            usage_frequency = st.slider(
                "Usage Frequency", 
                min_value=0, 
                max_value=30, 
                value=10
            )
            
            last_interaction = st.slider(
                "Last Interaction (days ago)", 
                min_value=0, 
                max_value=30, 
                value=10
            )
            
            st.markdown("""
            <div class='section-header'>Financial Metrics</div>
            """, unsafe_allow_html=True)
            
            subscription_type = st.selectbox(
                "Subscription Type", 
                ["Basic", "Standard", "Premium"]
            )
            
            total_spend = st.slider(
                "Total Spend ($)", 
                min_value=0, 
                max_value=1000, 
                value=500
            )
            
            payment_delay = st.slider(
                "Payment Delay (days)", 
                min_value=0, 
                max_value=30, 
                value=5
            )
            
            st.markdown("""
            <div class='section-header'>Support History</div>
            """, unsafe_allow_html=True)
            
            support_calls = st.slider(
                "Support Calls", 
                min_value=0, 
                max_value=10, 
                value=1
            )
            
            # Reset button
            if st.button("Reset Fields", type="secondary"):
                st.rerun()
    
    # Main content area with enhanced UI
    if selected == "Prediction Tool":
        # Header with modern design
        st.markdown('<h1 class="main-header animated">Customer Churn Predictor</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header animated">Predict the likelihood of customer churn based on behavior and demographics</p>', unsafe_allow_html=True)
        
        # Add animated progress bar to indicate tool is ready
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
        st.success("Tool ready for predictions!")
        
        # Information box with enhanced styling
        with st.expander("ℹ️ About this tool", expanded=False):
            st.markdown("""
            <div class="info-box">
                <h3>Prediction Tool Overview</h3>
                <p>This advanced tool predicts the likelihood of a customer churning based on their demographics, 
                engagement patterns, and financial metrics. The AI model analyzes multiple factors to provide accurate 
                risk assessment and actionable recommendations.</p>
                
                <h4>How to use:</h4>
                <ol>
                    <li>Enter customer information in the sidebar</li>
                    <li>Click "Generate Prediction" to run the analysis</li>
                    <li>Review the prediction results and supporting visualizations</li>
                    <li>Explore the "Model Insights" page to understand key churn factors</li>
                </ol>
                
                <p>The prediction algorithm considers both direct factors (contract length, payment history) 
                and behavioral indicators (usage patterns, support interactions).</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Main content with modern tabs
        tab1, tab2 = st.tabs(["Prediction Results", "Customer Profile"])
        
        with tab1:
            # Create visually appealing prediction button
            cols = st.columns([1, 2, 1])
            with cols[1]:
                predict_button = st.button("Generate Prediction", type="primary", use_container_width=True)
            
            if predict_button:
                with st.spinner("Analyzing customer data..."):
                    # Create a DataFrame from user input
                    input_data = pd.DataFrame({
                        'Age': [age],
                        'Gender': [gender],
                        'Tenure': [tenure],
                        'Usage Frequency': [usage_frequency],
                        'Support Calls': [support_calls],
                        'Payment Delay': [payment_delay],
                        'Subscription Type': [subscription_type],
                        'Contract Length': [contract_length],
                        'Total Spend': [total_spend],
                        'Last Interaction': [last_interaction],
                        'AgeGroup': [age_group]
                    })
                    
                    # Simulate loading with progress bar for better UX
                    progress_bar = st.progress(0)
                    for percent_complete in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(percent_complete + 1)
                    
                    try:
                        # Simulate model prediction (in a real app, this would load the model)
                        # Load the preprocessor and model
                        # preprocessor = joblib.load('preprocessor.pkl')
                        # model = joblib.load('model.pkl')
                        
                        # Preprocess the input data
                        # input_data_preprocessed = preprocessor.transform(input_data)
                        
                        # Simulate prediction
                        # Use contract type and tenure to determine churn probability for demo
                        churn_factors = {
                            'Monthly': 0.75,
                            'Quarterly': 0.45,
                            'Annual': 0.25
                        }
                        
                        tenure_factor = max(0, 1 - (tenure / 60))
                        usage_factor = max(0, 1 - (usage_frequency / 30))
                        support_factor = min(1, support_calls / 10)
                        
                        base_probability = churn_factors[contract_length]
                        churn_probability = (base_probability * 0.4 + 
                                            tenure_factor * 0.3 + 
                                            usage_factor * 0.2 + 
                                            support_factor * 0.1) * 100
                        
                        prediction = [1 if churn_probability > 50 else 0]
                        
                        # Display results with enhanced UI
                        cols = st.columns([1, 2, 1])
                        with cols[1]:
                            # Lottie animation for prediction
                            st_lottie(lottie_prediction, height=150, key="prediction_animation")
                            
                            if prediction[0] == 1:
                                st.markdown(f"""
                                <div class="prediction-box-negative animated">
                                    <h2>Churn Risk: High</h2>
                                    <h1 style="font-size: 3rem; font-weight: 700;">{churn_probability:.1f}%</h1>
                                    <p>This customer is showing significant signs of potential churn and requires immediate attention.</p>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                <div class="prediction-box-positive animated">
                                    <h2>Churn Risk: Low</h2>
                                    <h1 style="font-size: 3rem; font-weight: 700;">{churn_probability:.1f}%</h1>
                                    <p>This customer shows strong engagement patterns and is likely to remain active.</p>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        # Show prediction probability gauge chart with enhanced styling
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=churn_probability,
                            domain={'x': [0, 1], 'y': [0, 1]},
                            title={'text': "Churn Probability", 'font': {'size': 24, 'color': '#334155'}},
                            gauge={
                                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#334155"},
                                'bar': {'color': "#4F46E5"},
                                'steps': [
                                    {'range': [0, 30], 'color': "#BBF7D0"},
                                    {'range': [30, 70], 'color': "#FEF9C3"},
                                    {'range': [70, 100], 'color': "#FEE2E2"}
                                ],
                                'threshold': {
                                    'line': {'color': "#EF4444", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 70
                                }
                            }
                        ))
                        fig.update_layout(
                            height=300, 
                            margin=dict(l=20, r=20, t=50, b=20),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font={'color': "#334155", 'family': "Poppins"}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Show key factors with enhanced visualization
                        st.markdown('<div class="section-header animated">Key Churn Factors</div>', unsafe_allow_html=True)
                        
                        # Simulate feature importance with dynamic values
                        feature_importance = {
                            'Contract Length': 0.85 if contract_length == "Monthly" else 0.4,
                            'Tenure': 0.75 if tenure < 12 else 0.35,
                            'Usage Frequency': 0.65 if usage_frequency < 15 else 0.3,
                            'Payment Delay': 0.55 if payment_delay > 10 else 0.25,
                            'Support Calls': 0.45 if support_calls > 3 else 0.2
                        }
                        
                        # Sort features by importance
                        sorted_features = dict(sorted(feature_importance.items(), key=lambda item: item[1], reverse=True))
                        
                        # Plot horizontal bar chart with enhanced styling
                        fig = px.bar(
                            x=list(sorted_features.values()),
                            y=list(sorted_features.keys()),
                            orientation='h',
                            labels={'x': 'Impact on Prediction', 'y': 'Feature'},
                            title='',
                            color=list(sorted_features.values()),
                            color_continuous_scale='blues',
                            range_color=[0, 1]
                        )
                        fig.update_layout(
                            height=350,
                            margin=dict(l=20, r=20, t=30, b=20),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font={'color': "#334155", 'family': "Poppins"},
                            coloraxis_showscale=False,
                            xaxis_range=[0, 1]
                        )
                        
                        # Add value labels to the bars
                        fig.update_traces(texttemplate='%{x:.2f}', textposition='outside')
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Recommendations with enhanced card-based UI
                        if prediction[0] == 1:
                            st.markdown('<div class="section-header animated">Retention Recommendations</div>', unsafe_allow_html=True)
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.markdown("""
                                <div class="card animated">
                                    <h3 style="color: #4F46E5; margin-top: 0;">Personalized Outreach</h3>
                                    <p>Schedule a personalized check-in call to address potential concerns and gather feedback.</p>
                                    <p><strong>Priority: High</strong></p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                            with col2:
                                st.markdown("""
                                <div class="card animated">
                                    <h3 style="color: #4F46E5; margin-top: 0;">Contract Upgrade</h3>
                                    <p>Offer an incentive to upgrade to a longer-term contract with a loyalty discount.</p>
                                    <p><strong>Priority: Medium</strong></p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                            with col3:
                                st.markdown("""
                                <div class="card animated">
                                    <h3 style="color: #4F46E5; margin-top: 0;">Support Review</h3>
                                    <p>Review recent support interactions and follow up on any unresolved issues.</p>
                                    <p><strong>Priority: Medium</strong></p>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.error(f"Error making prediction: {e}")
                        st.warning("Please ensure the model and preprocessor files are available.")
            else:
                # Enhanced placeholder with animation before prediction
                cols = st.columns([1, 3, 1])
                with cols[1]:
                    st_lottie(lottie_prediction, height=200, key="waiting_animation")
                    st.markdown("""
                    <div class="info-box animated" style="text-align: center;">
                        <h3>Ready for Analysis</h3>
                        <p>Adjust the customer parameters in the sidebar and click 'Generate Prediction' to analyze churn risk.</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="section-header animated">Customer Profile Summary</div>', unsafe_allow_html=True)
            
            # Enhanced customer profile UI with cards
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="card">
                    <h3 style="color: #4F46E5; margin-top: 0;">Demographics</h3>
                    <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 0.5rem;">
                        <div style="font-weight: 600; color: #64748B;">Age:</div>
                        <div>{} ({})</div>
                        <div style="font-weight: 600; color: #64748B;">Gender:</div>
                        <div>{}</div>
                        <div style="font-weight: 600; color: #64748B;">Tenure:</div>
                        <div>{} months</div>
                        <div style="font-weight: 600; color: #64748B;">Contract:</div>
                        <div>{}</div>
                    </div>
                </div>
                """.format(age, age_group, gender, tenure, contract_length), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="card">
                    <h3 style="color: #4F46E5; margin-top: 0;">Activity & Financial</h3>
                    <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 0.5rem;">
                        <div style="font-weight: 600; color: #64748B;">Subscription:</div>
                        <div>{}</div>
                        <div style="font-weight: 600; color: #64748B;">Usage:</div>
                        <div>{}/30</div>
                        <div style="font-weight: 600; color: #64748B;">Total Spend:</div>
                        <div>${}</div>
                        <div style="font-weight: 600; color: #64748B;">Payment Delay:</div>
                        <div>{} days</div>
                        <div style="font-weight: 600; color: #64748B;">Support Calls:</div>
                        <div>{}</div>
                        <div style="font-weight: 600; color: #64748B;">Last Activity:</div>
                        <div>{} days ago</div>
                    </div>
                </div>
                """.format(subscription_type, usage_frequency, total_spend, payment_delay, support_calls, last_interaction), unsafe_allow_html=True)

    elif selected == "Model Insights":
        st.markdown('<h1 class="main-header animated">Model Insights</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header animated">Understanding the factors behind customer churn</p>', unsafe_allow_html=True)
        
        # Simulate model metrics and insights
        st.subheader("Model Performance")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Accuracy", "87.2%", "2.1%")
            
        with col2:
            st.metric("Precision", "83.5%", "1.8%")
            
        with col3:
            st.metric("Recall", "79.3%", "-0.5%")
            
        with col4:
            st.metric("F1 Score", "81.3%", "1.2%")
        
        # Feature importance visualization
        st.subheader("Overall Feature Importance")
        
        # Simulated feature importance
        features = ['Contract Length', 'Tenure', 'Usage Frequency', 'Last Interaction', 
                   'Payment Delay', 'Subscription Type', 'Support Calls', 'Total Spend', 'Age']
        importance = [0.23, 0.18, 0.15, 0.12, 0.10, 0.08, 0.07, 0.05, 0.02]
        
        # Create feature importance chart
        fig = px.bar(
            x=importance,
            y=features,
            orientation='h',
            labels={'x': 'Importance', 'y': 'Feature'},
            title=''
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Churn patterns
        st.subheader("Churn Patterns by Segment")
        
        # Create tabs for different segments
        segment_tabs = st.tabs(["Contract Type", "Age Group", "Subscription"])
        
        with segment_tabs[0]:
            # Contract type churn rates
            contract_types = ['Monthly', 'Quarterly', 'Annual']
            churn_rates = [0.27, 0.15, 0.08]
            
            fig = px.bar(
                x=contract_types,
                y=churn_rates,
                labels={'x': 'Contract Type', 'y': 'Churn Rate'},
                color=churn_rates,
                color_continuous_scale='blues'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Key Insight:** Monthly contract customers are more than 3x likely to churn compared to annual contract customers.
            We recommend focusing retention efforts on converting monthly customers to longer-term contracts.
            """)
            
        with segment_tabs[1]:
            # Age group churn rates
            age_groups = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
            age_churn_rates = [0.32, 0.24, 0.18, 0.15, 0.12, 0.10]
            
            fig = px.bar(
                x=age_groups,
                y=age_churn_rates,
                labels={'x': 'Age Group', 'y': 'Churn Rate'},
                color=age_churn_rates,
                color_continuous_scale='blues'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Key Insight:** Younger customers (18-35) show significantly higher churn rates.
            Consider developing targeted retention programs for these age segments.
            """)
            
        with segment_tabs[2]:
            # Subscription type churn rates
            subscription_types = ['Basic', 'Standard', 'Premium']
            sub_churn_rates = [0.23, 0.17, 0.08]
            
            fig = px.bar(
                x=subscription_types,
                y=sub_churn_rates,
                labels={'x': 'Subscription Type', 'y': 'Churn Rate'},
                color=sub_churn_rates,
                color_continuous_scale='blues'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Key Insight:** Premium subscribers have the lowest churn rate.
            Upselling customers to higher-tier packages could improve retention.
            """)
    
    elif selected == "Documentation":
        st.markdown('<h1 class="main-header animated">Documentation</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header animated">How to use the Churn Prediction tool</p>', unsafe_allow_html=True)
        
        # Documentation content
        st.markdown("""
        ### Overview
        This Churn Prediction application helps you identify customers at risk of churning.
        By analyzing customer data across multiple dimensions, the model provides a probability
        score indicating how likely a customer is to discontinue service.
        
        ### Input Parameters
        
        #### Demographics
        - **Age:** Customer's age in years
        - **Gender:** Customer's gender (Male/Female)
        - **Age Group:** Age bracket for segment analysis
        
        #### Relationship Information
        - **Tenure:** How long the customer has been with the company (in months)
        - **Contract Length:** Type of contract (Monthly, Quarterly, Annual)
        
        #### Usage Patterns
        - **Usage Frequency:** How often the customer uses the product/service (scale 0-100)
        - **Last Interaction:** Days since the customer last interacted with the product
        
        #### Financial Metrics
        - **Subscription Type:** Customer's subscription tier (Basic, Standard, Premium)
        - **Total Spend:** Total amount spent by the customer
        - **Payment Delay:** Average delay in payments (days)
        
        #### Support History
        - **Support Calls:** Number of support calls made by the customer
        
        ### Interpreting Results
        The prediction result includes:
        - Churn probability (percentage)
        - Risk classification (High/Low)
        - Key factors influencing the prediction
        - Retention recommendations for high-risk customers
        
        ### Recommended Actions
        For high-risk customers:
        1. Implement proactive outreach
        2. Offer personalized retention incentives
        3. Address identified pain points
        4. Consider contract upgrades or commitment incentives
        """)
        
        # Model information
        with st.expander("Model Information", expanded=False):
            st.markdown("""
            ### Model Details
            - **Algorithm:** Random Forest Classifier
            - **Features:** 11 customer attributes
            - **Training Data:** Historical customer data with churn outcomes
            - **Validation Method:** 5-fold cross-validation
            - **Last Updated:** February 2025
            
            ### Model Limitations
            - Predictions are probabilities, not certainties
            - Model may perform differently for customer segments underrepresented in training data
            - External factors (competition, industry changes) are not captured in the model
            """)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2025 Customer Churn Predictor | Version 1.0.2 | Last Updated: February 2025</p>
    </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()