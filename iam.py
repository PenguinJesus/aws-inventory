"""Script to export list of IAM users into .csv"""

import boto3
import pandas as pd

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


#convert createa_date datetime to string
for h in create_date:
    h = h.strftime("%Y-%m-%d %H:%M:%S+%z")
    h = h[:-6]
    create_date_str.append(h)

print(create_date)
print(password_last_used)


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
#df_iam.to_csv('eu-west-1-ck-iam.csv')

