#region headers
    # posh-api-template v20190521 / stephane.bourdeaud@nutanix.com
    # ! Meant to be edited in VSCode with the BetterComments extension installed
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
    # * anywhere else in order to improve reusability.
    $username = '@@{credname.username}@@' #this is the username which will be
                                          #used to make the API call
    $username_secret = "@@{credname.secret}@@" #this is the password for the
                                               #username used to make the API
                                               #call
    $api_server = "@@{endpoint_ip}@@" #this is the IP address of the API server
#endregion

#region prepare api call
    $api_server_port = "443" #this is the TCP port used to access the API server
    $api_server_endpoint = "/apis/batch/v1/" #this is the address of the API
                                             #endpoint
    $url = "https://{0}:{1}{2}" -f $api_server,$api_server_port, `
        $api_server_endpoint #this is the url which will be used to make the API
                             #call
    $secpasswd = ConvertTo-SecureString $username_secret -AsPlainText -Force
    $cred = New-Object System.Management.Automation.PSCredential ($username, `
        $secpasswd)
    $headers = @{
        "Content-Type"="application/json";
        "Accept"="application/json"
    } #those are the headers which will be used to make the API call
    $method = "POST" #this is the method which will be used for the API call
#endregion

#region prepare the json payload
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
    try {#using a try;catch;finally statement to process errors correctly
        $resp = Invoke-RestMethod -Credential $cred -Method $method -Uri `
            $url -Headers $headers -Body $payload -SkipCertificateCheck `
            -SslProtocol Tls12 -ErrorAction Stop #this makes the API call. Get
                                                 #rid of -SkipCertificateCheck
                                                 #if you're using proper
                                                 #certificates.
        Write-Host $resp.content #print the results
    }
    catch {#something went wrong
        ThrowError -ExceptionMessage "$(get-date) [ERROR] `
            $($_.Exception.Message)" #we're printing the content of the error
                                     #and throwing an exception
    }
    finally {
        #add any last words here; this gets processed no matter what
    }
#endregion