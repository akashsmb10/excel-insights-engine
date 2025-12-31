from flask import Flask, request, render_template, jsonify
import pandas as pd
from insights.report import generate_report

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/upload-excel", methods=["POST"])
def upload_excel():
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]

    # Read Excel
    excel_data = pd.read_excel(file, sheet_name=None, engine="openpyxl")

    # Generate EDA
    report = generate_report(excel_data)

    # Render HTML
    return render_template(
        "result.html",
        eda=report
    )

if __name__ == "__main__":
    app.run()
