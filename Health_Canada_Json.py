import csv

import requests
import pandas as pd

keywords = [
    "medicalcondition",
    "drugproduct",
    "sponsor",
    "studypopulation",
    "status",
    "protocol"
]

base_url = "https://health-products-dev.hres.ca/api/clinical-trial/{}/?lang=en&type=json"

for keyword in keywords:
    try:
        # Build URL dynamically
        url = base_url.format(keyword)

        # Fetch data
        response = requests.get(url, timeout=60)
        response.raise_for_status()

        data = response.json()


        # Convert to DataFrame
        df = pd.json_normalize(data)

        # Save CSV
        filename = f"{keyword}.csv"
        df.to_csv(filename, index=False)

        print(f"Saved: {filename}")

    except Exception as e:
        print(f"Failed for {keyword}: {e}") 