# get payg usage data from csv
# csv file contains the following 6 columns:
# uuid:str, device_id:str, org_id:str, time:date, pro:boolean, gsp:boolean

import pandas as pd
import json

def download_payg_usage_from_s3(s3_bucket: str, s3_key: str) -> pd.DataFrame:
    df = pd.read_csv(f"s3://{s3_bucket}/{s3_key}")
    return df

def get_payg_usage_from_csv(csv_file_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_file_path)
    return df

# count usage by org_id and gsp/pro
# if gsp and pro both are true, count gsp usage, ignore pro
# if gsp is false and pro is false, count pro usage
def count_usage_by_org_id(df: pd.DataFrame) -> pd.DataFrame:
    df['gsp_usage'] = df.apply(lambda x: 1 if x['gsp'] else 0, axis=1)
    df['pro_usage'] = df.apply(lambda x: 1 if x['pro'] else 0, axis=1)
    df_grouped = df.groupby('org_id').agg({'gsp_usage': 'sum', 'pro_usage': 'sum'}).reset_index()
    # pro is the subset of gsp, so the real usage is pro_usage - gsp_usage
    df_grouped['pro_usage'] = df_grouped.apply(lambda x: x['pro_usage'] - x['gsp_usage'] if x['pro_usage'] > x['gsp_usage'] else 0, axis=1)
    return df_grouped


# csv file contains the following 6 columns:
# uuid:str, device_id:str, org_id:str, time:date, pro:boolean, gsp:boolean
# save given org_id list, the write usage data to csv file
def save_usage_to_csv(df: pd.DataFrame, org_id_list: list, csv_file_path: str, s3_bucket: str, s3_key: str):
    df = df[df['org_id'].isin(org_id_list)]
    df.to_csv(csv_file_path, index=False)
    
    ## upload the csv file to aws s3 bucket
    # import boto3
    # s3_client = boto3.client('s3')
    # s3_client.upload_file(csv_file_path, s3_bucket, s3_key)    

def get_org_information_from_json(json_file_path: str) -> dict:
    with open(json_file_path, 'r') as f:
        org_info = json.load(f)
    return org_info

if __name__ == "__main__":
    usage_raw_data = get_payg_usage_from_csv(csv_file_path="sample_usage_raw.csv")
    usage = count_usage_by_org_id(usage_raw_data)
    print(usage)

    # Load sample_org.json to map device_id to owner_id
    with open("sample_payg.json", "r") as f:
        sample_org_data = json.load(f)

    device_to_owner = {}
    for org in sample_org_data["org_info"]:
        owner_id = org["owner_id"]
        for device_id in org["devices"]:
            device_to_owner[device_id] = owner_id

    # Group usage data by owner_id
    grouped_usage = {}
    for index, row in usage_raw_data.iterrows():
        device_id = row["device_id"]
        owner_id = device_to_owner.get(device_id)
        if owner_id:
            if owner_id not in grouped_usage:
                grouped_usage[owner_id] = []
            grouped_usage[owner_id].append(row)

    # Save usage data to csv file based on owner_id
    for owner_id, usage_data in grouped_usage.items():
        usage_df = pd.DataFrame(usage_data).sort_values(by=['org_id', 'device_id', 'time'], ascending=True)
        #usage_df content should be like:
        # uuid,device_id,org_id,time,pro,gsp,gsp_usage,pro_usage
        save_usage_to_csv(usage_df, usage_df["org_id"].unique(), csv_file_path=f"{owner_id}.csv", s3_bucket="XXXXXXXXXXXXXXXX", s3_key=f"{owner_id}.csv")

    print("Calculate PAYG usage report from CSV file generated.")
