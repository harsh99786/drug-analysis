from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import psycopg2.extras
import os

app = FastAPI(title="Drug Protocol Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "your_database_name"),
    "user":     os.getenv("DB_USER", "powerbi_reader"),
    "password": os.getenv("DB_PASSWORD", "ChangeMe123!"),
}

def get_data(query):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/api/summary")
def protocol_summary():
    return get_data('SELECT * FROM reporting.rpt_protocol_summary LIMIT 100')

@app.get("/api/by-status")
def by_status():
    return get_data('SELECT * FROM reporting.rpt_protocols_by_status ORDER BY "Total Protocols" DESC')

@app.get("/api/by-sponsor")
def by_sponsor():
    return get_data('SELECT * FROM reporting.rpt_protocols_by_sponsor ORDER BY "Total Protocols" DESC')

@app.get("/api/by-condition")
def by_condition():
    return get_data('SELECT * FROM reporting.rpt_protocols_by_condition ORDER BY "Protocol Count" DESC')

@app.get("/api/by-population")
def by_population():
    return get_data('SELECT * FROM reporting.rpt_protocols_by_population ORDER BY "Protocol Count" DESC')

@app.get("/api/top-manufacturers")
def top_manufacturers():
    return get_data('SELECT * FROM reporting.rpt_top_manufacturers')

@app.get("/api/kpis")
def kpis():
    data = get_data('''
        SELECT
            (SELECT COUNT(*) FROM reporting.rpt_protocol_summary)         AS total_protocols,
            (SELECT COUNT(DISTINCT "Sponsor") FROM reporting.rpt_protocol_summary) AS total_sponsors,
            (SELECT COUNT(DISTINCT "Brand Name") FROM reporting.rpt_protocol_summary) AS total_brands,
            (SELECT COUNT(*) FROM reporting.rpt_protocols_by_condition)   AS total_conditions
    ''')
    return data[0]