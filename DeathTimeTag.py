import boto3
import sys

def updateDeathTimeAsg(asgIDs, deathTime):
    client = boto3.client('autoscaling')
    invalid_asg = ""
    #invalid_asg = []
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
	    if invalid_asg:
                invalid_asg = invalid_asg + "," + asg
            else:
                invalid_asg = asg
            #invalid_asg.append(asg)
    return invalid_asg
            

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
    invalid_ASGsEast = ""
    invalid_ASGsWest = ""
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
        print("Trying for west region to check  for failed instances in east")
        invalid_InstancesWest = updateDeathTimeInstance(invalid_InstancesEast, sys.argv[3])
        print("#################################################")

    if invalid_ASGsEast:
        # Trying for west region for failed instances if any
        print("Trying for west region to check for failed AutoScalingGroup in east")
        invalid_ASGsWest = updateDeathTimeAsg(invalid_ASGsEast, sys.argv[3])
        print("#################################################")

    # To ensure that file is not appended if  invalid_InstancesWest is empty , therefore adding an or conditon 
    if invalid_InstancesWest or invalid_ASGsWest:
        emailFile = open("FailedInstanceData","w")
        emailFile.write("<br><b>Follwing Instances Could not be found in East or West Region:</b></br><br>%s</br>" %invalid_InstancesWest)
        emailFile.close()

    if invalid_ASGsWest:
        emailFile = open("FailedInstanceData","a")
        emailFile.write("<br><b>Following AutoScalingGroup Could not be found in East or West Region:</b></br><br>%s</br>" %invalid_ASGsWest)
        emailFile.close()
