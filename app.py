"""
Interactive Streamlit Data Dashboard: Alcoholic Beverage Sector - Wine Quality Analysis & Prediction
Client Presentation: Screaming Eagle Winery / Global Beverage Analytics
"""

import os
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn import metrics

# Set Streamlit page configuration
st.set_page_config(
    page_title="VinoAnalytics | Wine Quality Intelligence Dashboard",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #722F37; /* Wine Burgundy */
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555555;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #fcf8f8;
        border-radius: 8px;
        padding: 15px;
        border-left: 5px solid #722F37;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .highlight-box {
        background-color: #f7f9fa;
        padding: 18px;
        border-radius: 8px;
        border: 1px solid #e1e8ed;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. LOAD DATA & MODEL ARTIFACTS
# -------------------------------------------------------------
@st.cache_data
def load_dataset():
    df = pd.read_csv('wine_quality.csv')
    df.columns = df.columns.str.strip()
    return df

@st.cache_resource
def load_models():
    artifact_path = 'artifacts/model_bundle.joblib'
    if os.path.exists(artifact_path):
        return joblib.load(artifact_path)
    return None

df_raw = load_dataset()
model_bundle = load_models()

# -------------------------------------------------------------
# SIDEBAR CONTROLS
# -------------------------------------------------------------
st.sidebar.image("https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=500&auto=format&fit=crop&q=60", use_container_width=True)
st.sidebar.title("🍷 VinoAnalytics Studio")
st.sidebar.markdown("**Wine Quality Intelligence & Predictive Engine**")
st.sidebar.caption("Screaming Eagle Winery Case Study")

st.sidebar.divider()
st.sidebar.subheader("Navigation")
menu_choice = st.sidebar.radio(
    "Go to Module:",
    [
        "Executive Summary & Business Context",
        "Exploratory Data Analysis (EDA)",
        "Model Benchmarks & Evaluation",
        "Real-Time Wine Quality Predictor",
        "Strategic Winery Recommendations"
    ]
)

st.sidebar.divider()
st.sidebar.subheader("Global Data Filters")
selected_colors = st.sidebar.multiselect(
    "Wine Varietal Color:",
    options=['red', 'white'],
    default=['red', 'white']
)

alcohol_range = st.sidebar.slider(
    "Alcohol Range (% vol):",
    min_value=float(df_raw['alcohol'].min()),
    max_value=float(df_raw['alcohol'].max()),
    value=(float(df_raw['alcohol'].min()), float(df_raw['alcohol'].max())),
    step=0.1
)

quality_filter = st.sidebar.slider(
    "Quality Score Range (3 to 9):",
    min_value=int(df_raw['quality'].min()),
    max_value=int(df_raw['quality'].max()),
    value=(int(df_raw['quality'].min()), int(df_raw['quality'].max())),
    step=1
)

# Apply filters
filtered_df = df_raw[
    (df_raw['color'].isin(selected_colors)) &
    (df_raw['alcohol'] >= alcohol_range[0]) &
    (df_raw['alcohol'] <= alcohol_range[1]) &
    (df_raw['quality'] >= quality_filter[0]) &
    (df_raw['quality'] <= quality_filter[1])
]

st.sidebar.caption(f"Filtered Records: **{len(filtered_df):,}** of **{len(df_raw):,}** ({len(filtered_df)/len(df_raw):.1%})")

# -------------------------------------------------------------
# TOP STATS KPI BANNER
# -------------------------------------------------------------
col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)
with col_kpi1:
    st.metric("Total Samples", f"{len(filtered_df):,}")
with col_kpi2:
    good_pct = (filtered_df['good'].mean() * 100) if len(filtered_df) > 0 else 0
    st.metric("Premium Vintages (>=7)", f"{good_pct:.1f}%")
with col_kpi3:
    avg_alc = filtered_df['alcohol'].mean() if len(filtered_df) > 0 else 0
    st.metric("Avg Alcohol", f"{avg_alc:.2f}%")
with col_kpi4:
    avg_va = filtered_df['volatile acidity'].mean() if len(filtered_df) > 0 else 0
    st.metric("Avg Volatile Acidity", f"{avg_va:.3f} g/L")
with col_kpi5:
    avg_ph = filtered_df['pH'].mean() if len(filtered_df) > 0 else 0
    st.metric("Avg pH", f"{avg_ph:.2f}")

st.divider()

# =============================================================
# MODULE 1: EXECUTIVE SUMMARY & BUSINESS CONTEXT
# =============================================================
if menu_choice == "Executive Summary & Business Context":
    st.markdown('<div class="main-header">Alcoholic Beverage Sector: Wine Quality Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Data-driven decision framework for production consistency, sensory excellence, and commercial premiumization</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Business Problem & Domain Understanding
    In the global alcoholic beverage sector, wine quality dictates consumer satisfaction, critical acclaim (Robert Parker, Wine Spectator 100-point scale), brand prestige, and auction valuation.
    Unlike standard consumer packaged goods, wine quality is governed by a delicate synthesis of **chemical composition** (fermentation balance, acidity, preservative sulfur chemistry) and **sensory characteristics** (aroma, mouthfeel, finish, complexity).
    """)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        #### 🍇 Chemical Composition Foundations
        - **Fixed Acidity**: Tartaric, malic, and citric acids shaping crispness and structure.
        - **Volatile Acidity**: Acetic acid. Excessive levels lead to an undesirable vinegar flaw.
        - **Residual Sugar**: Post-fermentation sweetness, countering perceived astringency.
        - **Sulfur Dioxide ($SO2$)**: Essential antioxidant & antimicrobial agent.
        - **Density & Chlorides**: Reflect dissolved solids, body, and mouthfeel salinity.
        - **Alcohol**: Determines warmth, body, and aromatic volatility.
        """)
    with col2:
        st.markdown("""
        #### 🏆 The Business Imperative for Quality Prediction
        - **Brand Equity Protection**: Preventing defective or substandard batches from reaching ultra-premium product lines.
        - **Pricing Power & Allocation**: High-quality wines command exponential price premiums in premier markets.
        - **Fermentation Optimization**: Empowering cellar masters to intervene chemically (e.g. yeast nutrition, temperature control) before flaws become irreversible.
        - **Inventory & Aging Strategies**: Channeling well-structured wines into barrel aging while moving lighter wines to immediate distribution.
        """)
        
    st.subheader("Dataset Explorer")
    st.dataframe(filtered_df.head(20), use_container_width=True)
    
    csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Wine Dataset (CSV)",
        data=csv_bytes,
        file_name="filtered_wine_quality.csv",
        mime="text/csv"
    )

# =============================================================
# MODULE 2: EXPLORATORY DATA ANALYSIS (EDA)
# =============================================================
elif menu_choice == "Exploratory Data Analysis (EDA)":
    st.markdown('<div class="main-header">Sprint 1: Exploratory Data Analysis & Chemical Drivers</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Investigating feature distributions, color differentials, and key correlation drivers</div>', unsafe_allow_html=True)
    
    eda_tabs = st.tabs([
        "📊 Target Distributions",
        "📈 Physicochemical Distributions",
        "🔴 Red vs ⚪ White Chemistry",
        "🔥 Correlation Matrix",
        "🔬 Key Bivariate Drivers"
    ])
    
    with eda_tabs[0]:
        st.subheader("Sensory Quality Rating Distribution")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            fig_qual = px.histogram(
                filtered_df, x='quality', color='quality',
                title="Wine Quality Score Frequency (3 to 9)",
                color_discrete_sequence=px.colors.sequential.Viridis,
                labels={'quality': 'Sensory Quality Score'},
                text_auto=True
            )
            fig_qual.update_layout(bargap=0.2, showlegend=False)
            st.plotly_chart(fig_qual, use_container_width=True)
        with col_t2:
            good_summary = filtered_df['good'].value_counts().reset_index()
            good_summary['Label'] = good_summary['good'].map({0: 'Standard (Score < 7)', 1: 'Premium (Score >= 7)'})
            fig_pie = px.pie(
                good_summary, values='count', names='Label',
                title="Binary Quality Class Breakdown",
                color_discrete_sequence=['#e74c3c', '#27ae60'],
                hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        st.info("💡 **Key Finding**: Sensory scores follow a bell curve centered at scores 5 and 6 (~77% of all wines). Premium wines (score 7, 8, 9) make up approximately 19.7% of total vintages, representing an imbalanced but highly valuable target class.")

    with eda_tabs[1]:
        st.subheader("Distribution of Physicochemical Variables")
        feature_to_plot = st.selectbox(
            "Select Chemical Attribute to Inspect:",
            options=[
                'fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
                'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density',
                'pH', 'sulphates', 'alcohol'
            ],
            index=10
        )
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            fig_hist = px.histogram(
                filtered_df, x=feature_to_plot, color='good',
                marginal="box",
                barmode="overlay",
                opacity=0.6,
                color_discrete_map={0: '#e74c3c', 1: '#2ecc71'},
                title=f"Distribution of {feature_to_plot.title()} (Standard vs Premium)",
                labels={'good': 'Quality Tier'}
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            
        with col_d2:
            fig_box = px.box(
                filtered_df, x='quality', y=feature_to_plot, color='quality',
                title=f"{feature_to_plot.title()} across Quality Scores",
                color_discrete_sequence=px.colors.sequential.Plasma
            )
            fig_box.update_layout(showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)

    with eda_tabs[2]:
        st.subheader("Red Wine vs White Wine Physicochemical Profile")
        st.write("Red and white wines undergo fundamentally distinct vinification processes (maceration on grape skins vs pressed juice fermentation), resulting in marked chemical differences.")
        
        color_compare_feature = st.selectbox(
            "Compare Attribute by Wine Color:",
            options=['volatile acidity', 'fixed acidity', 'residual sugar', 'total sulfur dioxide', 'chlorides', 'sulphates', 'alcohol'],
            index=0
        )
        
        fig_color = px.violin(
            filtered_df, x='color', y=color_compare_feature, color='color',
            box=True, points="all",
            color_discrete_map={'red': '#8B0000', 'white': '#F4D03F'},
            title=f"Distribution of {color_compare_feature.title()} by Color Varietal"
        )
        st.plotly_chart(fig_color, use_container_width=True)
        
        # Color summary stats
        color_summary = filtered_df.groupby('color')[['alcohol', 'volatile acidity', 'residual sugar', 'total sulfur dioxide', 'chlorides', 'pH']].mean().round(3)
        st.dataframe(color_summary, use_container_width=True)

    with eda_tabs[3]:
        st.subheader("Physicochemical Correlation Heatmap")
        numeric_cols = [
            'fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
            'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density',
            'pH', 'sulphates', 'alcohol', 'quality', 'good'
        ]
        corr_matrix = filtered_df[numeric_cols].corr().round(3)
        
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r",
            zmin=-0.6, zmax=0.6,
            title="Pearson Correlation Matrix (Features vs Quality & Good)"
        )
        fig_corr.update_layout(height=650)
        st.plotly_chart(fig_corr, use_container_width=True)
        
        st.markdown("""
        **Top Quality Correlations:**
        1. **Alcohol (+0.44 with quality, +0.39 with good)**: Strongest positive driver. Riper grapes yield higher alcohol and fuller mouthfeel.
        2. **Density (-0.31 with quality, -0.28 with good)**: Negative correlation. Higher alcohol and lower unfermented solids decrease density.
        3. **Volatile Acidity (-0.27 with quality, -0.15 with good)**: Detrimental defect indicator. High acetic acid ruins sensory ratings.
        4. **Chlorides (-0.20 with quality, -0.16 with good)**: Excess salts create harsh, salty mouthfeel, detracting from balance.
        """)

    with eda_tabs[4]:
        st.subheader("Key Bivariate Chemical Drivers")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            fig_scat1 = px.scatter(
                filtered_df, x='volatile acidity', y='alcohol', color='good',
                opacity=0.65,
                color_discrete_map={0: '#95a5a6', 1: '#27ae60'},
                labels={'good': 'Good Wine (1=Yes, 0=No)'},
                title="Primary Quality Sweet Spot: High Alcohol & Low Volatile Acidity"
            )
            st.plotly_chart(fig_scat1, use_container_width=True)
            
        with col_b2:
            fig_scat2 = px.scatter(
                filtered_df, x='residual sugar', y='density', color='color',
                opacity=0.5,
                color_discrete_map={'red': '#8B0000', 'white': '#d4ac0d'},
                title="Density vs Residual Sugar (Body, Extraction, & Sweetness)"
            )
            st.plotly_chart(fig_scat2, use_container_width=True)

# =============================================================
# MODULE 3: MODEL BENCHMARKS & EVALUATION (SPRINT 3)
# =============================================================
elif menu_choice == "Model Benchmarks & Evaluation":
    st.markdown('<div class="main-header">Sprint 3: Model Building & Multi-Algorithm Benchmarking</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluating 5 Machine Learning Algorithms (KNN, Logistic Regression, SVM, Decision Tree, Random Forest)</div>', unsafe_allow_html=True)
    
    if model_bundle is not None:
        benchmark_df = model_bundle['benchmark_df']
        
        col_m1, col_m2 = st.columns([1.2, 1])
        with col_m1:
            st.subheader("Comparative Accuracy Leaderboard")
            
            # Interactive Bar Chart
            fig_bench = px.bar(
                benchmark_df,
                x='Algorithm', y='Test_Accuracy',
                text=[f"{v*100:.2f}%" for v in benchmark_df['Test_Accuracy']],
                color='Algorithm',
                color_discrete_sequence=['#27ae60', '#f39c12', '#8e44ad', '#c0392b', '#2980b9'],
                title="Test Accuracy Across All 5 Algorithms",
                labels={'Test_Accuracy': 'Accuracy Score'}
            )
            fig_bench.update_layout(yaxis_range=[0.70, 0.95], showlegend=False)
            fig_bench.add_hline(y=0.8037, line_dash="dash", line_color="gray", annotation_text="Majority Class Baseline (80.4%)")
            st.plotly_chart(fig_bench, use_container_width=True)
            
        with col_m2:
            st.subheader("Comprehensive Diagnostic Metrics")
            st.dataframe(
                benchmark_df.style.format({
                    'Train_Accuracy': '{:.2%}',
                    'Test_Accuracy': '{:.2%}',
                    'Precision': '{:.2%}',
                    'Recall': '{:.2%}',
                    'F1_Score': '{:.4f}',
                    'ROC_AUC': '{:.4f}'
                }).highlight_max(subset=['Test_Accuracy', 'F1_Score', 'ROC_AUC'], color='#d4edda'),
                use_container_width=True
            )
            
            st.success("""
            🏆 **Champion Model: Random Forest Classifier**
            - **Test Accuracy**: 88.00%
            - **F1-Score**: 0.6355
            - **ROC-AUC**: 0.9069
            - Outperforms linear and distance boundaries by capturing non-linear interactions across the chemical landscape without severe overfitting.
            """)
            
        st.divider()
        st.subheader("Diagnostic Deep Dive: Confusion Matrices & Feature Importance")
        col_cm, col_fi = st.columns(2)
        
        with col_cm:
            selected_algo_cm = st.selectbox(
                "Select Algorithm to View Confusion Matrix:",
                options=benchmark_df['Algorithm'].tolist()
            )
            cm_data = np.array(model_bundle['confusion_matrices'][selected_algo_cm])
            
            fig_cm = px.imshow(
                cm_data,
                text_auto=True,
                x=['Predicted Standard (0)', 'Predicted Premium (1)'],
                y=['Actual Standard (0)', 'Actual Premium (1)'],
                color_continuous_scale="Blues",
                title=f"Confusion Matrix: {selected_algo_cm}"
            )
            st.plotly_chart(fig_cm, use_container_width=True)
            
        with col_fi:
            feat_imp_df = model_bundle['feature_importances']
            fig_fi = px.bar(
                feat_imp_df,
                x='Importance', y='Feature',
                orientation='h',
                title="Random Forest Feature Importance (MDI)",
                color='Importance',
                color_continuous_scale='Viridis'
            )
            fig_fi.update_layout(yaxis={'categoryorder': 'total ascending'}, height=420)
            st.plotly_chart(fig_fi, use_container_width=True)
    else:
        st.warning("Model bundle not detected. Please run `train_models.py` first to generate models and metrics.")

# =============================================================
# MODULE 4: REAL-TIME WINE QUALITY PREDICTOR (INFERENCE)
# =============================================================
elif menu_choice == "Real-Time Wine Quality Predictor":
    st.markdown('<div class="main-header">Interactive Wine Quality Inference Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Adjust physicochemical inputs to simulate wine batches and receive real-time quality forecasts</div>', unsafe_allow_html=True)
    
    if model_bundle is not None:
        st.markdown("#### 🧪 Select Batch Preset or Tune Parameters")
        
        col_preset1, col_preset2, col_preset3 = st.columns(3)
        preset = None
        if col_preset1.button("🍷 Load Preset: Screaming Eagle Cabernet (Ultra-Premium Red)"):
            preset = "premium_red"
        if col_preset2.button("🥂 Load Preset: Sonoma Reserve Chardonnay (Premium White)"):
            preset = "premium_white"
        if col_preset3.button("📦 Load Preset: Commercial Table Blend (Standard Quality)"):
            preset = "standard"

        # Default presets
        defaults = {
            'color': 'red', 'alcohol': 12.8, 'volatile_acidity': 0.28, 'citric_acid': 0.42,
            'residual_sugar': 2.4, 'chlorides': 0.045, 'free_so2': 32.0, 'total_so2': 90.0,
            'density': 0.9935, 'pH': 3.35, 'sulphates': 0.72, 'fixed_acidity': 7.6
        }
        if preset == "premium_red":
            defaults = {'color': 'red', 'alcohol': 13.5, 'volatile_acidity': 0.26, 'citric_acid': 0.45, 'residual_sugar': 2.2, 'chlorides': 0.042, 'free_so2': 28.0, 'total_so2': 75.0, 'density': 0.9928, 'pH': 3.40, 'sulphates': 0.78, 'fixed_acidity': 7.8}
        elif preset == "premium_white":
            defaults = {'color': 'white', 'alcohol': 12.6, 'volatile_acidity': 0.22, 'citric_acid': 0.38, 'residual_sugar': 5.5, 'chlorides': 0.038, 'free_so2': 38.0, 'total_so2': 115.0, 'density': 0.9920, 'pH': 3.18, 'sulphates': 0.55, 'fixed_acidity': 6.8}
        elif preset == "standard":
            defaults = {'color': 'red', 'alcohol': 9.8, 'volatile_acidity': 0.68, 'citric_acid': 0.05, 'residual_sugar': 3.2, 'chlorides': 0.095, 'free_so2': 14.0, 'total_so2': 135.0, 'density': 0.9982, 'pH': 3.55, 'sulphates': 0.45, 'fixed_acidity': 7.2}

        # Input form
        with st.form("prediction_form"):
            col_f1, col_f2, col_f3 = st.columns(3)
            
            with col_f1:
                st.markdown("**Core Fermentation Profile**")
                color_in = st.selectbox("Wine Varietal Color", ['red', 'white'], index=0 if defaults['color'] == 'red' else 1)
                alcohol_in = st.slider("Alcohol (% vol)", 8.0, 15.0, float(defaults['alcohol']), 0.1)
                volatile_acidity_in = st.slider("Volatile Acidity (g/L acetic acid)", 0.05, 1.60, float(defaults['volatile_acidity']), 0.01)
                density_in = st.slider("Density (g/cm³)", 0.987, 1.010, float(defaults['density']), 0.0005, format="%.4f")
                
            with col_f2:
                st.markdown("**Acidity & Sugar Balance**")
                fixed_acidity_in = st.slider("Fixed Acidity (g/L)", 3.5, 16.0, float(defaults['fixed_acidity']), 0.1)
                citric_acid_in = st.slider("Citric Acid (g/L)", 0.0, 1.6, float(defaults['citric_acid']), 0.02)
                residual_sugar_in = st.slider("Residual Sugar (g/L)", 0.5, 30.0, float(defaults['residual_sugar']), 0.1)
                pH_in = st.slider("pH Level", 2.7, 4.1, float(defaults['pH']), 0.02)

            with col_f3:
                st.markdown("**Preservation & Salts**")
                chlorides_in = st.slider("Chlorides (g/L NaCl)", 0.01, 0.40, float(defaults['chlorides']), 0.005)
                free_so2_in = st.slider("Free Sulfur Dioxide (mg/L)", 2.0, 120.0, float(defaults['free_so2']), 1.0)
                total_so2_in = st.slider("Total Sulfur Dioxide (mg/L)", 10.0, 300.0, float(defaults['total_so2']), 2.0)
                sulphates_in = st.slider("Sulphates (g/L potassium sulphate)", 0.20, 2.00, float(defaults['sulphates']), 0.02)

            selected_model_name = st.selectbox(
                "Inference Engine Algorithm:",
                options=list(model_bundle['models'].keys()),
                index=4  # Default to Random Forest
            )
            
            submit_btn = st.form_submit_button("🍷 Run Batch Evaluation & Quality Forecast", use_container_width=True)

        if submit_btn:
            # Construct feature dataframe
            input_dict = {
                'fixed acidity': fixed_acidity_in,
                'volatile acidity': volatile_acidity_in,
                'citric acid': citric_acid_in,
                'residual sugar': residual_sugar_in,
                'chlorides': chlorides_in,
                'free sulfur dioxide': free_so2_in,
                'total sulfur dioxide': total_so2_in,
                'density': density_in,
                'pH': pH_in,
                'sulphates': sulphates_in,
                'alcohol': alcohol_in,
                'color': color_in
            }
            sample_df = pd.DataFrame([input_dict])
            
            # Transform
            scaler = model_bundle['scaler']
            ohe = model_bundle['ohe']
            num_cols = model_bundle['num_cols']
            cat_cols = model_bundle['cat_cols']
            
            sample_num = scaler.transform(sample_df[num_cols])
            sample_cat = ohe.transform(sample_df[cat_cols])
            sample_prep = np.hstack([sample_num, sample_cat])
            
            # Predict
            model = model_bundle['models'][selected_model_name]
            pred = model.predict(sample_prep)[0]
            
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(sample_prep)[0]
                prob_good = proba[1]
            else:
                prob_good = 1.0 if pred == 1 else 0.0

            st.markdown("### 🏆 Prediction Results & Sensory Prognosis")
            
            res_col1, res_col2 = st.columns([1.2, 1])
            with res_col1:
                if pred == 1:
                    st.success(f"""
                    ### 🌟 PREDICTED: PREMIUM VINTAGE (Quality Score $>=$ 7)
                    **Confidence / Probability of Good Wine**: **{prob_good:.1%}**  
                    *Model Employed: {selected_model_name}*
                    
                    This batch exhibits superior balance, sufficient alcohol structure ({alcohol_in}%), restrained volatile acidity ({volatile_acidity_in} g/L), and sound preservative chemistry.
                    """)
                else:
                    st.error(f"""
                    ### ⚠️ PREDICTED: STANDARD TABLE WINE (Quality Score < 7)
                    **Confidence / Probability of Standard Class**: **{(1 - prob_good):.1%}**  
                    *Model Employed: {selected_model_name}*
                    
                    The physicochemical composition does not currently satisfy ultra-premium reserve standards. Review winemaking intervention levers below.
                    """)
            
            with res_col2:
                # Gauge chart
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = prob_good * 100,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Premium Probability (%)"},
                    gauge = {
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#27ae60" if pred == 1 else "#e74c3c"},
                        'steps': [
                            {'range': [0, 50], 'color': "#f9ebea"},
                            {'range': [50, 75], 'color': "#fcf3cf"},
                            {'range': [75, 100], 'color': "#d4efdf"}
                        ],
                        'threshold': {
                            'line': {'color': "black", 'width': 3},
                            'thickness': 0.75,
                            'value': 50
                        }
                    }
                ))
                fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=30, b=20))
                st.plotly_chart(fig_gauge, use_container_width=True)

            # Winemaking recommendations for this batch
            st.markdown("#### 🛠️ Tailored Oenological Recommendations for this Batch:")
            recs = []
            if volatile_acidity_in > 0.50:
                recs.append("⚠️ **Volatile Acidity is Elevated (>0.50 g/L)**: Risk of vinegary aroma (acetic acid) and ethyl acetate nail-polish odor. Recommended Action: Enhance sulfur dioxide protection, avoid exposure to oxygen, or perform reverse osmosis/microfiltration.")
            if alcohol_in < 11.0:
                recs.append("📉 **Alcohol Level is Modest (<11.0%)**: Lower alcohol wines struggle to reach premium sensory scores. Recommended Action: Ensure grape maturity at harvest (Brix $>=$ 23-25) or evaluate chaptalization where legally permitted.")
            if sulphates_in < 0.50:
                recs.append("🧪 **Sulphate Buffer is Low (<0.50 g/L)**: Sulphates inhibit microbial spoilage. Recommended Action: Adjust potassium metabisulfite levels to safeguard aging potential.")
            if free_so2_in < 20.0 and pH_in > 3.4:
                recs.append("🛡️ **Molecular $SO2$ Deficit**: At pH > 3.4, free $SO2$ below 20 mg/L leaves the vintage vulnerable to oxidation and Brettanomyces bacterial spoilage.")
            if not recs:
                recs.append("✅ **Exemplary Physicochemical Balance**: All critical levers (Alcohol, Volatile Acidity, Free/Total $SO2$, and Sulphates) sit squarely within the premier benchmark zone.")
            
            for r in recs:
                st.markdown(f"- {r}")
    else:
        st.warning("Model bundle not loaded.")

# =============================================================
# MODULE 5: STRATEGIC WINERY RECOMMENDATIONS
# =============================================================
elif menu_choice == "Strategic Winery Recommendations":
    st.markdown('<div class="main-header">Strategic Winery Recommendations & Business Roadmap</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Data-driven business decisions for winery executive leadership, vineyard managers, and cellar masters</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Based on our exploratory data analysis and predictive model benchmarks across **6,497 wine samples**, we provide five strategic pillars to elevate wine quality, build brand equity, and maximize profitability.
    """)
    
    col_r1, col_r2 = st.columns(2)
    
    with col_r1:
        st.markdown("""
        ### 1. Vineyard Harvest & Sugar-Alcohol Optimization
        - **Insight**: Alcohol content is the single strongest positive correlate (+0.44) and top Random Forest feature (21.4% importance). Wines above **11.5% alcohol** have a **3.8x higher probability** of achieving premium quality ratings.
        - **Action**: Optimize canopy management, yield control (green harvesting), and harvest timing to achieve optimal grape phenolic maturity (23–26° Brix).
        
        ### 2. Fermentation Temperature & Volatile Acidity Control
        - **Insight**: Volatile acidity exhibits a severe negative correlation (-0.27 with quality). Premium wines maintain average volatile acidity below **0.29 g/L**, whereas low-quality wines average **0.53 g/L**.
        - **Action**: Enforce strict cellar sanitation, keep fermentation temperatures cool ($15-18^ deg C$ for whites, $24-28^ deg C$ for reds), prevent aeration during pump-overs, and inoculate selected Saccharomyces yeast strains to suppress wild acetic acid bacteria (*Acetobacter*).
        
        ### 3. Precision Sulfur Dioxide ($SO2$) Stewardship
        - **Insight**: Total $SO2$ alone does not drive quality; rather, maintaining an active **Free-to-Total $SO2$ ratio** relative to wine pH is essential to prevent oxidation without introducing sulfury aromas.
        - **Action**: Target 0.6–0.8 mg/L molecular $SO2$ by dynamically adjusting free $SO2$ based on pH measurements throughout aging and bottling.
        """)
        
    with col_r2:
        st.markdown("""
        ### 4. Color-Specific Cellar SOPs (Red vs White)
        - **Insight**: White wines require tighter total $SO2$ bounds due to vulnerability to enzymatic browning, while red wines benefit from higher polyphenol extraction, lower volatile acidity, and optimal sulphate levels (potassium sulphate average 0.65 g/L).
        - **Action**: Implement differentiated production protocols for Red vs White vinification rather than blanket cellar thresholds.
        
        ### 5. Commercial Tiering & Economic Allocation
        - **Insight**: Machine learning identifies batch quality before final bottling with **88% accuracy**.
        - **Action**:
          - **Tier 1 (Flagship / Screaming Eagle Reserve)**: Allocate batches with predicted premium probability $>= 85\%$ for new French oak maturation and premium auction pricing ($500+).
          - **Tier 2 (Estate Label)**: Batches between 50% and 84% probability allocated for second-label estate wines ($75-$150).
          - **Tier 3 (Everyday Blend / Bulk Distribution)**: Batches below 50% routed to early release or bulk blending, protecting brand reputation from substandard vintages.
        """)
        
    st.divider()
    st.info("💡 **Executive Summary**: Leveraging physicochemical predictive modeling enables early intervention during vinification, optimizes cellar resource allocation, protects brand prestige, and unlocks substantial price premiums across the winery portfolio.")
