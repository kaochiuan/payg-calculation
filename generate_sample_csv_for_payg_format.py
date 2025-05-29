# csv file contains the following 6 columns:
# uuid:str, device_id:str, org_id:str, time:date, pro:boolean, gsp:boolean
# time field is a datetime string in the format "YYYY-MM-DD"
# generate sample csv file

import pandas as pd
import random
import uuid
import datetime
import csv
import json
from datetime import timedelta

# Define date range (end_date is the last day of the last month, start_date is the first day of the month)
end_date = datetime.date(2025, 4, 1)
start_date = datetime.date(2025, 3, 14)

# List of supported GSP models
support_gsp_models = ["ATP100", "ATP100W", "ATP200", "ATP500", "ATP700", "ATP800", "USG FLEX 100", "USG FLEX 100AX", "USG FLEX 100H", "USG FLEX 100HP",
                      "USG FLEX 100W", "USG FLEX 200", "USG FLEX 200H", "USG FLEX 200HP", "USG FLEX 500", "USG FLEX 500H", "USG FLEX 50H", "USG FLEX 50HP", "USG FLEX 700", "USG FLEX 700H"]


def random_date(start, end):
    """Generate a random date between start and end dates"""
    time_between_dates = end - start
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start + timedelta(days=random_number_of_days)
    return random_date.strftime('%Y-%m-%d')


def generate_sample_csv():
    with open('sample_payg.json', 'r') as f:
        sample_data = json.load(f)

    with open('sample_payg.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["uuid", "device_id", "org_id", "time", "pro", "gsp"])

        # Iterate through organizations and devices
        for org in sample_data['org_info']:
            org_id = org['id']
            payg_mode = org['payg_mode']
            for device in org['devices']:  # Iterate through device objects
                device_id = device['id']   # Access the 'id' field
                is_support_gsp = device['is_support_gsp']
                used_dates = set()
                # Generate 18 rows of sample data for each device
                if not is_support_gsp:
                    gsp = False
                else:
                    if payg_mode == "pro":
                        gsp = False
                    elif payg_mode == "gsp":
                        gsp = True
                    else:
                        # Default case if payg_mode is neither "pro" nor "gsp"
                        # Or handle as an error, depending on expected data integrity
                        gsp = False
                for i in range(18):
                    # Generate random date in the format YYYY-MM-DD
                    while True:
                        random_time = random_date(start_date, end_date)
                        if random_time not in used_dates:
                            used_dates.add(random_time)
                            break
                    writer.writerow(
                        [str(uuid.uuid4()), device_id, org_id, random_time, True, gsp])


if __name__ == "__main__":
    generate_sample_csv()
    print("Sample CSV file generated.")
