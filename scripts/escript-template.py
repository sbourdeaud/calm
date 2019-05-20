# escript-template v20190520 / stephane.bourdeaud@nutanix.com
# ! Meant to be edited in VSCode with the BetterComments extension installed.

# * Conventions:
# 1. use all lower case for variable names.
# 2. when composing variable names, use underscore to separate words. Exp: username_secret. Use this same convention in Calm.
# 3. name sections with comments, comment line after the code.
# 4. don't print secrets, including tokens. Favor authentication (login/logout) in each script.
# 5. when saving your script, name it as the task name appears in Calm, using the following convention: NameOfIntegrationPoint-Verb-Text.py
# 6. use double quotes first, then single quotes.

# * Fill in this section with your information
#author:    <your email address here>
#version:   <date / notes>
#task_name: <enter the name of the task this script is for as it appears in your blueprint>

# * Capture variables here. This makes sure Calm macros are not referenced anywhere else in order to improve reusability.
username = '@@{credname.username}@@' #this is the username which will be used to make the API call
username_secret = "@@{credname.secret}@@" #this is the password for the username used to make the API call
api_server = "@@{endpoint_ip}@@" #this is the IP address of the API server

# Form method, url and headers for the API call
url     = "https://" + api_server + ":443/apis/batch/v1/"
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
method = "POST"

# Compose the json paylod
payload = {
  "apiVersion": "batch/v1",
  "kind": "Job",
  "metadata": {
    "name": "oscar-django-migrations-@@{calm_application_uuid}@@",
    "labels": {
      "app": "django",
      "component": "oscar",
      "tier": "frontend"
    }
  },
  "spec": {
    "template": {
      "metadata": {
        "labels": {
          "app": "django",
          "component": "oscar",
          "tier": "frontend"
        }
      },
      "spec": {
        "containers": [
          {
            "name": "django",
            "image": "michaelatnutanix/oscar_jet:latest",
            "imagePullPolicy": "Always",
            "command": [
              "/bin/bash",
              "migrate.sh"
            ],
            "env": [
              {
                "name": "DATABASE_USER",
                "value": "postgres"
              },
              {
                "name": "DATABASE_PASSWORD",
                "value": "@@{db_password}@@"
              },
              {
                "name": "DATABASE_HOST",
                "value": "@@{Era.DB_SERVER_IP}@@"
              },
              {
                "name": "DATABASE_NAME",
                "value": "@@{Era.DB_NAME}@@"
              },
              {
                "name": "ACCESS_KEY",
                "value": "@@{buckets_creds.username}@@"
              },
              {
                "name": "SECRET_ACCESS_KEY",
                "value": "@@{buckets_creds.secret}@@"
              },
              {
                "name": "STATIC_BUCKET",
                "value": "@@{buckets_name}@@"
              },
              {
                "name": "S3_ENDPOINT_URL",
                "value": "http://@@{buckets_ip}@@:7200/"
              }
            ]
          }
        ],
        "restartPolicy": "Never"
      }
    },
    "backoffLimit": 5
  }
}

# make the API call and capture the results in the variable called "resp"
resp = urlreq(url, verb=method, auth='BASIC', user=username, passwd=username_secret, params=json.dumps(payload), headers=headers)

# deal with the result/response
if resp.ok:
  print json.dumps(json.loads(resp.content), indent=4) #this prints the content of the response
else:
  print "Request failed", json.dumps(json.loads(resp.content), indent=4) #this prints the content of the response
  exit(1) #this makes sure the task will return as FALSE