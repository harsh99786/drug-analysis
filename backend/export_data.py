import psycopg2
import pandas as pd
import os
from datetime import datetime

# ── CONFIG ─────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "database": "Clinical_Trial",   # <-- change this
    "user":     "powerbi_reader",
    "password": "ChangeMe123!"          # <-- change this
}

OUTPUT_FOLDER = "frontend/data"

VIEWS = {
    "kpis": """
        SELECT
            (SELECT COUNT(*)                    FROM reporting.rpt_protocol_summary)    AS total_protocols,
            (SELECT COUNT(DISTINCT "Sponsor")   FROM reporting.rpt_protocols_by_sponsor) AS total_sponsors,
            (SELECT COUNT(DISTINCT "Brand Name") FROM reporting.rpt_protocol_summary)   AS total_brands,
            (SELECT COUNT(*)                    FROM reporting.rpt_protocols_by_condition) AS total_conditions
    """,
    "rpt_protocol_summary":         'SELECT * FROM reporting.rpt_protocol_summary',
    "rpt_protocols_by_status":      'SELECT * FROM reporting.rpt_protocols_by_status ORDER BY "Total Protocols" DESC',
    "rpt_protocols_by_sponsor":     'SELECT * FROM reporting.rpt_protocols_by_sponsor ORDER BY "Total Protocols" DESC',
    "rpt_protocols_by_condition":   'SELECT * FROM reporting.rpt_protocols_by_condition ORDER BY "Protocol Count" DESC',
    "rpt_protocols_by_population":  'SELECT * FROM reporting.rpt_protocols_by_population ORDER BY "Protocol Count" DESC',
    "rpt_top_manufacturers":        'SELECT * FROM reporting.rpt_top_manufacturers',
}

def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    print("=" * 50)
    print("  Drug Protocol — CSV Export")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    conn = psycopg2.connect(**DB_CONFIG)
    print("Connected to PostgreSQL\n")

    for name, query in VIEWS.items():
        df = pd.read_sql(query, conn)
        path = os.path.join(OUTPUT_FOLDER, f"{name}.csv")
        df.to_csv(path, index=False)
        print(f"  Saved {name}.csv  ({len(df)} rows)")

    conn.close()

    # Write last refresh timestamp
    with open(os.path.join(OUTPUT_FOLDER, "last_refresh.txt"), "w") as f:
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    print("\nAll CSVs saved to frontend/data/")
    print("\nNext steps:")
    print("  git add .")
    print("  git commit -m 'update data'")
    print("  git push origin main")

if __name__ == "__main__":
    main()