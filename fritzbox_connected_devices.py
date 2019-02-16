#!/usr/bin/env python
"""
  fritzbox_connected_devices - A munin plugin for Linux to monitor AVM Fritzbox
  Copyright (C) 2015 Christian Stade-Schuldt
  Author: Christian Stade-Schuldt
  Like Munin, this plugin is licensed under the GNU GPL v2 license
  http://www.opensource.org/licenses/GPL-2.0
  Add the following section to your munin-node's plugin configuration:

  [fritzbox_*]
  env.fritzbox_ip [ip address of the fritzbox]
  env.fritzbox_username [fritzbox username]
  env.fritzbox_password [fritzbox password]
  
  This plugin supports the following munin configuration parameters:
  #%# family=auto contrib
  #%# capabilities=autoconf
"""

import os
import re
import sys
# pip install git+https://github.com/SirAnthony/slpp
from slpp import slpp as lua
import fritzbox_helper as fh

PAGE = '/net/network_user_devices.lua'
LUA_DATA='MQUERIES'
pattern = re.compile('^'+LUA_DATA+'\s*=\s*({.*^\})', re.DOTALL | re.MULTILINE)

# bet box name from first part before '_' in (symlink) file name
boxname = os.path.basename(__file__).rsplit('_')[0]


def get_connected_devices():
    """gets the number of currently connected devices"""

    server = os.environ['fritzbox_ip']
    username = os.getenv('fritzbox_username', "None")
    password = os.environ['fritzbox_password']

    sid = fh.get_sid(server, username, password)
    data = fh.get_page(server, sid, PAGE)

    m = re.search(pattern, data)
    lua_answer = m.group(1)

    lua_dec = lua.decode(lua_answer)

    lan_devices = 0
    wlan_devices = 0

    for key in lua_dec.keys():
        if key.startswith('landevice:settings/landevice/list'):
            #print key, ":", lua_dec[key]
            for device in lua_dec[key].keys():
                #print lua_dec[key][device]
                if lua_dec[key][device]['wlan'] == '1' and lua_dec[key][device]['active'] == '1':
                    wlan_devices += 1
                if lua_dec[key][device]['ethernet'] == '1' and lua_dec[key][device]['active'] == '1':
                    lan_devices += 1
    print 'wlan.value %d' % wlan_devices
    print 'lan.value %d' % lan_devices


def print_config():
    print "host_name %s" % boxname
    print 'graph_title AVM Fritz!Box Connected Devices'
    print 'graph_vlabel Number of connected devices'
    print 'graph_args --base 1000'
    print 'graph_category network'
    print 'graph_order wlan'
    print 'wlan.label Wifi connections'
    print 'wlan.type GAUGE'
    print 'wlan.graph LINE1'
    print 'wlan.info Wifi connections'
    print 'lan.label LAN connections'
    print 'lan.type GAUGE'
    print 'lan.graph LINE1'
    print 'lan.info LAN connections'


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        print_config()
    elif len(sys.argv) == 2 and sys.argv[1] == 'autoconf':
        print 'yes'
    elif len(sys.argv) == 1 or len(sys.argv) == 2 and sys.argv[1] == 'fetch':
        # Some docs say it'll be called with fetch, some say no arg at all
        try:
            get_connected_devices()
        except:
            sys.exit("Couldn't retrieve connected fritzbox devices")


