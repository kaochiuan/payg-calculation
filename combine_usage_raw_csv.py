# I have two bigquery tables:
# 1. table1(sample_postpay.csv): has 4 columns: device_id:str, organization_id:str, date:date, create_at:timestamp
# 2. table2(sample_payg.csv): has 6 columns: uuid:str, device_id:str, org_id:str, time:date, pro:boolean, gsp:boolean
# I want to do this in using python and write the query result to another csv file

import pandas as pd
import uuid


def read_data_from_csv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    return df


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

# append data from table1 and table2


def append_data_from_table1_and_table2(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    df = df1.append(df2)
    return df


def combine_data_from_table1_and_table2(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    df = pd.concat([df1, df2], ignore_index=True)
    return df


def write_data_to_csv(df: pd.DataFrame, file_path: str) -> None:
    df.to_csv(file_path, index=False)


if __name__ == "__main__":
    df1 = read_data_from_csv("sample_postpay.csv")
    df2 = read_data_from_csv("sample_payg.csv")
    df3 = transfer_data_format_from_postpay_to_payg(df1)
    df = combine_data_from_table1_and_table2(df2, df3)
    write_data_to_csv(df, "sample_usage_raw.csv")
    print("Combined usage raw data written to sample_usage_raw.csv")
