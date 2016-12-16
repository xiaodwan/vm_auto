from env_config import *


if get_config_bool_value('debug', 'readcfgfromfile') is True:
    print "success"
else:
    print "Failure"
