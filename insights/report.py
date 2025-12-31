import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew, kurtosis

# Directory for saving plots
PLOT_DIR = "static/plots"
os.makedirs(PLOT_DIR, exist_ok=True)

def generate_plots(df, sheet_name):
    """Generate histograms, boxplots, correlation heatmap."""
    plots = {}
    numeric_cols = df.select_dtypes(include="number")
    
    if numeric_cols.empty:
        return plots
    
    # Histogram & Boxplot
    for col in numeric_cols.columns:
        # Histogram
        plt.figure(figsize=(4,3))
        sns.histplot(numeric_cols[col].dropna(), kde=True, color='skyblue')
        plt.title(f"{col} Distribution")
        hist_path = f"{PLOT_DIR}/{sheet_name}_{col}_hist.png"
        plt.tight_layout()
        plt.savefig(hist_path)
        plt.close()
        plots[f"{col}_hist"] = hist_path

        # Boxplot
        plt.figure(figsize=(4,3))
        sns.boxplot(x=numeric_cols[col], color='salmon')
        plt.title(f"{col} Boxplot")
        box_path = f"{PLOT_DIR}/{sheet_name}_{col}_box.png"
        plt.tight_layout()
        plt.savefig(box_path)
        plt.close()
        plots[f"{col}_box"] = box_path

    # Correlation heatmap
    if len(numeric_cols.columns) > 1:
        plt.figure(figsize=(6,5))
        sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', fmt=".2f")
        heatmap_path = f"{PLOT_DIR}/{sheet_name}_corr.png"
        plt.tight_layout()
        plt.savefig(heatmap_path)
        plt.close()
        plots["correlation_heatmap"] = heatmap_path

    return plots

def detect_outliers(df):
    """Detect outliers using IQR method for numeric columns."""
    numeric_cols = df.select_dtypes(include="number")
    outliers = {}
    for col in numeric_cols.columns:
        Q1 = numeric_cols[col].quantile(0.25)
        Q3 = numeric_cols[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers[col] = int(((numeric_cols[col] < Q1 - 1.5*IQR) | (numeric_cols[col] > Q3 + 1.5*IQR)).sum())
    return outliers

def generate_report(excel_data: dict):
    """Generate full EDA for all sheets in the Excel file."""
    eda_report = {}
    
    for sheet_name, df in excel_data.items():
        report = {}

        # Basic info
        report["rows"] = df.shape[0]
        report["columns"] = df.shape[1]
        report["memory_usage"] = f"{round(df.memory_usage(deep=True).sum()/1024**2,2)} MB"
        report["duplicates"] = int(df.duplicated().sum())
        report["dtypes"] = df.dtypes.apply(lambda x: str(x)).to_dict()

        # Sample rows
        report["sample"] = df.head(5).to_dict(orient="records")

        # Missing values
        report["missing_values"] = df.isnull().sum().to_dict()
        report["missing_percentage"] = (df.isnull().mean()*100).round(2).to_dict()

        # Numeric summary
        numeric_cols = df.select_dtypes(include="number")
        report["summary_numeric"] = numeric_cols.describe().to_dict() if not numeric_cols.empty else {}

        # Skewness & Kurtosis
        skewness = {col: float(skew(numeric_cols[col].dropna())) for col in numeric_cols.columns} if not numeric_cols.empty else {}
        kurt = {col: float(kurtosis(numeric_cols[col].dropna())) for col in numeric_cols.columns} if not numeric_cols.empty else {}
        report["skewness"] = skewness
        report["kurtosis"] = kurt

        # Categorical summary
        categorical_cols = df.select_dtypes(include="object")
        report["summary_categorical"] = categorical_cols.describe().to_dict() if not categorical_cols.empty else {}

        # Correlation
        report["correlation"] = numeric_cols.corr().to_dict() if len(numeric_cols.columns) > 1 else {}

        # Outliers
        report["outliers"] = detect_outliers(df)

        # Plots
        report["plots"] = generate_plots(df, sheet_name)

        # Add to main report
        eda_report[sheet_name] = report

    return eda_report
