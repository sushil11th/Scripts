import boto3
import json
from collections import defaultdict

region = 'us-west-1'

def lambda_handler(event, context):
    HTTPS_PROXY = 'http://primary-proxy.gslb.intranet.barcapint.com:8080'
    elbv2client = boto3.client('elbv2')
    
    client = boto3.client('ec2')

    running_instances = client.describe_instances(
      Filters=[
        {
            'Name': 'tag:INFRA:Hostname',
            'Values': [
                'duwdsr002070613.intranet.barcapint.com',
            ]
        },
    ],
    )
    
    instance_ids = []    
    
    for reservation in running_instances['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])
        
    #return instance_ids
    for each in instance_ids:
        #print(each)
    #return each
    
        healthtarget = elbv2client.describe_target_health(
        TargetGroupArn='arn:aws:elasticloadbalancing:eu-west-1:632210341693:targetgroup/vault-albtg-vlt-csm-dev/d5018c0bc84243d4',
        Targets=[
        {
            'Id': each,
        }
        ]
        )
        print("healthtarget = ", healthtarget)
        register_response = elbv2client.register_targets(
        TargetGroupArn='arn:aws:elasticloadbalancing:eu-west-1:632210341693:targetgroup/vault-albtg-vlt-csm-dev/d5018c0bc84243d4',
        Targets=[
        {
            'Id':each,
        }
        ]
        )
        print("register_response = ",  register_response)

    return {
        
        'statusCode': 200,
        'body': json.dumps(register_response)
    }