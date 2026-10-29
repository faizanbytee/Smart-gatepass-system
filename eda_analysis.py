"""
Wine Quality Case Study - Sprint 1: Exploratory Data Analysis (EDA)
Author: Data Science Team (Screaming Eagle Winery Case Study)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configure visual style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

os.makedirs('eda_plots', exist_ok=True)

# 1. Load Data
df = pd.read_csv('wine_quality.csv')
df.columns = df.columns.str.strip()

print("="*60)
print("DATASET OVERVIEW")
print("="*60)
print(f"Total rows: {df.shape[0]}, Total columns: {df.shape[1]}")
print("\nMissing Values per column:\n", df.isnull().sum())
print("\nData Types:\n", df.dtypes)
print("\nStatistical Summary:\n", df.describe().T)

# 2. Target Variable Exploration
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Quality score distribution
sns.countplot(data=df, x='quality', palette='viridis', ax=axes[0], hue='quality', legend=False)
axes[0].set_title('Sensory Quality Score Distribution (3 to 9)', fontsize=13, fontweight='bold', pad=10)
axes[0].set_xlabel('Quality Score (0-10 scale)', fontsize=11)
axes[0].set_ylabel('Wine Sample Count', fontsize=11)
for p in axes[0].patches:
    axes[0].annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='baseline', fontsize=10, xytext=(0, 4), textcoords='offset points')

# Good (binary) distribution
good_counts = df['good'].value_counts()
colors = ['#d9534f', '#5cb85c']
axes[1].pie(good_counts, labels=['Standard Wine (0)\nQuality < 7', 'Premium/Good Wine (1)\nQuality >= 7'],
           autopct='%1.1f%%', startangle=140, colors=colors, explode=(0, 0.08),
           textprops={'fontsize': 11, 'fontweight': 'bold'}, shadow=True)
axes[1].set_title('Wine Quality Classification: Standard vs Premium', fontsize=13, fontweight='bold', pad=10)

plt.tight_layout()
plt.savefig('eda_plots/01_target_distributions.png', dpi=300)
plt.close()

# 3. Distribution of Each Physicochemical Feature
numeric_features = [
    'fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
    'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density',
    'pH', 'sulphates', 'alcohol'
]

fig, axes = plt.subplots(4, 3, figsize=(16, 14))
axes = axes.flatten()

for i, col in enumerate(numeric_features):
    sns.histplot(df[col], kde=True, ax=axes[i], color='#2c3e50', bins=30)
    skew = df[col].skew()
    axes[i].set_title(f'{col} (Skew: {skew:.2f})', fontsize=11, fontweight='bold')
    axes[i].set_xlabel('')
    axes[i].set_ylabel('Frequency')

fig.delaxes(axes[11])
plt.suptitle('Physicochemical Feature Distributions & Skewness', fontsize=15, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig('eda_plots/02_feature_distributions.png', dpi=300)
plt.close()

# 4. Feature Distributions by Wine Color (Red vs White)
fig, axes = plt.subplots(4, 3, figsize=(16, 14))
axes = axes.flatten()

for i, col in enumerate(numeric_features):
    sns.kdeplot(data=df, x=col, hue='color', common_norm=False, fill=True, alpha=0.35,
                palette={'red': '#8B0000', 'white': '#F4D03F'}, ax=axes[i])
    axes[i].set_title(f'{col} by Wine Color', fontsize=11, fontweight='bold')
    axes[i].set_xlabel('')
    axes[i].set_ylabel('Density')

fig.delaxes(axes[11])
plt.suptitle('Physicochemical Contrasts: Red Wine vs White Wine', fontsize=15, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig('eda_plots/03_color_comparisons.png', dpi=300)
plt.close()

# 5. Correlation Matrix Heatmap
plt.figure(figsize=(12, 9))
corr = df[numeric_features + ['quality', 'good']].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm', vmin=-0.7, vmax=0.7,
            linewidths=0.5, cbar_kws={'label': 'Pearson Correlation'})
plt.title('Correlation Heatmap: Physicochemical Attributes vs Quality Indicators', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('eda_plots/04_correlation_heatmap.png', dpi=300)
plt.close()

# 6. Boxplots: Physicochemical Features vs Quality (Significance analysis)
fig, axes = plt.subplots(4, 3, figsize=(16, 14))
axes = axes.flatten()

for i, col in enumerate(numeric_features):
    sns.boxplot(data=df, x='good', y=col, palette=['#e74c3c', '#2ecc71'], ax=axes[i], hue='good', legend=False)
    axes[i].set_title(f'{col} vs Good Wine (0 vs 1)', fontsize=11, fontweight='bold')
    axes[i].set_xlabel('Wine Quality Class (0 = Standard, 1 = Good)')
    axes[i].set_ylabel(col)

fig.delaxes(axes[11])
plt.suptitle('Boxplot Analysis: Standard Wines (0) vs Premium Wines (1)', fontsize=15, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig('eda_plots/05_boxplots_vs_good.png', dpi=300)
plt.close()

# 7. Crucial Bivariate Driver Plots
fig, axes = plt.subplots(2, 2, figsize=(14, 11))

# Alcohol vs Volatile Acidity with Good hue
sns.scatterplot(data=df, x='volatile acidity', y='alcohol', hue='good', alpha=0.6,
                palette=['#7f8c8d', '#27ae60'], ax=axes[0, 0])
axes[0, 0].set_title('Alcohol vs Volatile Acidity (Top Quality Drivers)', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Volatile Acidity (g/dm³ acetic acid)')
axes[0, 0].set_ylabel('Alcohol (% vol)')

# Density vs Residual Sugar by Color
sns.scatterplot(data=df, x='residual sugar', y='density', hue='color', alpha=0.5,
                palette={'red': '#8B0000', 'white': '#d4ac0d'}, ax=axes[0, 1])
axes[0, 1].set_title('Density vs Residual Sugar (Body & Sweetness)', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Residual Sugar (g/dm³)')
axes[0, 1].set_ylabel('Density (g/cm³)')

# Free SO2 vs Total SO2
sns.scatterplot(data=df, x='total sulfur dioxide', y='free sulfur dioxide', hue='good', alpha=0.6,
                palette=['#95a5a6', '#2980b9'], ax=axes[1, 0])
axes[1, 0].set_title('Free vs Total Sulfur Dioxide (Preservation Chemistry)', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Total Sulfur Dioxide (mg/dm³)')
axes[1, 0].set_ylabel('Free Sulfur Dioxide (mg/dm³)')

# Sulphates vs Chlorides
sns.scatterplot(data=df, x='chlorides', y='sulphates', hue='good', alpha=0.6,
                palette=['#95a5a6', '#8e44ad'], ax=axes[1, 1])
axes[1, 1].set_title('Sulphates vs Chlorides (Salts & Antimicrobial Balance)', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Chlorides (g/dm³ NaCl)')
axes[1, 1].set_ylabel('Sulphates (g/dm³ potassium sulphate)')

plt.suptitle('Multi-Variable Physicochemical Interactions in Wine Vintages', fontsize=14, fontweight='bold', y=0.99)
plt.tight_layout()
plt.savefig('eda_plots/06_bivariate_interactions.png', dpi=300)
plt.close()

# 8. Print Key Correlation Table
corr_good = corr['good'].sort_values(ascending=False).drop(['good', 'quality'])
corr_qual = corr['quality'].sort_values(ascending=False).drop(['good', 'quality'])
stats_df = pd.DataFrame({
    'Corr_with_Good': corr_good,
    'Corr_with_Quality': corr_qual
})
print("\n" + "="*60)
print("FEATURE SIGNIFICANCE RANKING (CORRELATIONS)")
print("="*60)
print(stats_df)

print("\nEDA completed successfully. All figures saved in 'eda_plots/'.")
