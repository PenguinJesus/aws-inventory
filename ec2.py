"""Script to export list of EC2 instances from AWS"""

import boto3
import pandas as pd

client = boto3.client('ec2')


response = client.describe_instances()

print(response)


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
private_ip = []



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
    


instance_info = {"name":name, "instance ID" : instance_id , "instance type" : instance_type, "state": state_name, "image ID": image_id, "Platform type": platform_type, "ami ID": ami_id,"VPC ID": vpc_id, "subnet": subnet, "private ip": private_ip , "security groups": security_groups}

df_ec2 = pd.DataFrame(instance_info)

print(df_ec2)


print(df_ec2)

# Change the string below to change the name of the output file
df_ec2.to_csv('output-filename.csv')



