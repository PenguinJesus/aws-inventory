import boto3
import json
import pandas as pd
from datetime import datetime

client = boto3.client('s3')

response = client.list_buckets()

# print(response)

s3_name = []
s3_create_time = []
s3_size = []

for n in response["Buckets"]:
    s3_name.append(n["Name"])
    s3_create_time.append(n["CreationDate"])

for x in s3_name:
    size = 0
    obj = client.list_objects(Bucket = x)
    if "Contents" in obj:
        for b in obj["Contents"]:
            size += b["Size"]
        s3_size.append(size)
    else:
        s3_size.append(0)

s3_create_time_str = []

for h in s3_create_time:
    h = h.strftime("%Y-%m-%d %H:%M:%S+%z")
    h = h[:-6]
    s3_create_time_str.append(h)


s3_info = {"name":s3_name, "creation date": s3_create_time_str, "size (bytes)": s3_size}

df_s3 = pd.DataFrame(s3_info)


# Change the string below to change the name of the output file
df_s3.to_csv('eu-west-1-ck-s3.csv')

print(df_s3)