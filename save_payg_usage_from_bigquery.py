# I have two bigquery tables:
# 1. table1(sample_postpay.csv): has 4 columns: device_id:str, organization_id:str, date:date, create_at:timestamp
# 2. table2(sample_payg.csv): has 6 columns: uuid:str, device_id:str, org_id:str, time:date, pro:boolean, gsp:boolean
# I want to do this in bigquery using python and write the query result to a csv file
# And upload the csv file to aws s3 bucket

import pandas as pd
from google.cloud import bigquery
from typing import Optional
import uuid

# get usage data from table1, start_date and end_date are the date range for the usage data


def get_usage_data_from_table1(start_date, end_date):
    query = """
    SELECT table1.device_id, table1.organization_id, table1.date, table1.create_at
    WHERE table1.date between {start_date} and {end_date}
    """
    return query


def get_usage_data_from_table2(start_date, end_date):
    query = """
    SELECT table2.uuid, table2.device_id, table2.org_id, table2.time, table2.pro, table2.gsp
    WHERE table2.time between {start_date} and {end_date}
    """
    return query


def transfer_data_format_from_postpay_to_payg(df: pd.DataFrame) -> pd.DataFrame:
    df['uuid'] = uuid.uuid4()
    df['device_id'] = df['device_id']
    df['org_id'] = df['organization_id']
    df['time'] = df['date']
    df['pro'] = True
    df['gsp'] = False
    df = df.drop(columns=['create_at', 'organization_id', 'date'])
    df.reindex(columns=['uuid', 'device_id', 'org_id', 'time', 'pro', 'gsp'])
    return df


def run_bigquery_query_to_dataframe(
    query: str,
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    credentials_path: Optional[str] = None,
    **kwargs
) -> pd.DataFrame:
    try:
        if credentials_path:
            import os
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        client = bigquery.Client(
            project=project_id, location=location, **kwargs)
        query_job = client.query(query)
        query_job.result()
        df = query_job.to_dataframe()
        return df
    except Exception as e:
        raise Exception(f"Error running BigQuery query: {e}")


def write_dataframe_to_csv(df: pd.DataFrame, file_path: str):
    try:
        df.to_csv(file_path, index=False)
    except Exception as e:
        raise Exception(f"Error writing DataFrame to CSV: {e}")


def upload_csv_to_s3(file_path: str, bucket_name: str, object_name: Optional[str] = None):
    try:
        import boto3
        s3 = boto3.client('s3')
        if object_name is None:
            object_name = file_path
        s3.upload_file(file_path, bucket_name, object_name)
    except Exception as e:
        raise Exception(f"Error uploading CSV to S3: {e}")
