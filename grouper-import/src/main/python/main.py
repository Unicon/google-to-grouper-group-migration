#!/usr/bin/python3
from adaptors.google import google
from adaptors.grouper import grouperws

def main():
    print("*** Starting ***");

    google_groups = google(False, 'dev')
    grouper = grouperws(False, 'dev')
    files = google_groups.getFiles()

    for file in files:
        file_contents = google_groups.loadGroupFile(file)

        newGroup = grouper.grouperGroupSave(file_contents['groupSettings'])

        if newGroup:
            # Assign group and update attributes
            addAttributes = grouper.grouperAssignAttributes(grouper.groupname, file_contents['groupSettings'])

            if "members" in file_contents['groupMembers']:
                for member in file_contents['groupMembers']['members']:

                    subjectId = member['email'].split("@")[0]

                    subjectExists = grouper.grouperGetSubject(subjectId)

                    if subjectExists and subjectExists['WsGetSubjectsResults']['wsSubjects'][0]['success'] == "T":

                        addMember = grouper.grouperAddMember(grouper.groupname, subjectId)

                        if addMember and addMember['WsAddMemberResults']['results'][0]['resultMetadata']['success']:

                            # Update user privilege
                            if member['role'] == "OWNER":

                                update_privileges = grouper.grouperGrantMemberGroupAdminPrivilege(grouper.groupname, subjectId)
                                if not update_privileges:
                                    grouper.logger.warning("Unable to assign admin privilege to " + subjectId)
                        else:
                            grouper.logger.warning("Unable to add member to " + grouper.groupname + ". The user may not be in grouper")
                    else:
                        grouper.grouperSaveMissingUser(grouper.groupname, subjectId, member)
    print("*** finished ***")


if __name__ == '__main__':
    main()