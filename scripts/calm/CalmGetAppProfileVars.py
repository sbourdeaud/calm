# region headers
# escript-template v20190605 / stephane.bourdeaud@nutanix.com
# * author:       igor.zecevic@nutanix.com
# * version:      2019/06/05
# task_name:      CalmGetAppProfileVars
# description:    This script gets all the Application Profiles variable of the
# specified blueprint.
# TODO: add ability to specify the application profile (right now it only looks at the first one)
# TODO: test
# endregion

# region capture Calm macros
pc_ip = "@@{pc_ip}@@"
username = "@@{pc_user.username}@@"
username_secret = "@@{pc_user.secret}@@"
blueprint_uuid = "@@{blueprint_uuid}@@"
application_profile_name = "@@{application_profile_name}@@"
vm_hostname = "@@{name}@@"
# endregion

# region prepare variables
headers = {'content-type': 'application/json'}
# endregion

# region REST call: Get Blueprint
method = 'GET'
url = "https://{}:9440/api/nutanix/v3/blueprints/{}".format(
    pc_ip,
    blueprint_uuid
)
print("Making a {} API call to {}".format(method, url))
resp = urlreq(
    url,
    verb=method,
    headers=headers,
    auth="BASIC",
    user=username,
    passwd=username_secret,
    verify=False
)

if resp.ok:
    json_resp = json.loads(resp.text)
    blueprint_app_profile_uuid = json_resp['spec']['resources']['app_profile_list'][0]['uuid']
    blueprint_app_profile_variables = json_resp['spec']['resources']['app_profile_list'][0]['variable_list']

    print("blueprint_app_profile_uuid=", blueprint_app_profile_uuid)
    print("blueprint_app_profile_variables=", blueprint_app_profile_variables)

    for x in blueprint_app_profile_variables:
        if x['name'] == ''+vm_hostname+'':
            print("{}_var_uuid={}".format(vm_hostname, x['uuid']))
        else:
            continue
    exit(0)
else:
    print("Request failed")
    print("Headers: {}".format(headers))
    print('Status code: {}'.format(resp.status_code))
    print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
    exit(1)
# endregion
