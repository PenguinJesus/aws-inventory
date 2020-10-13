import boto3
import pandas as pd

client = boto3.client('rds')

response = client.describe_db_instances()

db_name = []
db_engine = []
db_status = []
db_class = []
db_multiaz = []
db_security_groups = []
db_vpc = []
db_vpc_security_groups = []
db_subnets = []
db_storage = []


empty_list = []



for x in response['DBInstances']:
    db_name.append(x['DBInstanceIdentifier'])
    db_class.append(x['DBInstanceClass'])
    db_engine.append(x['Engine'])
    db_status.append(x['DBInstanceStatus'])
    db_storage.append(x['AllocatedStorage'])
    if x['MultiAZ'] is True:
        db_multiaz.append('Yes')
    else:
        db_multiaz.append('no')
    if len(x['DBSecurityGroups']) > 1:
        y = []
        for n in x["DBSecurityGroups"]:
            y.append(n["DBSecurityGroupName"])
        db_security_groups.append(y)
    elif x['DBSecurityGroups'] == []:
        db_security_groups.append("no sec group")
    else:
        print(x)
        db_security_groups.append(x['DBSecurityGroups'][0]['GroupName'])
    db_vpc.append(x['DBSubnetGroup']["VpcId"])
    if len(x['VpcSecurityGroups']) > 1:
        z = []
        for n in x["VpcSecurityGroups"]:
            z.append(n["VpcSecurityGroupId"])
        db_vpc_security_groups.append(z)
    elif x['VpcSecurityGroups'] == []:
        db_vpc_security_groups.append("no vpc sec group")
    else:
        db_vpc_security_groups.append(x['VpcSecurityGroups'][0]['VpcSecurityGroupId'])
    if len(x["DBSubnetGroup"]['Subnets']) > 1:
        b = []
        for n in x["DBSubnetGroup"]['Subnets']:
            b.append(n["SubnetIdentifier"])
        db_subnets.append(b)
    elif x["DBSubnetGroup"]['Subnets'] == []:
        db_subnets.append("no subnets")
    else:
        db_subnets.append(x["DBSubnetGroup"]['Subnets'][0]['SubnetIdentifier'])



db_info = {"name":db_name, "engine": db_engine,"status": db_status,"instance type": db_class,"Size GiB": db_storage, "multiAZ":db_multiaz,"vpc id": db_vpc, "security group": db_security_groups, "vpc security groups": db_vpc_security_groups, "subnets": db_subnets}

df_rds = pd.DataFrame(db_info)


print(df_rds)


# Change the string below to change the name of the output file
df_rds.to_csv('rds.csv')



