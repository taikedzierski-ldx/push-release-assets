#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pprint
import os
from sys import argv as args
from github import Github

# Use a local_creds.py
#   see _loacl_creds.py for an example
import local_creds

pp = pprint.PrettyPrinter(indent=2)

def printdir(item):
    for keyname in dir(item):
        data = getattr(item, keyname)
        print("[36;1m%s : (%s) -----------[0m" % (keyname, type(data) ) )
        if type(data) is list or type(data) is dict:
            pp.pprint(data)
        else:
            print "\t",
            print( str(data) )
        print("")

# can take arguments of username and password, or PAT, or empty for unauthenticated
auth = local_creds.getUser("taikedzierski-ldx")
g = Github(*auth)


repo = g.get_repo("taikedzierski-ldx/push-release-assets")

releases = repo.get_releases()

if "-p" in args:
    print("Releases:")

    for item in releases:
        printdir(item)
else:
    asset_id = int(args[1])
    item = args[2]
    if os.path.exists(item) and os.path.isfile(item):
        first_release = releases[0]
        first_release.upload_asset(item, label=args[3]) # upload_asset(path, label='', content_type=NotSet, name=NotSet)
