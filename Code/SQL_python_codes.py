import csv

clinic_file = r"C:\Users\CoreX\OneDrive\Desktop\CareLoop Clinics\Data\clinics_temp.csv"
appoint_file = r"C:\Users\CoreX\OneDrive\Desktop\CareLoop Clinics\Data\appointments_clean.csv"

#For creating query of inserting clinics 
with open(clinic_file, newline="", encoding='utf-8') as file:
    reader = csv.DictReader(file)
    db_command = []
    header = reader.fieldnames
    for row in reader:
        formatted_values = []
        for value in row.values():
            if value.replace(".","").isdigit():
                formatted_values.append(str(value))
            else:
                formatted_values.append(f"'{value}'")
        db_command.append(f"({', '.join(formatted_values)})")
    db_values = ", \n".join(db_command)
print(f'INSERT INTO clinics {"(" + ", ".join(header) + ")"} VALUES {db_values}')


#for creating query for inserting appointment records 
with open(appoint_file, newline="", encoding='utf-8') as file:
    reader = csv.DictReader(file)
    db_command = []
    header = reader.fieldnames
    for row in reader:
        formatted_values = []
        for value in row.values():
            if value.replace(".","").isdigit():
                formatted_values.append(str(value))
            else:
                formatted_values.append(f"'{value}'")
        db_command.append(f"({', '.join(formatted_values)})")
    db_values = ", \n".join(db_command)
print(f'INSERT INTO appointments {"(" + ", ".join(header) + ")"} VALUES {db_values}')