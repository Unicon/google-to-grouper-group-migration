#!/usr/bin/python3
import httplib2
import configparser
import json
import os
import logging
import logging.config
import yaml

class grouperws:
    # charon(debug, env)
    #  debug = True/ False
    #  env = dev/ live
    def __init__(self, debug=False, env='dev'):
        config = configparser.ConfigParser()
        config.read('config/' + env +'_config.ini')

        logging.config.dictConfig(yaml.load(open('config/logging.conf', 'r')))
        self.logger = logging.getLogger(__name__)

        self.grouper_wsuri = config['ENV']['grouper_wsURI'] # Grouper WS URI and credentials
        self.grouper_username = config['ENV']['username']
        self.grouper_pwd = config['ENV']['password']
        self.stem = config['ENV']['attributes_stem']

        self.active_attrDefName = config['attributes']['active_attrDefName'].split(",") # A list of active attributes
        self.debug = config['debug'] # Debugging mode on/off.
        self.groupname = ''  # Current group name

        if self.debug:
            httplib2.debuglevel = 1

        self.http = httplib2.Http('.cache')
        self.http.add_credentials(name=self.grouper_username, password=self.grouper_pwd)

    # Get grouper subject membership details
    def grouperWSRequest(self, url, method="GET", body=''):
        """
        :param url: Request uri
        :param method: POST / GET / PUT
        :param body: json object
        :return: Json object grouper rest api
        """
        content_type = 'application/x-www-form-urlencoded'
        if method == "POST" or method == "PUT":
            content_type = 'text/x-json; charset=UTF-8'

        try:
            resp, content = self.http.request(uri=url,
                method=method,
                body=json.dumps(body),
                headers={'Content-Type': content_type})
            if resp.status == 200 or resp.status == 201:
                result = json.loads(content.decode('utf-8'))
                return result
        except httplib2.ServerNotFoundError as err:
            self.logger.warning("Error connecting to grouper: " + err)
            print("There has been en error, the request never succeeded.")
        return None

    # Get grouper attribute definitions.
    def grouperGroupSave(self, groupObject):

        """
        https://spaces.internet2.edu/display/Grouper/Group+Save
        :param subject: A dictionary returned from sqs message
        :return: json payload from grouper

        POST /grouper-ws/servicesRest/v2_2_000/groups HTTP/1.1
        POST /grouper-ws/servicesRest/v2_2_000/groups/aStem%3AaGroup HTTP/1.1
        """
        body = {
          "WsRestGroupSaveLiteRequest": {
            "actAsSubjectId": "GrouperSystem",
            "description": groupObject['description'],
            "displayExtension": groupObject['name'],
            "groupName": 'google:GoogleImports:' + str(groupObject['name'])
          }
        }
        # Grouper does not accept spaces in the url so we us the url special character "%20" to replace any spaces
        self.groupname = 'google:GoogleImports:' + groupObject['name']
        groupName = groupObject['name'].replace(' ', '%20')
        result = self.grouperWSRequest(self.grouper_wsuri + "/groups/google%3AGoogleImports%3A" + groupName, "POST", body)

        if not result['WsGroupSaveLiteResult']['resultMetadata']['success'] == "T":
            self.logger.warning("Unable to save group: " + str(groupObject['name']))
        else:
            self.logger.debug("new group created: %s", 'google:GoogleImports:' + str(groupObject['name']))

        return result

    def grouperAssignAttributes(self, groupName, attributes):
        """
        https://spaces.internet2.edu/display/Grouper/Assign+Attributes
        POST /grouper-ws/servicesRest/json/v2_2_000/attributeAssignments HTTP/1.1
        :param groupinfo:
        :param attributes:
        :return:
        """
        for attribute in attributes:
            if attribute in self.active_attrDefName:

                attributeName = self.stem + attribute
                attributeValue = attributes[attribute]

                body = {
                  "WsRestAssignAttributesLiteRequest":{
                    "actAsSubjectId": "GrouperSystem",
                    "attributeAssignOperation": "assign_attr",
                    "attributeAssignType": "group",
                    "wsAttributeDefNameName": attributeName,
                    "wsOwnerGroupName": groupName,
                    "attributeAssignValueOperation": "assign_value",
                    "valueSystem": attributeValue,
                  }
                }

                result = self.grouperWSRequest(self.grouper_wsuri + "/attributeAssignments", 'POST', body)

                if result and result['WsAssignAttributesLiteResults']['resultMetadata']['success'] == "T":
                    self.logger.debug("attribute: " + attributeName + " value: " + attributeValue + " assigned to %s", groupName)
                else:
                    self.logger.warning("Unable to assign attribute: " + attributeName + " to group: " + groupName)

        return result

    def grouperAddMember(self, groupName, subjectId):

        body = {
          "WsRestAddMemberRequest": {
            "actAsSubjectLookup": {
              "subjectId": "GrouperSystem"
            },
            "wsGroupLookup": {
                'groupName': groupName
            },
            "replaceAllExisting": "F",
            "subjectLookups": [
              {
                "subjectId": subjectId
              }
            ]
          }
        }
        result = self.grouperWSRequest(self.grouper_wsuri + "/groups/"+groupName+"/members", "PUT", body)

        self.logger.debug("Member: " + subjectId + " added to %s", groupName)

        return result

    def grouperGetSubject(self, subjectId):
        result = self.grouperWSRequest(self.grouper_wsuri + "/subjects/" + subjectId, 'GET')
        self.logger.debug("User: " + subjectId + " exists in grouper")
        return result

    def grouperGrantMemberGroupAdminPrivilege(self, groupName, subjectId):
        body = {
            "WsRestAssignGrouperPrivilegesLiteRequest": {
                "actAsSubjectId": "GrouperSystem",
                "allowed": "T",
                "groupName": groupName,
                "privilegeName": "admin",
                "privilegeType": "access",
                "subjectId": subjectId,
            }
        }
        result = self.grouperWSRequest(self.grouper_wsuri + "/grouperPrivileges", 'POST', body)
        self.logger.debug("Member: " + subjectId + " has been granted admin privilege for group %s", groupName)
        return result

    def grouperSaveMissingUser(self, groupName, subjectId, member):
        if not os.path.exists("unprocessed"):
                os.makedirs("unprocessed")

        with open('unprocessed/' + subjectId + '.json', 'w') as f:
            json.dump([{"groupName": groupName},{"memberInfo":member}], f, ensure_ascii=False)

            self.logger.warning("Member: " + subjectId + " not found in grouper and has been written to unprocessed/" + subjectId + ".json")