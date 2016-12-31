import sys
import unittest

if __name__ == '__main__':
    sys.path.insert(0, '..')

from getpass import getuser
from dogtail.utils import screenshot

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
    # get from config file
    DEFAULT_TREE = get_config_value('Installation', 'url')
    DEFAULT_KICKSTART = get_config_value('Installation', 'ks')
    # for auto version detecting
    OS_VERSION = get_config_value('checkpoint', "osversion")
    GUEST_NAME = get_config_value('Installation', 'guestname')
else:
    DEFAULT_TREE = "http://download.eng.pek2.redhat.com/pub/rhel/released/RHEL-7/7.3/Server/x86_64/os/"
    DEFAULT_KICKSTART = "ks=http://fileshare.englab.nay.redhat.com/pub/section3/run/http-ks/ks-rhel7u3-x86_64.cfg"
    # for auto version detecting
    OS_VERSION = "Red Hat Enterprise Linux 7.3"  
    GUEST_NAME = "rhel7.3_autotest"

"""
Installation Test
"""
class installationTest(unittest.TestCase):
    """
    Installation Test cases
    """
    def setUp(self):
        self.app = vmmApp(DEFAULT_URI)
        self.app.select_connection(DEFAULT_CONNECTION)
    def tearDown(self):
        try:
            self.app.kill()
        except:
            raise

    def test_vm_install_url(self):
        """ 
        # RHEL7-13827
        # [Install domain] Install vm from HTTP - qcow2	
        """
        testcase_begin_log(get_current_function_name())
        DEFAULT_CASE_RESULT = "FAILED"
        
        try:
            newvm_wizard = vmmAddNewVM(app=self.app)
            newvm_wizard.open_create_wizard(self.app.root)

            find_fuzzy(newvm_wizard.rootwindow, "Network Install", "radio").click()
            find_fuzzy(newvm_wizard.rootwindow, "Forward", "button").click()

            find_pattern(newvm_wizard.rootwindow, None, "text", "URL").typeText(DEFAULT_TREE)
            # type kickstart into kernel options for auto installation
            # toggle button click doesn't work, so user keyCombo instead
            # uiutils.find_pattern(newvm_wizard, "URL Options", "toggle button").click()
            newvm_wizard.rootwindow.keyCombo('<Alt>o')
            find_pattern(newvm_wizard.rootwindow, None, 
                         "text", "Kernel options").typeText(DEFAULT_KICKSTART)
                

            # auto detect will begin after clicking Forward button
            find_fuzzy(newvm_wizard.rootwindow, "Forward", "button").click()

            version = find_pattern(newvm_wizard.rootwindow, "install-os-version-label")
            time.sleep(1)
            check_in_loop(lambda: "Detecting" not in version.text 
                          and "-" not in version.text)

            # check auto detecting version
            self.assertEquals(version.text, OS_VERSION)

            find_fuzzy(newvm_wizard.rootwindow, "Forward", "button").click()
            find_fuzzy(newvm_wizard.rootwindow, "Forward", "button").click()
            find_pattern(newvm_wizard.rootwindow, None, "text", "Name").typeText(GUEST_NAME)
            find_fuzzy(newvm_wizard.rootwindow, "Finish", "button").click()
            #time.sleep(.5)

            progress = find_fuzzy(self.app.root,
                                    "Creating Virtual Machine", "frame")
            # waiting 5 mins, if timeout, maybe a network problem
            check_in_loop(lambda: not progress.showing, 300)
            time.sleep(.5)

            find_fuzzy(self.app.root, GUEST_NAME +" on", "frame")
            self.assertFalse(newvm_wizard.rootwindow.showing)
            
            if self.app.pid is not None:
                # waiting vm installation complete
                check_vm_install_complete(self.app.pid, GUEST_NAME)
            else:
                self.assertTrue(False, "Error: pid is None")

            # check ping to guest, this only works for qemu:///system
            res = ping_vm(GUEST_NAME)
            self.assertTrue(res)

            self.app.quit()

            DEFAULT_CASE_RESULT = "PASSED"
        except Exception as e:
            screenshot(get_current_function_name())
            exception_log(e)
            raise
        finally:
            testcase_finish_log(get_current_function_name(), DEFAULT_CASE_RESULT)

            
if __name__ == '__main__':
    unittest.main()
