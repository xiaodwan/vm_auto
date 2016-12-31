import re
import os
import time
import urllib
import inspect
import commands

import xml.etree.ElementTree as ET
from getpass import getuser

VIRT_MANAGER_LOG = "~/.cache/virt-manager/virt-manager.log"

def get_vm_lifecycle_time(cmd):
    ret, output = commands.getstatusoutput(cmd)
    if output:
        res = re.search('\[(.*) virt-manager [0-9]+\]', output)
        timestr = res.group(1)
    else:
        return None

    lifecyle_time = time.mktime(time.strptime(timestr, "%a, %d %b %Y %H:%M:%S"))
    return lifecyle_time 

def check_vm_install_complete(pid, domain_name):
    cmd = "grep 'virt-manager %s].*domain lifecycle event: domain=%s' "\
          %(pid, domain_name) + VIRT_MANAGER_LOG + " | tail -1"

    oldtime = get_vm_lifecycle_time(cmd)

    if oldtime is None:
        print "Error: doesn't find vm event in log file"
        exit(1)

    # time out after 30 mins
    times = 1800/3
    i = 1

    newtime = get_vm_lifecycle_time(cmd)
    while oldtime >= newtime:
        time.sleep(3)
        newtime = get_vm_lifecycle_time(cmd)
        if i > times:
            return False
        i+=1

    return True

def get_vm_mac(domain):
    cmd = "virsh dumpxml " + domain + " | grep 'mac address'"
    ret, output = commands.getstatusoutput(cmd)

    return output.split('\'')[1]

def get_vm_ip(mac, network='default'):
    # virsh net-dhcp-leases default
    cmd = "virsh net-dhcp-leases " + network + " | grep " + mac
    ret, output = commands.getstatusoutput(cmd)

    return output.split('/')[0].split()[-1]

def ping_vm(domain):
    mac = get_vm_mac(domain)
    ip = get_vm_ip(mac)

    i = 1

    cmd = "ping -c 3 " + ip

    # time out after 5 mins
    while i<=30:
        ret, output = commands.getstatusoutput(cmd)
        if ret == 0:
            return True
        time.sleep(10)

    return False


def get_default_img_path():
    cmd = 'virsh pool-dumpxml default'
    ret, output = commands.getstatusoutput(cmd)

    if ret != 0:
        path = os.path.expanduser("~/.local/share/libvirt/images/")
        return path

    root = ET.fromstring(output)
    path = root.find(".//path").text

    if not path.strip().endswith('/'):
        path = path + '/'

    return path

def get_default_uri():
    if getuser() == "root":
        return "qemu:///system"
    else:
        return "qemu:///session"

def get_default_connection(uri=None):
    if uri is None:
        return None

    if uri == "qemu:///system":
        return 'QEMU/KVM'
    elif uri == "qemu:///session":
        return 'QEMU/KVM User session'
    else:
        return None


def check_bug_fixed(bugid):

    url = "https://bugzilla.redhat.com/buglist.cgi?f1=bug_id&f2=bug_status&o1=equals&o2=anywords&query_format=advanced&v1=" + \
          "%s" % bugid + "&v2=ON_QA%20VERIFIED%20RELEASE_PENDING%20CLOSED%20"
    f = urllib.urlopen(url)
    res = re.search("No results were found that matched your query", f.read())
    f.close()

    if res is None:
        return True
    else:
        return False


def get_current_function_name():
        return inspect.stack()[1][3]
