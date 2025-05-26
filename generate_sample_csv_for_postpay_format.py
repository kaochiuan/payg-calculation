# csv file contains the following 4 columns:
# device_id:str, organization_id:str, date:date, create_at:timestamp
# date field is a datetime string in the format "YYYY-MM-DD"
# timestamp field is a unix timestamp in milliseconds
# generate sample csv file

import pandas as pd
import random
import uuid
import datetime
import csv
import json
from datetime import timedelta

# Define date range (end_date is the last day of the last month, start_date is the first day of the month)
end_date = datetime.date(2025, 3, 14)
start_date = datetime.date(2025, 3, 1)

def random_date(start, end):
    """Generate a random date between start and end dates"""
    time_between_dates = end - start
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start + timedelta(days=random_number_of_days)
    return random_date.strftime('%Y-%m-%d')

def generate_sample_csv():
    with open('sample_postpay.json', 'r') as f:
        sample_data = json.load(f)

    with open('sample_postpay.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["device_id", "organization_id", "date", "create_at"])

        # Iterate through organizations and devices
        for org in sample_data['org_info']:
            org_id = org['id']
            for device_id in org['devices']:
                used_dates = set()
                # Generate 13 rows of sample data for each device
                gsp = random.choice([True, False])
                for i in range(13):
                    # Generate random date in the format YYYY-MM-DD
                    while True:
                        random_time = random_date(start_date, end_date)
                        if random_time not in used_dates:
                            used_dates.add(random_time)
                            break
                    writer.writerow([device_id, org_id, random_time, int(datetime.datetime.strptime(random_time, '%Y-%m-%d').timestamp() * 1000)])


if __name__ == "__main__":
    generate_sample_csv()
    print("Sample CSV file generated.")
