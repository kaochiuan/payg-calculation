# PAYG Usage Calculation

A Python-based utility for calculating and processing Pay-As-You-Go (PAYG) usage data from various sources including BigQuery and CSV files.

## Project Overview

This project provides tools to:
1. Extract usage data from BigQuery tables or CSV files
2. Transform data between postpay and PAYG formats
3. Calculate usage metrics by organization and device
4. Generate usage reports by organization and device model
5. Export data to CSV files and optionally upload to AWS S3

## Features

- Data extraction from BigQuery tables
- Data format conversion between postpay and PAYG formats
- Usage calculation and aggregation by organization
- Device model-based usage analysis and reporting
- CSV file generation for usage reports
- Sample data generation for testing
- AWS S3 integration for data storage

## File Structure

- `calculate_payg_usage_report_from_csv.py`: Processes PAYG usage data from CSV files and generates reports with device model analysis
- `save_payg_usage_from_bigquery.py`: Extracts usage data from BigQuery and saves to CSV/S3
- `combine_usage_raw_csv.py`: Combines and transforms data from multiple CSV sources
- `generate_sample_csv_for_payg_format.py`: Creates sample data in PAYG format with GSP support information
- `generate_sample_csv_for_postpay_format.py`: Creates sample data in postpay format
- Sample data files: `sample_payg.csv`, `sample_postpay.csv`, `sample_usage_raw.csv`
- Sample JSON files: `sample_payg.json`, `sample_postpay.json`
- Generated reports: `[owner_id].csv`, `[owner_id]_gsp_summary_by_model.csv`

## Data Formats

### Postpay Format
- `device_id`: String - Unique identifier for the device
- `organization_id`: String - Organization identifier
- `date`: Date - Usage date (YYYY-MM-DD)
- `create_at`: Timestamp - Record creation timestamp

### PAYG Format
- `uuid`: String - Unique identifier for the usage record
- `device_id`: String - Unique identifier for the device
- `org_id`: String - Organization identifier
- `time`: Date - Usage date (YYYY-MM-DD)
- `pro`: Boolean - Pro tier flag
- `gsp`: Boolean - GSP tier flag
- `device_model`: String - Model of the device (added in latest version)

## Usage

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/payg-calculation.git
cd payg-calculation

# Install dependencies
pip install -r requirements.txt
```

### Calculate PAYG Usage from CSV

```python
# Example usage
from calculate_payg_usage_report_from_csv import get_payg_usage_from_csv, count_usage_by_org_id

# Load usage data
usage_data = get_payg_usage_from_csv("sample_usage_raw.csv")

# Calculate usage by organization
usage_by_org = count_usage_by_org_id(usage_data)
print(usage_by_org)
```

### Generate Device Model Usage Reports

The latest version now supports generating usage reports by device model:

```python
# Example usage
from calculate_payg_usage_report_from_csv import get_payg_usage_from_csv

# Load usage data and device information
usage_raw_data = get_payg_usage_from_csv("sample_usage_raw.csv")

# Load device model information from JSON
with open("sample_payg.json", "r") as f:
    sample_org_data = json.load(f)

# Map device IDs to models
device_to_model = {}
for org in sample_org_data["org_info"]:
    for device in org["devices"]:
        device_id = device["id"]
        device_model = device["device_model"]
        device_to_model[device_id] = device_model

# Add device model information to usage data
usage_raw_data['device_model'] = usage_raw_data['device_id'].map(device_to_model)

# Generate model-specific reports
gsp_usage_by_model = usage_raw_data.groupby('device_model')['gsp_usage'].sum().reset_index(name='total_gsp_usage')
gsp_usage_by_model.to_csv("gsp_summary_by_model.csv", index=False)
```

### Extract Data from BigQuery

```python
# Example usage
from save_payg_usage_from_bigquery import run_bigquery_query_to_dataframe, write_dataframe_to_csv

# Define query
query = """
SELECT uuid, device_id, org_id, time, pro, gsp
FROM your_project.your_dataset.your_table
WHERE time BETWEEN '2023-01-01' AND '2023-01-31'
"""

# Run query and save results
df = run_bigquery_query_to_dataframe(query, project_id="your-project-id")
write_dataframe_to_csv(df, "usage_data.csv")
```

### Combine Data from Multiple Sources

```python
# Example usage
from combine_usage_raw_csv import read_data_from_csv, append_postpay_usage_to_payg_usage

# Read data from CSV files
postpay_data = read_data_from_csv("sample_postpay.csv")
payg_data = read_data_from_csv("sample_payg.csv")

# Combine data
combined_data = append_postpay_usage_to_payg_usage(postpay_data, payg_data)
```

## Requirements

- Python 3.6+
- pandas
- google-cloud-bigquery
- boto3 (for AWS S3 integration)

## License

[MIT License]
