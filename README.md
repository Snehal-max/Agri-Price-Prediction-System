# Agri Price Prediction System
 
An AI-powered crop price forecasting system that helps farmers make smarter selling decisions by predicting market prices up to 4 weeks ahead.
 
---
 
## Live Demo
[Click here to open the vdo](https://anonmp4.help/v/kBq1r7hoFLgWdPa)
 
---
 
## Problem Statement
Indian farmers lose **20-30% of potential income** due to poor market timing. With over 7,000 APMCs across India, price volatility driven by seasonal demand, rainfall, and arrival quantities makes it nearly impossible for smallholder farmers to decide **when** and **where** to sell their produce.
 
---
 
## Solution
A **Random Forest-based multi-model prediction engine** that forecasts crop modal prices for **Weeks 1 through 4** ahead of harvest. The system uses:
- Commodity type & market location
- Arrival quantity
- Real-time/historical rainfall data (via Open-Meteo API)
- Current modal price
---
 
## How It Works
 
```
Harvest Date → Weather API → Rainfall → ML Model → Price Prediction
```
 
1. User selects **Commodity**, **Market**, and **Harvest Date**
2. System fetches **real rainfall** from Open-Meteo API
   - Past/near dates → Live API data
   - Beyond 14 days → Historical monthly average from dataset
3. Four **Random Forest models** predict prices for Week 1, 2, 3, 4
4. App recommends the **best week to sell** with expected % gain
---
 
## Features
 
| Feature | Description |
|---------|-------------|
| 4-Week Forecast | Separate model per week for higher accuracy |
| Rainfall-Aware | Incorporates real rainfall as a price driver |
| Market-Specific | Predictions scoped to individual APMC markets |
| Sell Recommendation | Highlights best week with % gain estimate |
| Simple UI | Streamlit app — no technical knowledge needed |
 
---
 
## Project Structure
 
```
AXILLA Final/
│
├── app.py              # Main Streamlit application
├── Week1.py            # Model training script - Week 1
├── Week2.py            # Model training script - Week 2
├── Week3.py            # Model training script - Week 3
├── Week4.py            # Model training script - Week 4
├── requirements.txt    # Python dependencies
├── Poster/
│   └── Project.py      # Poster generation script
└── README.md
```
 
> `data.csv` and `.pkl` model files are not included in this repo due to size limits.
 
---
 
## Setup Instructions
 
### 1. Clone the repository
```bash
git clone https://github.com/Snehal-max/Agri-Price-Prediction-System.git
cd Agri-Price-Prediction-System
```
 
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
 
### 3. Download the dataset
Download `data.csv` from the root folder.
 
### 4. Train the models
```bash
python Week1.py
python Week2.py
python Week3.py
python Week4.py
```
 
### 5. Run the app
```bash
streamlit run app.py
```
 
---
 
## Requirements
 
```
streamlit
pandas
numpy
scikit-learn
requests
matplotlib
```
 
---
 
## Markets Covered
 
| Market | Location |
|--------|----------|
| Agra APMC | Uttar Pradesh |
| Bhopal APMC | Madhya Pradesh |
| Cuttack Main | Odisha |
| Indore Mandi | Madhya Pradesh |
| Lucknow Mandi | Uttar Pradesh |
| Mysuru APMC | Karnataka |
| Nagpur Main | Maharashtra |
| Nashik APMC | Maharashtra |
| Pune Main | Maharashtra |
| Unit-4 Market | Odisha |
| Yeshwanthpur | Karnataka |
 
---
 
## Team
 
**Team AXILLA**
---
 
## Expected Impact
 
- **15-25%** income increase for smallholder farmers
- **7,000+** APMCs scalable to
- **4 weeks** forecast horizon
- Reduces dependence on middlemen
---
 
## Innovation Poster
 
![Poster](AXILLA_IITKharagpur_SRM_AgriPricePredictionSystem.pdf)
 
---

## Power Point Presentation 
 
![PPT](AXILLA_KisanPrice_Ideathon2026.pptx)
 
---
 
*Built with ❤️ for farmers of India 🇮🇳*
