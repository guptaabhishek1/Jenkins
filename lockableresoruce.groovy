import groovy.json.*;
import java.util.*; 

JsonSlurper jsonSlurper = new JsonSlurper()
List<String>params = new ArrayList<String>()

def proc = "curl https://jenins:xxxxxxxxx@jenkins.jenkins.com/plugin/lockable-resources/api/json".execute().text
Map convertedJSONMap  = jsonSlurper.parseText(proc)

if(convertedJSONMap."resources"){
	for(resource in convertedJSONMap."resources"){
		resource_status = resource."locked"
		resource_name = resource."name" 
		resource_bname = resource."buildName" 

		if(resource_bname){
			buildname = resource_bname.split("#")[0]
      // change test1 to project name
			if(buildname.trim() == 'test1')
			{
				print resource_name
			}

		}

	}
}

//Steps to run qatest
//cd to directory 
//RESOURCENAME=$(groovy test.groovy)
//cd ../.pl
