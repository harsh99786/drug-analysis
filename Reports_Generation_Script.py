import psycopg2
import pandas as pd
import os
from datetime import datetime

# ============================================================
#  CONFIGURATION — update these values
# ============================================================

DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "database": "Clinical_Trial",   
    "user":     "postgres",
    "password": "387162"          
}

# Folder where CSV files will be saved
# Power BI will point to this folder
OUTPUT_FOLDER = "/Users/manat/Desktop/projects/ClinicalTrialData/Reports"  

# Reporting views to export
VIEWS = [
    "reporting.rpt_protocol_summary",
    "reporting.rpt_protocols_by_status",
    "reporting.rpt_protocols_by_sponsor",
    "reporting.rpt_protocols_by_condition",
    "reporting.rpt_protocols_by_population",
    "reporting.rpt_top_manufacturers",
]

# ============================================================
#  SCRIPT — no need to change anything below this line
# ============================================================

def create_output_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created folder: {folder}")
    else:
        print(f"Folder exists: {folder}")


def connect_db(config):
    try:
        conn = psycopg2.connect(**config)
        print("Connected to PostgreSQL successfully.\n")
        return conn
    except Exception as e:
        print(f"Connection failed: {e}")
        raise


def export_view_to_csv(conn, view_name, output_folder):
    try:
        # Read view into dataframe
        df = pd.read_sql(f"SELECT * FROM {view_name}", conn)

        # Build file name from view name  e.g. rpt_protocol_summary.csv
        file_name = view_name.split(".")[-1] + ".csv"
        file_path = os.path.join(output_folder, file_name)

        # Save to CSV
        df.to_csv(file_path, index=False)

        print(f"  Exported {view_name}")
        print(f"    Rows : {len(df)}")
        print(f"    File : {file_path}\n")

    except Exception as e:
        print(f"  Failed to export {view_name}: {e}\n")


def write_log(output_folder, views):
    log_path = os.path.join(output_folder, "_last_refresh.txt")
    with open(log_path, "w") as f:
        f.write(f"Last refreshed : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Views exported : {len(views)}\n\n")
        for v in views:
            f.write(f"  - {v}\n")
    print(f"Log written to: {log_path}")


def main():
    print("=" * 50)
    print("  Drug Protocol Analytics — CSV Export")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50 + "\n")

    create_output_folder(OUTPUT_FOLDER)

    conn = connect_db(DB_CONFIG)

    print("Exporting reporting views...\n")
    for view in VIEWS:
        export_view_to_csv(conn, view, OUTPUT_FOLDER)

    conn.close()

    write_log(OUTPUT_FOLDER, VIEWS)

    print("\nAll done! Open Power BI and refresh to see latest data.")


if __name__ == "__main__":
    main()
