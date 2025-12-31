import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

PLOT_DIR = "static/plots"
os.makedirs(PLOT_DIR, exist_ok=True)

def generate_report(excel_data):
    eda_report = {}

    for sheet, df in excel_data.items():
        report = {}

        # ---------------- BASIC INFO ----------------
        report["rows"] = df.shape[0]
        report["columns"] = df.shape[1]
        report["duplicates"] = int(df.duplicated().sum())
        report["missing"] = df.isnull().sum().to_dict()

        # ---------------- NUMERIC EDA ----------------
        num_df = df.select_dtypes(include="number")
        report["numeric_summary"] = num_df.describe().round(2).to_dict()

        plots = {}

        for col in num_df.columns:
            # Histogram
            plt.figure(figsize=(5,4))
            sns.histplot(num_df[col].dropna(), kde=True)
            path = f"{PLOT_DIR}/{sheet}_{col}_hist.png"
            plt.title(f"{col} Distribution")
            plt.tight_layout()
            plt.savefig(path)
            plt.close()
            plots[f"{col}_hist"] = path

            # Boxplot
            plt.figure(figsize=(5,4))
            sns.boxplot(x=num_df[col])
            path = f"{PLOT_DIR}/{sheet}_{col}_box.png"
            plt.title(f"{col} Boxplot")
            plt.tight_layout()
            plt.savefig(path)
            plt.close()
            plots[f"{col}_box"] = path

        # Correlation Heatmap
        if num_df.shape[1] > 1:
            plt.figure(figsize=(6,5))
            sns.heatmap(num_df.corr(), annot=True, cmap="coolwarm")
            path = f"{PLOT_DIR}/{sheet}_corr.png"
            plt.tight_layout()
            plt.savefig(path)
            plt.close()
            plots["correlation"] = path

        # ---------------- CATEGORICAL EDA ----------------
        cat_df = df.select_dtypes(include="object")

        for col in cat_df.columns:
            top = cat_df[col].value_counts().head(5)

            if len(top) > 1:
                plt.figure(figsize=(5,5))
                top.plot.pie(autopct="%1.1f%%", startangle=90)
                plt.title(f"{col} Distribution")
                plt.ylabel("")
                path = f"{PLOT_DIR}/{sheet}_{col}_pie.png"
                plt.tight_layout()
                plt.savefig(path)
                plt.close()
                plots[f"{col}_pie"] = path

        report["plots"] = plots
        eda_report[sheet] = report

    return eda_report
