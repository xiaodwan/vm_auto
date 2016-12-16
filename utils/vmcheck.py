import time
import commands
import re

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

