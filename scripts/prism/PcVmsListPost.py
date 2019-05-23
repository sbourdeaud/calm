# region headers
# escript-template v20190523 / stephane.bourdeaud@nutanix.com
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
# 7. Try your best and keep line length under 80 characters, even though
#    it makes your eyes bleed.

# TODO Fill in this section with your information
# author:    stephane.bourdeaud@nutanix.com
# version:   23/05/2019: initial tested version (Calm 2.6.0.3)
# task_name: PcVmsListPost
# endregion

# region capture Calm variables
# * Capture variables here. This makes sure Calm macros are not referenced
# * anywhere else in order to improve maintainability.
username = '@@{prism_api_user.username}@@'
username_secret = "@@{prism_api_user.secret}@@"
api_server = "@@{prism_ip}@@"
# endregion

# region prepare api call
# Form method, url and headers for the API call
api_server_port = "9440"
api_server_endpoint = "/api/nutanix/v3/vms/list"
url = "https://{}:{}{}".format(
    api_server,
    api_server_port,
    api_server_endpoint
)
method = "POST"
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Compose the json payload
payload = {
    "kind": "vm",
    "offset": 0
}
# endregion

# region make api call
# make the API call and capture the results in the variable called "resp"
print("Making a {} API call to {}".format(method, url))
# ! Get rid of verify=False if you're using proper certificates
resp = urlreq(
    url,
    verb=method,
    auth='BASIC',
    user=username,
    passwd=username_secret,
    params=json.dumps(payload),
    headers=headers,
    verify=False
    )

# ! You should not have to change the code below, unless you are passing on
# ! a variable in which case you will need to print it under "if resp.ok"
# deal with the result/response
if resp.ok:
    # print the content of the response
    print(json.dumps(
        json.loads(resp.content),
        indent=4
    ))
    exit(0)
else:
    # print the content of the response (which should have the error message)
    print("Request failed", json.dumps(
        json.loads(resp.content),
        indent=4
    ))
    print("Headers: {}".format(headers))
    print("Payload: {}".format(payload))
    exit(1)
# endregion
