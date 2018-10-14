import boto3
import sys

def updateDeathTimeAsg(asgIDs, deathTime):
    client = boto3.client('autoscaling')
    invalid_asg = []
    for asg in asgIDs.split(","):
        print asg
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
        print instance
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
    
    # try for east region first
    print("#################################################")
    if sys.argv[1] == "None" or sys.argv[1] == "":
        print("No Instance tags specified in jenkins parameters")
    else:
        print("Instance tags found in jenkins parameters")
        invalid_InstancesEast = updateDeathTimeInstance(sys.argv[1], sys.argv[3])
    
    print("#################################################")
    if sys.argv[2] == "None" or sys.argv[2] == "":
        print("No AutoScaling tags specified in jenkins parameters")
    else:
        print("AutoScaling tags specified in jenkins parameters")
        invalid_ASGsEast = updateDeathTimeAsg(sys.argv[2], sys.argv[3])
    print("#################################################")

    if invalid_InstancesEast:
        # Trying for west region for failed instances if any
        print("Trying for west region for failed instances if any")
        invalid_InstancesWest = updateDeathTimeInstance(invalid_InstancesEast, sys.argv[3])

    if invalid_ASGsEast:
        # Trying for west region for failed instances if any
        invalid_ASGsWest = updateDeathTimeAsg(invalid_ASGsEast, sys.argv[3])

    if invalid_InstancesWest:
        print "Sending email for instances not found in both region east and west"
        print invalid_InstancesWest
    
    if invalid_ASGsWest:
        print "Sending ASG for instances not found in both region east and west"
        print invalid_ASGsWest
