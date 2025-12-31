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
    excel_data = pd.read_excel(file, sheet_name=None)
    report = generate_report(excel_data)

    return jsonify(report)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
