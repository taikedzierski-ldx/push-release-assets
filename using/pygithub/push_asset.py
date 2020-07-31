#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pprint
import os
import sys
import zipfile
from github import Github

# Use a local_creds.py
#   see _loacl_creds.py for an example
import local_creds

# Mock out the args parse parser details
class ArgsInstances:

    def __init__(self):
        self.release_tagname = sys.argv[1]
        self.upload_path = sys.argv[2]

class MockedFreya:

    # mock - do not include
    def __init__(self):
        # can take arguments of username and password, or PAT, or empty for unauthenticated
        auth = local_creds.getUser("taikedzierski-ldx")
        git = Github(*auth)
        self.repo = git.get_repo("taikedzierski-ldx/push-release-assets")



## FUNCTIONS FOR EXPORTING

    def __get_release(self, releases_list, tag_name):
        """ Lookup a release by name in a PaginatedList of GithubRelease-s

        @param release_list - a list of GithubRelease objects
        @param tab_name - string representing the exact release tag name to upload onto

        @raises KeyError - if release tag name is not found in the list of releases
        """
        for release in releases_list:
            if release.tag_name == tag_name:
                return release
        raise KeyError("Could not fine release with tag name '%s'" % tag_name)

    def __zip_folder(self, folder_path):
        """ Combine a folder into a ZIP file

        @param folder_path - a path string to the folder

        @returns the path to the created ZIP file
        """
        # Strip final dir separator, or name detection will be broken
        if folder_path[-1] in [os.path.sep, '/', '\\']:
            folder_path = folder_path[:-1]

        parent_path = os.path.dirname(os.path.abspath(folder_path) )
        base_name = os.path.basename(folder_path)

        zip_name = base_name + ".zip"
        zip_path = os.path.sep.join([parent_path, zip_name])

        print("Writing "+zip_path)

        with zipfile.ZipFile(zip_path, "w") as zip_handler:
            for root, directories, files in os.walk(folder_path):
                for file_subpath in files:
                    zip_handler.write( os.path.sep.join([root, file_subpath]) )
        return zip_path

    def __require_arg(self, flagname):
        if not hasattr(args, flagname):
            raise argparse.ArgumentError("--%s not specified" % (flagname))

    def publish_asset(self):
        """ Publish an asset to Github

        Options are pulled from arguments:
        --release_tagname
        --upload_path
        """

        self.__require_arg("release_tagname")
        self.__require_arg("upload_path")

        file_to_upload = None
        if os.path.exists(args.upload_path):
            if os.path.isfile(args.upload_path):
                file_to_upload = args.upload_path

            elif os.path.isdir(args.upload_path):
                file_to_upload = self.__zip_folder(args.upload_path)
        else:
            raise OSError("The specified path '%s' was not found in <%s>" % (args.upload_path, os.getcwd()) )

        releases = self.repo.get_releases()
        release = self.__get_release(releases, args.release_tagname)
        release.upload_asset(file_to_upload)

# =====
args = None
def main():
    global args
    args = ArgsInstances()
    mf = MockedFreya()
    mf.publish_asset()

if __name__ == "__main__":
    main()
