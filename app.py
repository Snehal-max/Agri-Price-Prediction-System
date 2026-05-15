import streamlit as st
import pandas as pd
import pickle
import numpy as np
import requests
from datetime import date, timedelta

market_coords = {
    'Agra APMC':     (27.1767, 78.0081),
    'Bhopal APMC':   (23.2599, 77.4126),
    'Cuttack Main':  (20.4625, 85.8830),
    'Indore Mandi':  (22.7196, 75.8577),
    'Lucknow Mandi': (26.8467, 80.9462),
    'Mysuru APMC':   (12.2958, 76.6394),
    'Nagpur Main':   (21.1458, 79.0882),
    'Nashik APMC':   (19.9975, 73.7898),
    'Pune Main':     (18.5204, 73.8567),
    'Unit-4 Market': (20.2961, 85.8245),  # Bhubaneswar
    'Yeshwanthpur':  (13.0227, 77.5551),  # Bangalore
}

def get_rainfall(lat, lon, target_date):
    today = date.today()
    days_ahead = (target_date - today).days
 
    if days_ahead <= 14:

        if days_ahead >= 0:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": lat,
                "longitude": lon,
                "daily": "precipitation_sum",
                "forecast_days": min(days_ahead + 1, 14),
                "timezone": "Asia/Kolkata"
            }
        else:
            url = "https://archive-api.open-meteo.com/v1/archive"
            params = {
                "latitude": lat,
                "longitude": lon,
                "daily": "precipitation_sum",
                "start_date": target_date.strftime("%Y-%m-%d"),
                "end_date": target_date.strftime("%Y-%m-%d"),
                "timezone": "Asia/Kolkata"
            }
 
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            daily = data.get("daily", {})
            precip = daily.get("precipitation_sum", [])
 
            if days_ahead >= 0 and precip:
                return round(precip[-1] or 0.0, 2)  # last forecasted day
            elif precip:
                return round(precip[0] or 0.0, 2)
        except Exception:
            pass  
 
    return None  
 

dataset = pd.read_csv('data.csv')
dataset['Date'] = pd.to_datetime(dataset['Date'])
dataset['Month'] = dataset['Date'].dt.month

model_week1 = pickle.load(open('model_week1.pkl', 'rb'))
model_week2 = pickle.load(open('model_week2.pkl', 'rb'))
model_week3 = pickle.load(open('model_week3.pkl', 'rb'))
model_week4 = pickle.load(open('model_week4.pkl', 'rb'))
 

ct = pickle.load(open('encoder.pkl', 'rb'))
 

st.title("🌾 Agri Price Prediction System")
st.write("Predict future crop prices and get the best selling recommendation.")

commodity_list = sorted(dataset['Commodity'].unique())
market_list    = sorted(dataset['Market'].unique())
 
commodity    = st.selectbox("Select Commodity", commodity_list)
market       = st.selectbox("Select Market", market_list)
harvest_date = st.date_input("Harvest Date")
 

if st.button("Predict Prices"):
 
    filtered = dataset[
        (dataset['Commodity'] == commodity) &
        (dataset['Market']    == market)
    ]
 
    if filtered.empty:
        st.error("No data available for selected Commodity and Market.")
 
    else:
        lat, lon = market_coords.get(market, (20.5937, 78.9629))  
        with st.spinner("Fetching rainfall data..."):
            rainfall = get_rainfall(lat, lon, harvest_date)
 
        if rainfall is None:
            month = harvest_date.month
            monthly_avg = filtered[filtered['Month'] == month]['Rainfall_mm'].mean()
            rainfall = round(monthly_avg if not np.isnan(monthly_avg) else filtered['Rainfall_mm'].mean(), 2)
            st.info(f"Using historical average rainfall for this month: {rainfall} mm")
        else:
            st.info(f"Rainfall fetched for {harvest_date}: {rainfall} mm")
 
        filtered = filtered.copy()
        filtered['date_diff'] = (filtered['Date'] - pd.Timestamp(harvest_date)).abs()
        closest_row = filtered.loc[filtered['date_diff'].idxmin()]
 
        arrival_qty  = closest_row['Arrival_Qty_qtl']
        modal_price  = closest_row['Modal_Price']
 
        
        input_df = pd.DataFrame({
            'Commodity':       [commodity],
            'Market':          [market],
            'Arrival_Qty_qtl': [arrival_qty],
            'Rainfall_mm':     [rainfall],
            'Modal_Price':     [modal_price]
        })
 
       
        input_encoded = ct.transform(input_df)
 
        pred1 = model_week1.predict(input_encoded)[0]
        pred2 = model_week2.predict(input_encoded)[0]
        pred3 = model_week3.predict(input_encoded)[0]
        pred4 = model_week4.predict(input_encoded)[0]
 
        predictions = [pred1, pred2, pred3, pred4]
        best_week   = np.argmax(predictions) + 1
        best_price  = max(predictions)
        gain        = ((best_price - pred1) / pred1) * 100
 
        def label(price, max_price):
            if price >= 0.9 * max_price:
                return "🟢 Good"
            elif price >= 0.7 * max_price:
                return "🟡 Average"
            else:
                return "🔴 Low"
 

        st.subheader("📈 Predicted Prices")
        st.write(f"Week 1: ₹{pred1/100:.2f}/kg  {label(pred1, best_price)}")
        st.write(f"Week 2: ₹{pred2/100:.2f}/kg  {label(pred2, best_price)}")
        st.write(f"Week 3: ₹{pred3/100:.2f}/kg  {label(pred3, best_price)}")
        st.write(f"Week 4: ₹{pred4/100:.2f}/kg  {label(pred4, best_price)}")
 
        st.success(
            f"Recommendation: Wait until Week {best_week} — expected {gain:.1f}% higher return"
        )
