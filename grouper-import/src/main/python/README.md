This app is to be used to parse google groups .json files from "groups/" directory, into grouper groups, attributes and users.
    - If a user is not found in grouper, a file is created with the username in the "unprocessed/" directory.
    - Grouper usernames are derived from the first part of the google user email address separated by "@"

## Running app:
    python3 main.py

## Logging
    - Logging is controlled through `config/logging.conf

## Grouper web services implemented:
    1. https://spaces.internet2.edu/display/Grouper/Group+Save
    2. https://spaces.internet2.edu/display/Grouper/Assign+Attributes
    3. https://spaces.internet2.edu/display/Grouper/Get+Subjects
    4. https://spaces.internet2.edu/display/Grouper/Add+Member
    5. https://spaces.internet2.edu/display/Grouper/Add+or+remove+grouper+privileges

## Groups with valid users
    cbit_group,
    class-1-group,
    cm,
    collabinbox-test-group,
    core-middleware-test-2-g,
    derek-test-shared-mailboxgroup-g,
    dereks-ee-gorups-123-cc-derek_stansadad-g,
    dereks-new-group,
    going-google-early-adopters-group,
    going-google-early-adopters-mcob-group,
    jameslitholdtest-group,
    johnk-testgroup-group,
    nd-office-of-information-technologies-group