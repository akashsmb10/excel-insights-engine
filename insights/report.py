def generate_report(excel_data):
    report = {}

    for sheet, df in excel_data.items():
        report[sheet] = {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "missing_values": df.isnull().sum().to_dict(),
            "summary": df.describe(include="all").to_dict()
        }

    return report
