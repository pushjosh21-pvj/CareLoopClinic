import csv
import json

FILE_PATH = r"..\Data\Appointments.csv"
#FILE_PATH = r"./Data/Appointments.csv"


def parse_row(row):
    print('age', row['age'])
    if row['age'].strip() == "" or row['age'] is None:
        raise ValueError("Age is blank")
    elif int(row['age']) <= 0:
        raise ValueError("Age is zero or negative")
    elif int(row['age']) > 110:
        raise ValueError("Age can not be greater than 110")
    elif row['fee_inr'].strip() == '' or row['fee_inr'] is None:
        raise ValueError("fee_inr is blank")
    elif row['prior_no_shows'].strip() == '' or row['prior_no_shows'] is None:
        raise ValueError("prior_no_show is blank")
    elif row['distance_km'].strip() == '' or row['distance_km'] is None:
        raise ValueError("distance_km is blank")
    else :
        row["age"] = int(row["age"])
        row["fee_inr"] = int(row["fee_inr"])
        row["prior_no_shows"] = int(row["prior_no_shows"])
        row["distance_km"] = float(row["distance_km"])
    return row


with open(FILE_PATH, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    print("Headers: ", reader.fieldnames)
    n = 0
    accepted_rows = []
    rejected_rows = []
    for row in reader:
        n += 1
        try:
            accepted_rows.append(parse_row(row))
        except ValueError as e:
            row['error'] = str(e)
            rejected_rows.append(row)

    print("No of rows are: ", n)
    print("No of rejected rows", len(rejected_rows))

with open(r"../Data/rejected_rows.json", "w") as f1, open(r"../Data/accepted_rows.json", "w") as f2:
    json.dump(rejected_rows, f1, indent=2)
    json.dump(accepted_rows, f2, indent=2)




"""
Using only the csv module (not pandas): 
open appointments.csv with with open(..., newline=""), 
read it with csv.DictReader, and print the header and row count. 
Write a function parse_row(row) that converts age, fee_inr and prior_no_shows to int and distance_km to float, 
returning the converted dictionary. Loop over every row; use try/except ValueError to put rows that fail into a rejected list and the rest into an accepted list. Save rejected with json.dump(..., indent=2) as rejected_rows.json.
"""
