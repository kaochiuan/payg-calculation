# PAYG Usage Calculation

A Python-based utility for calculating and processing Pay-As-You-Go (PAYG) usage data from various sources including BigQuery and CSV files.

## Project Overview

This project provides tools to:
1. Extract usage data from BigQuery tables or CSV files
2. Transform data between postpay and PAYG formats
3. Calculate usage metrics by organization and device
4. Generate usage reports by organization
5. Export data to CSV files and optionally upload to AWS S3

## Features

- Data extraction from BigQuery tables
- Data format conversion between postpay and PAYG formats
- Usage calculation and aggregation by organization
- CSV file generation for usage reports
- Sample data generation for testing
- AWS S3 integration for data storage

## File Structure

- `calculate_payg_usage_report_from_csv.py`: Processes PAYG usage data from CSV files and generates reports
- `save_payg_usage_from_bigquery.py`: Extracts usage data from BigQuery and saves to CSV/S3
- `combine_usage_raw_csv.py`: Combines and transforms data from multiple CSV sources
- `generate_sample_csv_for_payg_format.py`: Creates sample data in PAYG format
- `generate_sample_csv_for_postpay_format.py`: Creates sample data in postpay format
- Sample data files: `sample_payg.csv`, `sample_postpay.csv`, `sample_usage_raw.csv`

## Data Formats

### Postpay Format
- `device_id`: String - Unique identifier for the device
- `organization_id`: String - Organization identifier
- `date`: Date - Usage date
- `create_at`: Timestamp - Record creation timestamp

### PAYG Format
- `uuid`: String - Unique identifier for the usage record
- `device_id`: String - Unique identifier for the device
- `org_id`: String - Organization identifier
- `time`: Date - Usage date
- `pro`: Boolean - Pro tier flag
- `gsp`: Boolean - GSP tier flag

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
from combine_usage_raw_csv import read_data_from_csv, combine_data_from_table1_and_table2

# Read data from CSV files
postpay_data = read_data_from_csv("sample_postpay.csv")
payg_data = read_data_from_csv("sample_payg.csv")

# Combine data
combined_data = combine_data_from_table1_and_table2(postpay_data, payg_data)
```

## Requirements

- Python 3.6+
- pandas
- google-cloud-bigquery
- boto3 (optional, for AWS S3 integration)

## License

[MIT License]
