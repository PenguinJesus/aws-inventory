"""Script to export list of ebs volumes in .csv"""

import boto3
import json
import pandas as pd

client = boto3.client('ec2')

response = client.describe_volumes()

# print(response)

ebs_name = []
ebs_volume_id = []
ebs_size = []
ebs_volume_type = []
ebs_state = []
ebs_az = []
ebs_iops = []


for n in response["Volumes"]:
    if "Tags" in n:
        g = ""
        for x in n["Tags"]:
            if x["Key"] == "Name":
                g=x["Value"]
            else:
                g="N/A"
        ebs_name.append(g)
    else:
        ebs_name.append("N/A")
    ebs_volume_id.append(n["VolumeId"])
    ebs_size.append(n["Size"])
    ebs_volume_type.append(n["VolumeType"])
    ebs_state.append(n["State"])
    ebs_az.append(n["AvailabilityZone"])
    if "Iops" in n:
        ebs_iops.append(n["Iops"])
    else:
        ebs_iops.append("N/A")

# print(name)
# print(len(name))

# print(volume_id)
# print(len(volume_id))

volume_info = {"name":ebs_name, "volume id": ebs_volume_id, "size GiB": ebs_size, "type": ebs_volume_type, "state": ebs_state, "az":ebs_az, "iops": ebs_iops}

df_ebs = pd.DataFrame(volume_info)


print(df_ebs)

# Change the string below to change the name of the output file
df_ebs.to_csv('eu-west-1-ck-ebs.csv')
