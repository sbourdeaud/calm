# escript-template v20190520 / stephane.bourdeaud@nutanix.com
# ! Meant to be edited in VSCode with the BetterComments extension installed.
# ! Do NOT delete comments from this script!

# * Conventions:
# 1. use all lower case for variable names.
# 2. when composing variable names, use underscore to separate words. 
#    Exp: username_secret. Use this same convention in Calm.
# 3. name sections with comments, comment line after the code.
# 4. don't print secrets, including tokens. Favor authentication (login/logout) 
#    in each script.
# 5. when saving your script, name it as the task name appears in Calm, using
#    the following convention: NameOfIntegrationPoint-Verb-Text.py
# 6. use double quotes first, then single quotes.

# TODO Fill in this section with your information
# TODO author:    <your email address here>
# TODO version:   <date / notes>
# TODO task_name: <enter the name of the task this script is for as it appears in your blueprint>

# * Capture variables here. This makes sure Calm macros are not referenced 
# * anywhere else in order to improve reusability.
username = '@@{credname.username}@@' #this is the username which will be used to make the API call
username_secret = "@@{credname.secret}@@" #this is the password for the username used to make the API call
api_server = "@@{endpoint_ip}@@" #this is the IP address of the API server
api_server_port = "443" #this is the TCP port used to access the API server
api_server_endpoint = "/apis/batch/v1/" #this is the address of the API endpoint

# Form method, url and headers for the API call
url = "https://{}:{}{}".format(api_server,api_server_port,api_server_endpoint) #this is the url which will be used to make the API call
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'} #those are the headers which will be used to make the API call
method = "POST" #this is the method which will be used for the API call

# Compose the json payload
payload = {
  "example": "example",
  "example": {
    "example": "example"
  }
}

# make the API call and capture the results in the variable called "resp"
resp = urlreq(url, verb=method, auth='BASIC', user=username, passwd=username_secret, params=json.dumps(payload), headers=headers)

# ! You should not have to change the code below, unless you are passing on a 
# ! variable in which case you will need to print it under "if resp.ok"
# deal with the result/response
if resp.ok:
  print json.dumps(json.loads(resp.content), indent=4) #this prints the content of the response
  exit(0)
else:
  print "Request failed", json.dumps(json.loads(resp.content), indent=4) #this prints the content of the response
  exit(1) #this makes sure the task will return as FALSE