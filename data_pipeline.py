import csv
import json

FILE_PATH = r"./Data/Appointments.csv"


def parse_row(row):
    row["age"] = int(row["age"])
    row["fee_inr"] = int(row["fee_inr"])
    row["prior_no_shows"] = int(row["prior_no_shows"])
    row["distance_km"] = float(row["distance_km"])
    return row


with open(FILE_PATH, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    print("Headers: ", reader.fieldnames)
    n = 0
    for row in reader:
        n += 1
        accepted_rows = []
        rejected_rows = []

        try:
            accepted_rows.append(parse_row(row))
        except ValueError:
            rejected_rows.append(row)

    print("No of rows are: ", n)
    print("No of rejected rows", len(rejected_rows))

with open(r"./Data/rejected_rows.json", "w") as file:
    json.dump(rejected_rows, file, indent=2)




"""
Using only the csv module (not pandas): open appointments.csv with with open(..., newline=""), read it with csv.DictReader, and print the header and row count. Write a function parse_row(row) that converts age, fee_inr and prior_no_shows to int and distance_km to float, returning the converted dictionary. Loop over every row; use try/except ValueError to put rows that fail into a rejected list and the rest into an accepted list. Save rejected with json.dump(..., indent=2) as rejected_rows.json.
"""
