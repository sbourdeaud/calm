# region headers
# escript-template v20190520 / stephane.bourdeaud@nutanix.com
# ! Meant to be edited in VSCode w/ the BetterComments extension installed
# ! Do NOT delete comments from this script!

# * Conventions:
# * Golden Rule: Adhere to https://pep8.org/ Anything listed below which is
# * in contradiction with PEP8 is a lie.
# 1. use all lower case for variable names.
# 2. when composing variable names, use underscore to separate words.
#    Exp: username_secret. Use this same convention in Calm.
# 3. name sections with comments, and comment code where deemed useful.
# 4. don't print secrets, including tokens. Favor authentication
#    (login/logout) in each task.
# 5. when saving your script, name it as the task name appears in Calm,
#    using the following convention: NameOfIntegrationPoint-Verb-Text.py
# 6. use double quotes first, then single quotes.

# TODO Fill in this section with your information
# author:    <your email address here>
# version:   <date / notes>
# task_name: <enter the name of the task this script is for as it appears
# in your blueprint>
# endregion

# region capture Calm variables
# * Capture variables here. This makes sure Calm macros are not referenced
# * anywhere else in order to improve maintainability.
username = '@@{credname.username}@@'
username_secret = "@@{credname.secret}@@"
api_server = "@@{endpoint_ip}@@"
api_server_port = "443"
api_server_endpoint = "/apis/batch/v1/"
# endregion

# region prepare api call
# Form method, url and headers for the API call
url = "https://{}:{}{}".format(
    api_server,
    api_server_port,
    api_server_endpoint
    )
headers = {
    'Content-Type': 'application/json', 
    'Accept': 'application/json'
    }
method = "POST"

# Compose the json payload
payload = {
    "example": "example",
    "example": {
        "example": "example"
    }
}
# endregion

# region make api call
# make the API call and capture the results in the variable called "resp"
resp = urlreq(
    url, verb=method, auth='BASIC', 
    user=username, passwd=username_secret, 
    params=json.dumps(payload), headers=headers
    )

# ! You should not have to change the code below, unless you are passing on
# ! a variable in which case you will need to print it under "if resp.ok"
# deal with the result/response
if resp.ok:
    # print the content of the response
    print json.dumps(
        json.loads(resp.content),
        indent=4
    )
    exit(0)
else:
    # print the content of the response (which should have the error message)
    print "Request failed", json.dumps(
        json.loads(resp.content),
        indent=4
    )
    exit(1)
# endregion