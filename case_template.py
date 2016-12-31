import sys
import unittest

from getpass import getuser
from dogtail.utils import screenshot

if __name__ == '__main__':
    sys.path.insert(0, '..')

from utils.env_config import *
from utils.logging import *
from utils.uiutils import *
from utils.dogtailutils import *
from utils.generalutils import *

DEFAULT_URI = get_default_uri()
DEFAULT_CONNECTION = get_default_connection(DEFAULT_URI)
DEFAULT_PATH = get_default_img_path()
DEFAULT_POOLNAME = "autotestdir"

if get_config_bool_value('debug', 'readcfgfromfile') is True:
    """
    Get the configration value from configration file
    """
    ## get from config file
    #DEFAULT_TREE = get_config_value('Installation', 'url')
    #DEFAULT_KICKSTART = get_config_value('Installation', 'ks')
    ## for auto version detecting
    #OS_VERSION = get_config_value('checkpoint', "osversion")
    #GUEST_NAME = get_config_value('Installation', 'guestname')
    ##DEFAULT_PATH = get_config_value('Installation', 'path')
    #DEFAULT_POOLNAME = get_config_value('storage_pool', 'name')

else:
    ## Temporary change config when debugging a special case and don't worry about recovering configration files
    #DEFAULT_TREE = "http://download.eng.pek2.redhat.com/pub/rhel/released/RHEL-7/7.3/Server/x86_64/os/"
    #DEFAULT_KICKSTART = "ks=http://fileshare.englab.nay.redhat.com/pub/section3/run/http-ks/ks-rhel7u3-x86_64.cfg"
    ## for auto version detecting
    #OS_VERSION = "Red Hat Enterprise Linux 7.3"  
    #GUEST_NAME = "rhel7.3_autotest"


class templateModuleTest(unittest.TestCase):
    """
    Storage Management test cases
    """
    def setUp(self):
        self.app = vmmApp(DEFAULT_URI)
        self.app.select_connection(DEFAULT_CONNECTION)
    def tearDown(self):
        try:
            self.app.kill()
        except:
            raise

    ###### Test Cases ######
    #@unittest.skipIf(not check_bug_fixed(xxxx), "Bug xxxx has not yet been fixed")
    def test_template_case(self):
        """ 
        # RHEL7-13710
        # [Storage] Add storage pool- dir
        """
        testcase_begin_log(get_current_function_name())
        DEFAULT_CASE_RESULT = "FAILED"

        try:
            # case body
            # ......
            DEFAULT_CASE_RESULT = "PASSED"
        except Exception as e:
            screenshot(get_current_function_name())
            exception_log(e)
            raise
        finally:
            # env clear
            # ......
            testcase_finish_log(get_current_function_name(), DEFAULT_CASE_RESULT)
            

if __name__ == '__main__':
    unittest.main()
