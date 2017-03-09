grouperSession = GrouperSession.startRootSession();
addStem("etc:attribute", "provisioningTargets", "Provisioning Targets")

addStem("etc:attribute:provisioningTargets", "google", "Google")
attributeStem = StemFinder.findByName(GrouperSession.staticGrouperSession(), "etc:attribute:provisioningTargets:google", true);
attrDef = attributeStem.addChildAttributeDef("googleProvisioningTargetDef", AttributeDefType.attr);
attrDef.setAssignToGroup(true);
attrDef.setValueType(AttributeDefValueType.string);
attrDef.store();

attrDefName = attributeStem.addChildAttributeDefName(attrDef,  "email", "mail Address");
attrDefName.setDescription("The email address to associate with the Google Group.");
attrDefName.store();
attrDefName = attributeStem.addChildAttributeDefName(attrDef,  "replyTo", "Reply Email Address");
attrDefName.setDescription("The Email address that can be replied to.");
attrDefName.store();
attrDefName = attributeStem.addChildAttributeDefName(attrDef,  "whoCanLeaveGroup", "Who Can Leave Group");
attrDefName.setDescription("Who can leave this group.");
attrDefName.store();
attrDefName = attributeStem.addChildAttributeDefName(attrDef,  "whoCanContactOwner", "Who Can Contact Owner");
attrDefName.setDescription("Who can contact the group owner.");
attrDefName.store();
attrDefName = attributeStem.addChildAttributeDefName(attrDef,  "allowWebPosting", "Allow Web Posting");
attrDefName.setDescription("Allow to post on the web.");
attrDefName.store();
attrDefName = attributeStem.addChildAttributeDefName(attrDef,  "whoCanInvite", "Who Can Invite");
attrDefName.setDescription("Who can invite members.");
attrDefName.store();
attrDefName = attributeStem.addChildAttributeDefName(attrDef,  "allowExternalMembers", "Allow External Memmbers");
attrDefName.setDescription("Allow external members to join this group.");
attrDefName.store();
attrDefName = attributeStem.addChildAttributeDefName(attrDef,  "spamModerationLevel", "Spam Moderation Level");
attrDefName.setDescription("The spam moderation level of the group.");
attrDefName.store();
attrDefName = attributeStem.addChildAttributeDefName(attrDef,  "whoCanPostMessage", "Who Can Post");
attrDefName.setDescription("Who can post message in this group.");
attrDefName.store();
attrDefName = attributeStem.addChildAttributeDefName(attrDef,  "includeInGlobalAddressList", "Include Global Address List");
attrDefName.setDescription("Include global address list to this group.");
attrDefName.store();
attrDefName = attributeStem.addChildAttributeDefName(attrDef,  "whoCanViewMembership", "Who Can View Membership");
attrDefName.setDescription("Who can view membership in this group.");
attrDefName.store();
attrDefName = attributeStem.addChildAttributeDefName(attrDef,  "whoCanViewGroup", "Who Can View Group");
attrDefName.setDescription("Who can view this group.");
attrDefName.store();
attrDefName = attributeStem.addChildAttributeDefName(attrDef,  "sendMessageDenyNotification", "Send Deny Notification");
attrDefName.setDescription("Send message deny notification to sender.");
attrDefName.store();
attrDefName = attributeStem.addChildAttributeDefName(attrDef,  "showInGroupDirectory", "Show In Group Directory");
attrDefName.setDescription("Show this group in group directory.");
attrDefName.store();
attrDefName = attributeStem.addChildAttributeDefName(attrDef,  "customReplyTo", "Custom Reply To");
attrDefName.setDescription("Custom reply to email.");
attrDefName.store();
attrDefName = attributeStem.addChildAttributeDefName(attrDef,  "allowGoogleCommunication", "Allow Google Communication");
attrDefName.setDescription("Allow Google Communication.");
attrDefName.store();
attrDefName = attributeStem.addChildAttributeDefName(attrDef,  "whoCanJoin", "Who Can Join");
attrDefName.setDescription("Who can join this group.");
attrDefName.store();
attrDefName = attributeStem.addChildAttributeDefName(attrDef,  "maxMessageBytes", "Max Message Bytes");
attrDefName.setDescription("Maximum size of message for the group in bytes.");
attrDefName.store();

addRootStem("google", "Google");
addStem("google", "GoogleImports", "Google Imports")
