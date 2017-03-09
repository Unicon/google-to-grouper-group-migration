#!/usr/bin/python3
import os
import glob
import configparser
import json

"""
    Load file
    Move it to processing queue
    process the file
        if successful, then delete the file
        if failure, then move the file back to the original location

    Open each file
    Read file contents
        Group Settings information
        Users information

    Create group
    Check group attributes against grouper attributes
    If attributes excists, then add them to the group
    Get all users in the google group and create users for the grouper group
"""
class google:

    def __init__(self, debug=False, env='dev'):
        config = configparser.ConfigParser()

        config.read('config/' + env +'_config.ini')

        self.FILES_DIRECTORY=config['files']['files_dir']

    def getFiles(self):
        files = glob.glob(self.FILES_DIRECTORY+"/*.json")
        return files

    def loadGroupFile(self, filename):
        if os.path.exists(filename):
                try:
                    with open(filename, 'r') as f:
                        file_content = json.load(f)
                        return file_content
                except:
                    print("Could not read file: %s", filename)