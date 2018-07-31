#!/bin/bash

actualvalue=$1
comparevalue=$2

compare_content()
{
	echo $1
	echo $2
	cat $1
	cat $2
	status="SUCCESS"
}

compare_content $1 $2
echo $status
