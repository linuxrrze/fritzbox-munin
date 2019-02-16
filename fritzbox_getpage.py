#!/usr/bin/env python
"""
  fritzbox_getpage - A helper tool to download webpages
  Like Munin, this plugin is licensed under the GNU GPL v2 license
  http://www.opensource.org/licenses/GPL-2.0
  Add the following section to your munin-node's plugin configuration:

  Call it like:
  ./fritzbox_getpage \
  fritzbox_ip=[ip address of the fritzbox] \
  fritzbox_username=[fritzbox username] \
  fritzbox_password=[fritzbox password] \
  [fritzbox url path]
  
"""

import os
import sys
import fritzbox_helper as fh

PAGE = sys.argv[1]

def get_page():
    """download and print fritzbox page """

    server = os.environ['fritzbox_ip']
    username = os.getenv('fritzbox_username', "None")
    password = os.environ['fritzbox_password']

    sid = fh.get_sid(server, username, password)
    data = fh.get_page(server, sid, PAGE)
    print data

if __name__ == '__main__':
    try:
        get_page()
    except:
        sys.exit("Couldn't retrieve page from fritzbox")
