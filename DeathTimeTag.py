#import boto3
import sys

def updateDeathTimeAsg(asgIDs):
    #client = boto3.client('autoscaling')
    for asg in asgIDs.split(","):
        print asg

if __name__ == "__main__":

    if sys.argv[1] == "None" or sys.argv[1] == "":
        print "No Instance to tag"
    else:
        print sys.argv[1]
        updateDeathTimeAsg(sys.argv[1])
    
    if sys.argv[2] == "None" or sys.argv[1] == "":
        print "No Autoscaling to tag"
    else:
        print sys.argv[2]
        updateDeathTimeAsg(sys.argv[2])
