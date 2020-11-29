"""Script to export list of EBS/EC2/RDS/S3/Subnets from AWS to .csv"""

import boto3
import pandas as pd

"""EBS""" 


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




"""EC2"""


client = boto3.client('ec2')


response = client.describe_instances()


instance_id = []
instance_type = []
state_name = []
image_id = []
platform_type = []
ami_id = []
empty_list = []
security_groups = []
vpc_id = []
subnet = []
name = []
private_ip=[]



# print(response) #pretty print response from describe_instance

for x in response['Reservations']:
    for y in x['Instances']:
        instance_id.append(y['InstanceId'])
        instance_type.append(y['InstanceType'])
        image_id.append(y['ImageId'])
        state_name.append(y['State']['Name'])
        vpc_id.append(y["VpcId"])
        if len(y['SecurityGroups']) > 1:
            x = []
            for n in y["SecurityGroups"]:
                x.append(n["GroupName"])
            security_groups.append(x)
        else:
            security_groups.append(y['SecurityGroups'][0]['GroupName'])
        subnet.append(y["NetworkInterfaces"][0]["SubnetId"])
        if "Tags" in y:   
            for n in y["Tags"]:
                if n["Key"] == "Name":
                    name.append(n["Value"])
        else:
            name.append("N/A")
        private_ip.append(y["NetworkInterfaces"][0]["PrivateIpAddress"])



for n in image_id:
    obj = client.describe_images(ImageIds=[n])
    if obj['Images'] == empty_list:
        platform_type.append('NoPlatform')
        ami_id.append('NoAccess')
    else:
        for b in obj['Images']:
            if 'PlatformDetails' in b:
                platform_type.append(b['PlatformDetails'])
                ami_id.append(b['Name'])
            else:
                platform_type.append('NoPlatform')
                ami_id.append(b['Name'])
    



instance_info = {"name":name, "instance ID" : instance_id , "instance type" : instance_type, "state": state_name, "image ID": image_id, "Platform type": platform_type, "ami ID": ami_id,"VPC ID": vpc_id, "private ip": private_ip, "subnet": subnet}

df_ec2 = pd.DataFrame(instance_info)


print(df_ec2)




""" RDS """


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

print(df_s3)


""" Subnets """


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




""" IAM """
client = boto3.client('iam')

response_list_users = client.list_users()


username = []
user_arn = []
create_date = []
create_date_str = []
password_last_used = []
password_last_used_str = []
groups = []
access_keys_id = []
access_keys_status = []
access_keys_create_date = []


for x in response_list_users['Users']:
    username.append(x['UserName'])
    user_arn.append(x['Arn'])
    create_date.append(x['CreateDate'])
    if 'PasswordLastUsed' in x:
        password_last_used.append(x['PasswordLastUsed'])
    else:
        password_last_used.append('null')
    ###list group information
    response_groups = client.list_groups_for_user(UserName=x['UserName'])
    groups_temp = [] #temporary list to hold group information
    if response_groups['Groups'] is not None:
        for y in response_groups['Groups']:
            groups_temp.append(y['GroupName'])
    else:
        groups_temp.append('None')
    groups.append(groups_temp)
    #list Access key information
    response_access = client.list_access_keys(UserName=x['UserName'])
    access_keys_id_temp = []
    access_keys_status_temp = []
    access_keys_create_date_temp = []
    if response_access is not None:
        for z in response_access['AccessKeyMetadata']:
            access_keys_id_temp.append(z['AccessKeyId'])
            access_keys_status_temp.append(z['Status'])
            c_date_str = z['CreateDate'].strftime("%Y-%m-%d %H:%M:%S+%z")
            c_date_str = c_date_str[:-6]
            access_keys_create_date_temp.append(c_date_str)
    else:
        access_keys_id_temp.append('None')
        access_keys_status_temp.append('None')
        access_keys_create_date_temp.append('None')
    access_keys_id.append(access_keys_id_temp)
    access_keys_status.append(access_keys_status_temp)
    access_keys_create_date.append(access_keys_create_date_temp)



#convert create_date datetime to string
for h in create_date:
    h = h.strftime("%Y-%m-%d %H:%M:%S+%z")
    h = h[:-6]
    create_date_str.append(h)

for g in password_last_used:
    if g is not 'null':
        g = g.strftime("%Y-%m-%d %H:%M:%S+%z")
        g = g[:-6]
        password_last_used_str.append(g)
    else:
        password_last_used_str.append('None')


iam_info = {'username': username, 'user_arn': user_arn, 'Created Date': create_date_str, 'Password last used': password_last_used_str, 'Groups': groups, 'Access key ID': access_keys_id, 'Access key status': access_keys_status, 'Access key create date': access_keys_create_date}

df_iam = pd.DataFrame(iam_info)

print(df_iam)



# Change the string below to change the name of the output file
writer = pd.ExcelWriter('eu-central-1-ck-all.xlsx', engine = 'xlsxwriter')

df_ec2.to_excel(writer, sheet_name="ec2")
df_ebs.to_excel(writer,sheet_name="ebs")
df_rds.to_excel(writer,sheet_name="rds")
df_s3.to_excel(writer,sheet_name="s3")
df_subnet.to_excel(writer,sheet_name="subnets")
df_iam.to_excel(writer, sheet_name='iam')

writer.save()
