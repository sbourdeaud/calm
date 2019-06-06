# region headers
# escript-template v20190605 / stephane.bourdeaud@nutanix.com
# * author:       igor.zecevic@nutanix.com
# * version:      2019/06/05
# task_name:      CalmLaunchBp
# description:    This script launches the specified Calm blueprint with the
# specified application profile. You will need to edit the variable_list section
# of the json payload in the "REST call: Launch Blueprint" region with
# your list of variables an values defined in your application profile.
# TODO: deal with non default app profile name
# TODO: test
# endregion

# region capture Calm macros
pc_ip = '@@{pc_ip}@@'
username = '@@{pc_user.username}@@'
username_secret = '@@{pc_user.secret}@@'
blueprint_uuid = "@@{blueprint_uuid}@@"
blueprint_app_name = "VM-@@{blueprint_name}@@"
blueprint_app_profile_uuid = '@@{blueprint_app_profile_uuid}@@'
vm_hostname_var_uuid = '@@{vm_hostname_var_uuid}@@'
vm_hostname_value = '@@{vm_hostname}@@'
# endregion

# region prepare variables
headers = {'content-type': 'application/json'}
# endregion

# region REST call: Launch Blueprint
method = 'POST'
url = "https://{}:9440/api/nutanix/v3/blueprints/{}/launch".format(
    pc_ip,
    blueprint_uuid
)
print("Making a {} API call to {}".format(method, url))
payload = {
    "api_version": "3.0",
    "metadata": {
        "uuid": ""+blueprint_uuid+"",
        "kind": "blueprint"
    },
    "spec": {
        "application_name": ""+blueprint_app_name+"",
        "app_profile_reference": {
            "kind": "app_profile",
            "uuid": ""+blueprint_app_profile_uuid+""
        },
        "resources": {
            "app_profile_list": [
                {
                    "name": "Default",
                    "uuid": ""+blueprint_app_profile_uuid+"",
                    "variable_list": [
                        {
                            "name": "vm_hostname",
                            "value": ""+vm_hostname_value+"",
                            "uuid": ""+vm_hostname_var_uuid+""
                        }
                    ]
                }
            ]
        }
    }
}
resp = urlreq(
    url,
    verb=method,
    params=json.dumps(payload),
    headers=headers,
    auth="BASIC",
    user=username,
    passwd=username_secret,
    verify=False
)

if resp.ok:
    json_resp = json.loads(resp.content)
    print("Blueprint {} was launched successfully".format(blueprint_uuid))
    print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
    exit(0)
else:
    print("Request failed")
    print("Headers: {}".format(headers))
    print("Payload: {}".format(json.dumps(payload)))
    print('Status code: {}'.format(resp.status_code))
    print('Response: {}'.format(json.dumps(json.loads(resp.content), indent=4)))
    exit(1)

# endregion
