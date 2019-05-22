#region headers
# posh-api-template v20190522 / stephane.bourdeaud@nutanix.com
# ! Meant to be edited in VSCode w/ the BetterComments extension installed
# ! Do NOT delete comments from this script!

# * Conventions:
# 1. use all lower case for variable names.
# 2. when composing variable names, use underscore to separate words. 
#    Exp: username_secret. Use this same convention in Calm.
# 3. name sections with comments, comment line after the code.
# 4. don't print secrets, including tokens. Favor authentication 
#    (login/logout) in each script.
# 5. when saving your script, name it as the task name appears in Calm,
#    using the following convention: NameOfIntegrationPoint-Verb-Text.ps1
# 6. use double quotes first, then single quotes.

# TODO Fill in this section with your information
# author:    <your email address here>
# version:   <date / notes>
# task_name: <enter the name of the task as it appears in your bp>
#endregion

#region capture Calm variables
# * Capture variables here. This makes sure Calm macros are not referenced 
# * anywhere else in order to improve maintainability.
$username = '@@{credname.username}@@'
$username_secret = "@@{credname.secret}@@"
$api_server = "@@{endpoint_ip}@@"
#endregion

#region prepare api call
$api_server_port = "443"
$api_server_endpoint = "/apis/batch/v1/"
$url = "https://{0}:{1}{2}" -f $api_server,$api_server_port, `
    $api_server_endpoint

# take the clear text password, convert it and put user and secret in a
# credential object (generally more secure)
$secpasswd = ConvertTo-SecureString $username_secret -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential ($username, `
    $secpasswd)

$headers = @{
    "Content-Type"="application/json";
    "Accept"="application/json"
}
$method = "POST"

$content = @{
    property1="value";
    property2=@{
        property21="value";
        property22="value"
    };
    property3="value"
} #this is used to capture the content of the payload
$payload = (ConvertTo-Json $content -Depth 4) #this converts the payload to 
                                                #proper json format
#endregion

#region make api call
try {
    # ! Get rid of -SkipCertificateCheck if you're using proper
    # ! certificates
    $resp = Invoke-RestMethod -Credential $cred -Method $method -Uri `
        $url -Headers $headers -Body $payload -SkipCertificateCheck `
        -SslProtocol Tls12 -ErrorAction Stop
    Write-Host $resp.content
}
catch {
    ThrowError -ExceptionMessage "$(get-date) [ERROR] `
        $($_.Exception.Message)"
}
finally {
    #add any last words here; this gets processed no matter what
}
#endregion