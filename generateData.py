import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# -----------------------------
# CONFIGURATION
# -----------------------------
num_records = 2500
num_employees = 60

departments = ["HR", "IT", "Finance", "Operations", "Sales"]
shift_types = ["Morning", "Evening"]
locations = ["Office", "Remote"]
attendance_statuses = ["Present", "Absent", "Late", "Work From Home"]

# -----------------------------
# GENERATE EMPLOYEE MASTER DATA
# -----------------------------
employee_ids = [f"E{1000+i}" for i in range(num_employees)]
employee_names = [f"Employee_{i}" for i in range(num_employees)]

employee_data = list(zip(employee_ids, employee_names))

# -----------------------------
# GENERATE RANDOM DATES
# -----------------------------
start_date = datetime(2024, 1, 1)
date_list = [start_date + timedelta(days=i) for i in range(90)]

data = []

for _ in range(num_records):
    emp_id, emp_name = random.choice(employee_data)
    dept = random.choice(departments)
    shift = random.choice(shift_types)
    location = random.choice(locations)
    status = random.choice(attendance_statuses)
    date = random.choice(date_list)

    # Intentionally mix date formats
    date_formats = [
        date.strftime("%Y-%m-%d"),
        date.strftime("%d/%m/%Y"),
        date.strftime("%m-%d-%Y")
    ]
    mixed_date = random.choice(date_formats)

    # Generate check-in and check-out times
    if status == "Absent":
        check_in = ""
        check_out = ""
    else:
        hour_in = random.randint(8, 11)
        minute_in = random.randint(0, 59)
        check_in = f"{hour_in}:{minute_in}"

        hour_out = random.randint(16, 20)
        minute_out = random.randint(0, 59)
        check_out = f"{hour_out}:{minute_out}"

    data.append([
        emp_id,
        emp_name,
        dept,
        mixed_date,
        check_in,
        check_out,
        status,
        shift,
        location
    ])

columns = [
    "Employee_ID",
    "Employee_Name",
    "Department",
    "Attendance_Date",
    "Check_In_Time",
    "Check_Out_Time",
    "Attendance_Status",
    "Shift_Type",
    "Location"
]

df = pd.DataFrame(data, columns=columns)

# -----------------------------
# INTRODUCE DATA QUALITY ISSUES
# -----------------------------

# Add extra spaces randomly
df.loc[df.sample(frac=0.05).index, "Department"] = df["Department"] + "  "

# Lowercase random rows
df.loc[df.sample(frac=0.05).index, "Attendance_Status"] = df["Attendance_Status"].str.lower()

# Insert missing values
df.loc[df.sample(frac=0.03).index, "Attendance_Status"] = np.nan

# Duplicate some rows
duplicates = df.sample(frac=0.03)
df = pd.concat([df, duplicates], ignore_index=True)

# -----------------------------
# EXPORT TO CSV
# -----------------------------
df.to_csv("attendance_raw_dataset.csv", index=False)

print("Dataset generated successfully!")
print("File saved as attendance_raw_dataset.csv")
print("Total records:", len(df))