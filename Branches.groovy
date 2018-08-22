import groovy.json.JsonSlurper;
try{
   List<String>params = new ArrayList<String>()
   # The url will be in the below format
   # -- https://api.github.com/users/<repo-owner>/<repo>/branches?access_token=<github-access-token> -- 
   URL apiUrl = "https://api.github.com/repos/widdix123/Jenkins/branches?access_token=1ed14534d3673dce495da3caa8441cd607df6782".toURL()
   List branches = new JsonSlurper().parse(apiUrl.newReader())
   for (branch in branches ) { 
     params.add(branch.name) 
   }
   return params
}
catch(IOException ex){
   print ex
}
