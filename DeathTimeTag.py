import boto3, sys

def updateDeathTimeAsg(asgIDs, deathTime):
    client = boto3.client('autoscaling')
    invalid_asg = []
    for asg in asgIDs.split(","):
        try:
            response = client.create_or_update_tags(
                Tags=[
                    {
                        'ResourceId': asg,
                        'ResourceType': 'auto-scaling-group',
                        'Key': 'DeathTime',
                        'Value': deathTime,
                        'PropagateAtLaunch': True
                    }]
                )
        except:
            invalid_asg.append(asg)
    return invalid_asg
            

def updateDeathTimeInstance(instanceIDs, deathTime):
    client = boto3.client('ec2')
    invalid_instances = []
    for instance in instanceIDs.split(","):
        try:
            response = client.create_tags(Resources=[instance],
                Tags=[
                    {   
                        'Key': 'DeathTime',
                        'Value': deathTime
                    }]
                )
        except:
            invalid_instances.append(instance)
    return invalid_instances
        

if __name__ == "__main__":
    
    print("#################################################")
    if sys.argv[1] == "None" or sys.argv[1] == "":
        print("No Instance tags specified in jenkins parameters")
    else:
        print("Instance tags found in jenkins parameters")
        invalid_Instances = updateDeathTimeInstance(sys.argv[1], sys.argv[3])
    
    print("#################################################")
    if sys.argv[2] == "None" or sys.argv[2] == "":
        print("No AutoScaling tags specified in jenkins parameters")
    else:
        print("AutoScaling tags specified in jenkins parameters")
        invalid_ASGs = updateDeathTimeAsg(sys.argv[2], sys.argv[3])
    print("#################################################")

    if invalid_Instances:
        print invalid_Instances

    if invalid_ASGs:
        print invalid_ASGs
