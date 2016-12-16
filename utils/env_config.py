#!/usr/bin/env python

"""
Configure default values when scripts are running.
For example: guest name, tree url, kickstart url, etc.
"""
from ConfigParser import ConfigParser

SECTION1 = 'Installation'
SECTION2 = 'storage_pool'
SECTION3 = 'debug'
SECTION4 = 'checkpoint'

def create_default_config():
    config = ConfigParser()
    # Installation
    config.add_section(SECTION1)
    config.set(SECTION1, 'url',
               "http://download.eng.pek2.redhat.com/pub/rhel/released/RHEL-7/7.3/Server/x86_64/os/")
    config.set(SECTION1, 'ks',
               "http://fileshare.englab.nay.redhat.com/pub/section3/run/http-ks/ks-rhel7u3-x86_64.cfg")
    config.set(SECTION1, 'guestname', "_ui_autotest")
    config.set(SECTION1, 'cpu', "1")
    config.set(SECTION1, 'memory', "1024")
    # disk size, unit is G.
    config.set(SECTION1, 'size', "8")
    config.set(SECTION1, 'path', "/var/lib/libvirt/images")
    config.set(SECTION1, 'images', "/var/lib/libvirt/images/_ui_autotest.img")
    config.set(SECTION1, 'firmware', "BIOS")
    config.set(SECTION1, 'chipset', "i440FX")

    # storage pool
    config.add_section(SECTION2)
    config.set(SECTION2, 'type', "dir")
    config.set(SECTION2, 'name', "autotestpool")

    # debug
    config.add_section(SECTION3)
    config.set(SECTION3, 'readcfgfromfile', "True")

    # CheckPoint
    config.add_section(SECTION4)
    # os version is now updated manually for every os tree.
    # will improve and auto detect in future.
    config.set(SECTION4, 'osversion', "Red Hat Enterprise Linux 7.3")

    try:
        with open('./autotest.cfg', 'wb') as configfile:
            config.write(configfile)
    except:
        raise

def get_config_value(section, option):
    config = ConfigParser()
    try:
        config.readfp(open('./autotest.cfg'))
    except IOError:
        create_default_config()
        config.readfp(open('./autotest.cfg'))

    return config.get(section, option)

def get_config_bool_value(section, option):
    config = ConfigParser()
    try:
        config.readfp(open('./autotest.cfg'))
    except IOError:
        create_default_config()
        config.readfp(open('./autotest.cfg'))

    return config.getboolean(section, option)

if __name__ == '__main__':
    create_default_config()
