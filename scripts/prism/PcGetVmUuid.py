# region headers
# escript-template v20190605 / stephane.bourdeaud@nutanix.com
# * author:     stephane.bourdeaud@nutanix.com
# * version:    20191022
# task_name:    PcGetVmUuid
# description:  Gets the uuid of the specified VMs from Prism Central.
# output:       vm_uuid
# endregion

# region capture Calm variables
username = "@@{pc.username}@@"
username_secret = "@@{pc.secret}@@"
api_server = "@@{pc_ip}@@"
vm_name = "@@{vm_name}@@"
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
    "filter": "vm_name == {}".format(vm_name) 
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

# deal with the result/response
if resp.ok:
    json_resp = json.loads(resp.content)
    for vm in json_resp['entities']:
        print "vm_uuid = {}".format(vm['metadata']['uuid'])
        exit(0)
    print("No vm found!")
    exit(1)
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
