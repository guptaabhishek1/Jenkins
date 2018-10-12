#import boto3
import sys

def updateDeathTimeAsg(asgIDs):
    #client = boto3.client('autoscaling')
    for asg in asgIDs.split(","):
        print asg

def updateDeathTimeInstance(instanceIDs):
    #client = boto3.client('autoscaling')
    for instance in instanceIDs.split(","):
        print instance
        
if __name__ == "__main__":

    if sys.argv[1] == "None" or sys.argv[1] == "":
        print("No Instance tags specified in jenkins parameters")
    else:
        print("Instance tags found in jenkins parameters")
        updateDeathTimeInstance(sys.argv[1])
    
    if sys.argv[2] == "None" or sys.argv[2] == "":
        print("No AutoScaling tags specified in jenkins parameters")
    else:
        print("AutoScaling tags specified in jenkins parameters")
        updateDeathTimeAsg(sys.argv[2])
