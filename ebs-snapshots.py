"""Script for exporting list of snapshots in AWS into .csv"""

import boto3
import pandas as pd

client = boto3.client('ec2')

response = client.describe_snapshots(OwnerIds=['123345456']) # ENTER ACCOUNT ID HERE


owner_id = "1234566789" # ENTER ACCOUNT ID HERE



snapshot_id = [] 
volume_id = []
volume_size = []
encryption = []
kms_key = []


for n in response["Snapshots"]:
    snapshot_id.append(n["SnapshotId"])
    volume_id.append(n["VolumeId"])
    volume_size.append(n["VolumeSize"])
    encryption.append(n["Encrypted"])
    if "KmsKeyId" in n:
        kms_key.append(n["KmsKeyId"])
    else:
        kms_key.append("N/A")




snapshot_info = {"snapshot id": snapshot_id, "volume id": volume_id, "volume size": volume_size,"encryption": encryption, "kms key id": kms_key}


df = pd.DataFrame(snapshot_info)


print(df)


df.to_csv('eu-west-1-ck-snapshots.csv')
