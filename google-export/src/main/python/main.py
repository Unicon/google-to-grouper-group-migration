#!/usr/bin/python3
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import json

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# account domain
DOMAIN = 'test.example.edu'

SCOPES = 'https://www.googleapis.com/auth/admin.directory.group.readonly ' \
         'https://www.googleapis.com/auth/admin.directory.group.member.readonly ' \
         'https://www.googleapis.com/auth/apps.groups.settings'

# Credential file
CLIENT_SECRET_FILE = 'client_secret.json'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'google-migration.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def getGroups(http):
    """
    Retrieve all groups for a domain or the account:

    Calls a Google Admin-SDK Directory API: Groups service object and outputs a
    all groups in an account identified by the domain.
    """
    data = {}
    service = discovery.build('admin', 'directory_v1', http=http)
    try:
        results = service.groups().list(domain=DOMAIN, alt='json').execute()

        if len(results['groups']):
            for group in results['groups']:
                filename = group['email'].split("@")[0]
                data.update({filename: group})

        return data
    except:
        print('Unable to read groups from domain: {0}'.format(DOMAIN))
        raise

def getGroupMembers(groupEmail,http):
    """
    Retrieve all group members:

    Calls a Google Admin-SDK Directory API: Group Members service object and outputs a
    all members of the group identified by the group's email address.
    """
    service = discovery.build('admin', 'directory_v1', http=http)
    try:
        results = service.members().list(groupKey=groupEmail, pageToken=None, maxResults=None, roles=None).execute()
        if len(results):
            print(json.dumps(results, indent=4))
            return results
    except:
        print('Unable to read members for group: {0}'.format(groupEmail))
        raise

def getGroupSettings(groupEmail,http):
    """
    Retrieving settings for a group:

    Calls a Google Admin-SDK Groups Settings API service object and outputs a
    group's settings identified by the group's email address.
    """
    service = discovery.build('groupssettings', 'v1', http=http)
    try:
        results = service.groups().get(groupUniqueId=groupEmail, alt='json').execute()
        if len(results):
            print(json.dumps(results, indent=4))
            return results
    except:
        print('Unable to read group: {0}'.format(groupEmail))
        raise

def writeRecordToFile(filename, data):
    # Make sure we have the folder to wright the files to
    if not os.path.exists("groups"):
        os.makedirs("groups")

    with open('groups/' + filename + '.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def main():
    print("****** Starting ******")
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    groups_info = getGroups(http)
    if len(groups_info) > 0:
        for groupName in groups_info:
            data = {'groupInfo': groups_info[groupName]}

            groupEmail = groups_info[groupName]['email']

            groupSettings = getGroupSettings(groupEmail, http)
            data.update({'groupSettings': groupSettings})

            groupMembers = getGroupMembers(groupEmail, http)
            if groupName:
                if groupMembers:
                    data.update({'groupMembers': groupMembers})

                writeRecordToFile(groupName, data)
    print("****** Finished ******")

if __name__ == '__main__':
    main()