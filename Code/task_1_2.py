import numpy as np
import pandas as pd

FILE_PATH = r"../Data/Appointments.csv"

#printing the dataframe information
df = pd.read_csv(FILE_PATH)
print("appointment dataframe information : ")
print(df.info())
print('Rows with null values are : ', df.isna().sum())
print('Rows with duplicate values are : ', df.duplicated().sum())

#cleaning 
print('Total Rows : ', df.shape[0])
df = df.drop_duplicates()
print('Remaining Rows after removing duplicates : ', df.shape[0])
df['booking_channel'] =  df['booking_channel'].str.strip().str.title()
df['appt_date'] = pd.to_datetime(df['appt_date'], errors='coerce')
df['booked_on'] = pd.to_datetime(df['booked_on'], errors='coerce')
df = df.dropna(subset=['appt_date', 'status'])
print('Remaining Rows after removing null values : ', df.shape[0])

#removing the invalid age values 
df.loc[(df['age'] < 1) | (df['age'] > 100), 'age'] = np.nan
print('Invalid ages are', df['age'].isna().sum())
df['age'] = df['age'].fillna(df['age'].median().round().astype('int'))
df['distance_km'] = df['distance_km'].fillna(df['distance_km'].median())
df['fee_inr'] = df['fee_inr'].fillna(df['fee_inr'].median())

#calculating Q1, Q3 for distance_km and fee_inr
Q1_fee = df['fee_inr'].quantile(0.25)
Q3_fee = df['fee_inr'].quantile(0.75)
IQR_fee = Q3_fee - Q1_fee
#print(Q1_fee, Q3_fee)
Q1_distance = df['distance_km'].quantile(0.25)
Q3_distance = df['distance_km'].quantile(0.75)
IQR_distance = Q3_distance - Q1_distance
#print(Q1_distance, Q3_distance)

#clipping both the data 
print("Number of rows being clipped are : ")
print('distance_km : ',len(df[(df['distance_km'] < Q1_distance - 1.5 * IQR_distance) | (df['distance_km'] > Q3_distance + 1.5 * IQR_distance)]))
print('fee_inr : ',len(df[(df['fee_inr'] < Q1_fee - 1.5 * IQR_fee) | (df['fee_inr'] > Q3_fee + 1.5 * IQR_fee)]))
df['distance_km'] = np.clip(df['distance_km'], Q1_distance - 1.5 * IQR_distance, Q3_distance + 1.5 * IQR_distance)
df['fee_inr'] = np.clip(df['fee_inr'], Q1_fee - 1.5 * IQR_fee, Q3_fee + 1.5 * IQR_fee)

#applying round 
df['distance_km'] = df['distance_km'].round(1)
df['fee_inr'] = df['fee_inr'].round().astype('int')

