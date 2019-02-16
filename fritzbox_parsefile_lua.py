#!/usr/bin/env python
"""
  fritzbox_getpage - A helper tool to download webpages
  Like Munin, this plugin is licensed under the GNU GPL v2 license
  http://www.opensource.org/licenses/GPL-2.0
  Add the following section to your munin-node's plugin configuration:

  Call it like:
  ./fritzbox_parsefile_lua.py filename
"""

import os
import sys
import re
# pip install git+https://github.com/SirAnthony/slpp
from slpp import slpp as lua

filename = sys.argv[1]

LUA_DATA='MQUERIES'
pattern = re.compile('^'+LUA_DATA+'\s*=\s*({.*^\})', re.DOTALL | re.MULTILINE)

def get_page():
    """parses lua part of lua page"""

    file = open(filename, "r")
    data = file.readlines()
    file.close()
    data = ''.join(data)
    # DEBUG: print data

    m = re.search(pattern, data)
    lua_answer = m.group(1)

    # DEBUG: print lua_answer

    lua_dec = lua.decode(lua_answer)
    # DEBUG: print lua_dec
    return lua_dec

if __name__ == '__main__':
    lan_devices = 0
    wlan_devices = 0
    try:
        data = get_page()
        for key in data.keys():
            if key.startswith('landevice:settings/landevice/list'):
               print key, ":", data[key]
               for device in data[key].keys():
                   print    data[key][device]['active'],        \
                            data[key][device]['ethernet'],      \
                            data[key][device]['wlan'],          \
                            data[key][device]['mac'],           \
                            data[key][device]['ethernet_port'], \
                            data[key][device]['ipv6_ifid'],     \
                            data[key][device]['speed'],         \
                            data[key][device]['name']
                   if data[key][device]['wlan'] == '1' and data[key][device]['active'] == '1':
                        wlan_devices += 1
                   if data[key][device]['ethernet'] == '1' and data[key][device]['active'] == '1':
                        lan_devices += 1
        print lan_devices
        print wlan_devices
              
    except Exception, e:
        print e
        sys.exit("Couldn't parse page from fritzbox")
