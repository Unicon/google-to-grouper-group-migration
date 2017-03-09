
This app is to be used to read google group information, settings and members.

## Functions:
1. Get all groups for this account and the group members. Merge the results and write each to the file system under groups/groupname.json

## Setup:
1. Go to https://console.developers.google.com/start
2. Log in and create a project and name you project. eg. "Google Migration To Grouper"
3. Under APIs & auth, click on Credentials and add OAuth 2.0 Client ID
4. Fill in the OAuth consent screen form
5. on the next screen, select other and input the name of you project
6. Close the dialog box, Download the JSON file of the credentials and save it to the root of this app
7. Run the app, the first time an oauth token will be retrived for future authentication and the client_secret.json file can be removed.

## Running app:
    python3 main.php


## RESOURCES:
    - [https://console.developers.google.com/flows/enableapi?apiid=admin](https://console.developers.google.com/flows/enableapi?apiid=admin)
    - [https://developers.google.com/admin-sdk/directory/v1/guides/manage-groups](https://developers.google.com/admin-sdk/directory/v1/guides/manage-groups)
  
  ### Authorization:
      - [https://developers.google.com/admin-sdk/directory/v1/guides/authorizing](https://developers.google.com/admin-sdk/directory/v1/guides/authorizing)       

  ### Required Scopes:
      - [https://www.googleapis.com/auth/admin.directory.group.readonly](https://www.googleapis.com/auth/admin.directory.group.readonly).
      - [https://www.googleapis.com/auth/admin.directory.group.member.readonly](https://www.googleapis.com/auth/admin.directory.group.member.readonly).
      - [https://www.googleapis.com/auth/apps.groups.settings](https://www.googleapis.com/auth/apps.groups.settings).
  
  ### All google Supported api:
      - [https://developers.google.com/api-client-library/python/apis/](https://developers.google.com/api-client-library/python/apis/)
  
  ### Group directory_v1 api:
      - [https://developers.google.com/resources/api-libraries/documentation/admin/directory_v1/python/latest/](https://developers.google.com/resources/api-libraries/documentation/admin/directory_v1/python/latest/)
      
      
  ## API Endpoint Implemented:
    #### Retrieve all groups for a domain or the account:
        - GET https://www.googleapis.com/admin/directory/v1/groups?domain=domain name&customer=my_customer or customerId&pageToken=pagination token &maxResults=max results
    #### Retrieving settings for a group:
        - GET https://www.googleapis.com/groups/v1/groups/group email address
    #### Members:
        - GET https://www.googleapis.com/admin/directory/v1/groups/groupKey/members?pageToken=pagination token&roles=one or more of OWNER,MANAGER,MEMBER separated by a comma&maxResults=maximum results per response page