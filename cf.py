import boto3
import json

client = boto3.client('cloudformation')

#response = client.get_template(
#	StackName="arn:aws:cloudformation:us-east-1:401369994581:stack/TestStack/a9999e30-caf7-11e8-81fd-500c286e1a36")
	
#body_response = json.dumps(response['TemplateBody'], sort_keys=True)
#print body_response


response = client.describe_stacks(StackName="arn:aws:cloudformation:us-east-1:401369994581:stack/Test1/d6eda8c0-cb03-11e8-a9a6-500c20fefad2")
print response['Stacks'][0]['Parameters']

datapoint = []
for parameters in response['Stacks'][0]['Parameters']:
    line = "{'ParameterKey': '%s', 'UsePreviousValue': True,}" %(parameters['ParameterKey'])
    datapoint.append(line)


param = json.dumps(datapoint, sort_keys=True)
print param


response = client.update_stack(
	StackName="arn:aws:cloudformation:us-east-1:401369994581:stack/Test1/d6eda8c0-cb03-11e8-a9a6-500c20fefad2",
    #TemplateBody=body_response,
    UsePreviousTemplate=True,
	Parameters=[
	{
		'ParameterKey': 'DBName',
		'UsePreviousValue': True,
	},
	{
		'ParameterKey': 'KeyName',
		'UsePreviousValue': True,
	},
	{	'ParameterKey': 'DBPassword',
		'UsePreviousValue': True,
	},
	{	'ParameterKey': 'DBRootPassword',
		'UsePreviousValue': True,
	},
	{
		'ParameterKey': 'DBUser',
		'UsePreviousValue': True,
	},],
	Tags=[
		{
			'Key': 'KDeathTime',
			'Value': "20181008"
		}
	])
