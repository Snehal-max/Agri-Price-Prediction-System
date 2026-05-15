import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
dataset = pd.read_csv('data.csv')
dataset['target_week1'] = (dataset.groupby(['Commodity', 'Market'])['Modal_Price'].shift(-3))
dataset = dataset.dropna()
X = dataset[['Commodity','Market','Arrival_Qty_qtl','Rainfall_mm','Modal_Price']]
y = dataset['target_week1']
train = dataset[dataset['Date'] < '2024-01-01']
test = dataset[dataset['Date'] >= '2024-01-01']
X_train = train[['Commodity','Market','Arrival_Qty_qtl','Rainfall_mm','Modal_Price']]
y_train = train['target_week1']
X_test = test[['Commodity','Market','Arrival_Qty_qtl','Rainfall_mm','Modal_Price']]
y_test = test['target_week1']
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), ['Commodity', 'Market'])],remainder='passthrough')
X_train = ct.fit_transform(X_train)
X_test = ct.transform(X_test)
from sklearn.ensemble import RandomForestRegressor
model_week3 = RandomForestRegressor(
    n_estimators=10,
    random_state=0
)
model_week3.fit(X_train, y_train)
y_pred = model_week3.predict(X_test)
import pickle

pickle.dump(model_week3, open('model_week3.pkl', 'wb'))

print("Week 3 model saved!")