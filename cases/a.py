conform_items = { 
                            "Force Poweroff" : 0,
                            "Poweroff/Reboot/Save" : 0,
                            "Pause" : 0,
                            "Interface start/stop" : 1,
                            "Device removal" : 0,
                            "Unapplied changes" : 1,
                            "Deleting storage" : 0 
                        }

try:
    raise ValueError("haha")
except Exception, e:
    print e.__class__
    print e.__dict__
    print e.message
