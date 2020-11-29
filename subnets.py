"""Script to export list of subnets from AWS to .csv"""

import boto3
import json
import pandas as pd

client = boto3.client('ec2')


response = client.describe_subnets()



subnet_id = []
az = []
cidr_block = []
state = []
vpc_id = []


for x in response['Subnets']:
    subnet_id.append(x['SubnetId'])
    az.append(x['AvailabilityZone'])
    cidr_block.append(x['CidrBlock'])
    state.append(x['State'])
    vpc_id.append(x['VpcId'])






subnet_info = {'subnet id': subnet_id, 'availabilityZone': az, 'cidr block': cidr_block, 'state':state, 'VpcId':vpc_id}

df_subnet = pd.DataFrame(subnet_info)


print(df_subnet)

# Change the string below to change the name of the output file
df_subnet.to_csv('output-filename.csv')



