#!/bin/bash

actualvalue=$1
comparevalue=$2

compare_content()
{
	status="SUCCESS"
	for line in `cat $1|sed -e "s/, /,/g"`
	do
		event=`echo $line|cut -d "," -f1`
		for cmp_line in `cat $2|sed -e "s/, /,/g"`
		do
			cmp_event=`echo $cmp_line|cut -d "," -f1`
			if [ ${cmp_event} = ${event} ]
			then
				original_value=`echo $line|cut -d "," -f2`	
				compare_value=`echo $cmp_line|cut -d "," -f2`	

				# get the percent diff 
				if [ $original_value -eq $compare_value ]
				then
					continue
				elif [ $original_value -eq 0 ]
				then
					continue
				else
					# pass limit is greater then 50%
					pass_limit_org_value=`expr $original_value / 2`

					if [ $compare_value -lt $pass_limit_org_value ]
					then
						status="FAILED"	
						break
					fi
				fi
			fi
		done
	done
		
}

compare_content ${actualvalue} ${comparevalue}
echo $status
