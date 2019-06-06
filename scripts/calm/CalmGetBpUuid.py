# region headers
# escript-template v20190605 / stephane.bourdeaud@nutanix.com
# * author:       igor.zecevic@nutanix.com
# * version:      2019/06/04
# task_name:      CalmGetBpUuid
# description:    This script gets the uuid of the specified blueprint.
# TODO: test
# endregion

# region capture Calm macros
pc_ip = '@@{pc_ip}@@'
username = '@@{pc_user.username}@@'
username_secret = '@@{pc_user.secret}@@'
blueprint_name = '@@{blueprint_name}@@'
# endregion

# region prepare variables
headers = {'content-type': 'application/json'}
# endregion

# region REST call: Get Blueprint UUID
method = 'POST'
url = "https://{}:9440/api/nutanix/v3/blueprints/list".format(pc_ip)
payload = {
    "kind": "blueprint",
    "filter": "name=='+blueprint_name+'"
}
print("Making a {} API call to {}".format(method, url))
resp = urlreq(
    url,
    verb=method,
    params=json.dumps(payload),
    headers=headers,
    auth='BASIC',
    user=username,
    password=username_secret,
    verify=False
)

if resp.ok:
    json_resp = json.loads(resp.content)
    blueprint_uuid = json_resp['entities']['metadata']['uuid']
    print("blueprint_uuid={}".format(blueprint_uuid))
    exit(0)
else:
    print("Request failed")
    print("Headers: {}".format(headers))
    print('Status code: {}'.format(resp.status_code))
    print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
    exit(1)
# endregion
