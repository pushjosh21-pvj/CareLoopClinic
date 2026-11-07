# coding: utf-8
import pandas as pd
import numpy as np
import requests
df = pd.read_csv(r"C:\Users\CoreX\OneDrive\Desktop\CareLoop Clinics\Data\Clinics.csv")
def get_temp(row):
    url = r"https://api.open-meteo.com/v1/forecast"
    params = {"latitude": 18.5074, "longitude": 73.8077, "hourly": "temperature_2m", "forecast_days": 1}
    params["latitude"] = row["latitude"]
    params["longitude"] = row["longitude"] 
    resp = requests.get(url, params)
    if resp.status_code == 200:
        return resp.json()['hourly']['temperature_2m'][0]
df['temp_c'] = df.apply(get_temp, axis=1)
df.to_csv("clinics_temp.csv", index=False)
