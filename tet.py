import boto3
import sys


def updateDeathTimeAsg(asg, deathTime):
    client = boto3.client('autoscaling')
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

def findAsgTaggedToInstance(instance, deathTime):
    client = boto3.client('ec2')
    response = client.describe_instances(InstanceIds=['i-024499041077374a7'])
    for tag in response['Reservations'][0]['Instances'][0]['Tags']:
	if tag['Key'] == 'aws:autoscaling:groupName':
	    asgname = tag['Value']
	    updateDeathTimeAsg(asgname, deathTime)

def updateDeathTimeInstance(instanceIDs, deathTime):
    client = boto3.client('ec2')
    invalid_instances = ""
    #invalid_instances = []
    for instance in instanceIDs.split(","):
        print instance
        try:
            response = client.create_tags(Resources=[instance],
                Tags=[
                    {   
                        'Key': 'DeathTime',
                        'Value': deathTime
                    }]
                )
            findAsgTaggedToInstance(instance, deathTime)
        except:
            #invalid_instances.append(instance)
            if invalid_instances:
                invalid_instances = invalid_instances + "," + instance
            else:
                invalid_instances = instance
    return invalid_instances
        

if __name__ == "__main__":
    
    # Assigning null values to prevent failures
    invalid_InstancesEast = ""
    invalid_InstancesWest = ""

    # try for east region first
    print("#################################################")
    if sys.argv[1] == "None" or sys.argv[1] == "":
        print("No Instance tags specified in jenkins parameters")
    else:
        print("Instance tags found in jenkins parameters")
        invalid_InstancesEast = updateDeathTimeInstance(sys.argv[1], sys.argv[2])
    
    print("#################################################")

    print "---------West----------"

    if invalid_InstancesEast:
        # Trying for west region for failed instances if any
        print("Trying for west region to check  for failed instances in east")
        invalid_InstancesWest = updateDeathTimeInstance(invalid_InstancesEast, sys.argv[2])
        print("#################################################")

    emailFile = open("FailedInstanceData","w")
    emailFile.close()
    if invalid_InstancesWest:
        emailFile = open("FailedInstanceData","w")
        emailFile.write("<br><b>Follwing Instances Could not be found in East or West Region:</b></br><br>%s</br>" %invalid_InstancesWest)
        emailFile.close()
