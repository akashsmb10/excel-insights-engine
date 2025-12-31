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
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    excel_data = pd.read_excel(
        file,
        sheet_name=None,
        engine="openpyxl"
    )

    eda_result = generate_report(excel_data)

    return render_template(
        "result.html",
        eda=eda_result
    )

if __name__ == "__main__":
    app.run(debug=True)
