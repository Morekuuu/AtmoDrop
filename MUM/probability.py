import requests
import pandas as pd
import joblib


latitude = 50.58
longitude = 22.05
forecast_horizons = [3, 6, 9, 12]


url = (
    f"https://api.open-meteo.com/v1/gfs?"
    f"latitude={latitude}&longitude={longitude}"
    f"&hourly=precipitation,temperature_2m&timezone=auto"
)
response = requests.get(url)
data = response.json()

forecast_df = pd.DataFrame({
    "time": data["hourly"]["time"],
    "precipitation": data["hourly"]["precipitation"],
    "temperature": data["hourly"]["temperature_2m"]
})
forecast_df["time"] = pd.to_datetime(forecast_df["time"])

now = pd.Timestamp.now().floor("h")
future_times = [now + pd.Timedelta(hours=h) for h in forecast_horizons]

gfs_forecast = {}
gfs_temp = {}
for h, ft in zip(forecast_horizons, future_times):
    row = forecast_df[forecast_df["time"] == ft]
    gfs_forecast[f"tp{h}"] = float(row["precipitation"].values[0]) if not row.empty else 0.0
    gfs_temp[f"temp{h}"] = float(row["temperature"].values[0]) if not row.empty else None

input_data = {
    'A': {
        'tp3': gfs_forecast['tp3'],
        'tp6': gfs_forecast['tp6'],
        'tp9': gfs_forecast['tp9'],
        'tp12': gfs_forecast['tp12'],
    },
    'B': {}
}

csv_path = "daneA.csv"
df_b = pd.read_csv(csv_path)
df_b.columns = df_b.columns.str.strip().str.lower().str.replace('"', '')
df_b = df_b.rename(columns={'hours': 'hour', 'minutes': 'minute'})
latest_b = df_b.iloc[-1]

input_data['B'] = {
    'tp3': float(latest_b['tp3']),
    'tp6': float(latest_b['tp6']),
    'tp9': float(latest_b['tp9']),
    'tp12': float(latest_b['tp12']),
    'hour': int(latest_b['hour']),
    'minute': int(latest_b['minute']),
    'month': int(latest_b['month']),
    'day': int(latest_b['day']),
    'year': int(latest_b['year']),
}

for key in ['hour', 'minute', 'month', 'day']:
    input_data['A'][key] = input_data['B'][key]

targets = ['ir3', 'ir6', 'ir9', 'ir12']
features_map = {
    'ir3': ['tp3', 'hour', 'minute', 'month', 'day'],
    'ir6': ['tp6', 'hour', 'minute', 'month', 'day'],
    'ir9': ['tp9', 'hour', 'minute', 'month', 'day'],
    'ir12': ['tp12', 'hour', 'minute', 'month', 'day'],
}

models = {}
for target in targets:
    try:
        models[target] = joblib.load(f'model_{target}.pkl')
    except:
        print(f" Nie znaleziono modelu: {target}, pomijam.")

print("\n Wyniki – tylko zwycięzca i jego dane wejściowe:")
zwyciestwa = {}

for target in targets:
    if target not in models:
        continue

    model = models[target]
    features = features_map[target]

    row_A = pd.DataFrame([{f: input_data['A'][f] for f in features}])
    row_B = pd.DataFrame([{f: input_data['B'][f] for f in features}])

    pred_A = model.predict(row_A)[0]
    pred_B = model.predict(row_B)[0]

    if pred_A > pred_B:
        wygrany = "A (GFS)"
        zwyciezca = 'A'
    elif pred_B > pred_A:
        wygrany = "B (CSV)"
        zwyciezca = 'B'
    else:
        wygrany = "oba równe"
        zwyciezca = 'A'

    zwyciestwa[target] = input_data[zwyciezca][features[0]]  # tp3, tp6 itd.

    print(f"\n {target} ➜ Bardziej Prawdopodobne: {wygrany}")
    print(" Dane wejściowe bardziej prawdopodbnego:")
    for f in features:
        print(f"  {f}: {input_data[zwyciezca][f]}")

wynik = {
    'year': input_data['B']['year'],
    'month': input_data['B']['month'],
    'day': input_data['B']['day'],
    'hour': input_data['B']['hour'],
    'minute': input_data['B']['minute'],

    'gfs_tp3': input_data['A']['tp3'],
    'gfs_tp6': input_data['A']['tp6'],
    'gfs_tp9': input_data['A']['tp9'],
    'gfs_tp12': input_data['A']['tp12'],

    'gfs_temp3': gfs_temp['temp3'],
    'gfs_temp6': gfs_temp['temp6'],
    'gfs_temp9': gfs_temp['temp9'],
    'gfs_temp12': gfs_temp['temp12'],

    'csv_tp3': input_data['B']['tp3'],
    'csv_tp6': input_data['B']['tp6'],
    'csv_tp9': input_data['B']['tp9'],
    'csv_tp12': input_data['B']['tp12'],
}

for target in targets:
    if target in zwyciestwa:
        wynik[f'best_{target}'] = zwyciestwa[target]

plik_wynikowy = "wyniki.csv"
df_w = pd.DataFrame([wynik])

try:
    df_w.to_csv(plik_wynikowy, mode='a', header=not pd.io.common.file_exists(plik_wynikowy), index=False)
    print(f"\n Wynik zapisany do pliku: {plik_wynikowy}")
except Exception as e:
    print(f" Błąd przy zapisie do CSV: {e}")
