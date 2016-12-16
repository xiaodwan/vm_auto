import sys
import unittest

from getpass import getuser
from dogtail.utils import screenshot
from dogtail.logging import debugLogger as vmmlogger

from utils.uiutils import exception_log

if __name__ == '__main__':
    sys.path.insert(0, '..')

from utils.uiutils import *
from utils.dogtailutils import *

DEFAULT_POOLNAME="autotestdir"

DEFAULT_URI = "qemu:///system"

if DEFAULT_URI == "qemu:///system":
    DEFAULT_PATH = "/var/lib/libvirt/images/"
elif DEFAULT_URI == "qemu:///session":
    if getuser() != 'root':
        DEFAULT_PATH = "/home/" + getuser() +"/.local/share/libvirt/images/"
    else:
        DEFAULT_PATH = "/var/lib/libvirt/images/"

class storageManagerTest(unittest.TestCase):
    """
    Storage Management test cases
    """
    def setUp(self):
        self.app = vmmApp(DEFAULT_URI)
        self.app.select_connection("QEMU/KVM")
    def tearDown(self):
        try:
            self.app.kill()
        except:
            raise

    ###### Test Cases ######
    def test_add_poor_type_dir(self):
        """ 
        # RHEL7-13710
        # [Storage] Add storage pool- dir
        """
        try:
            # Create a connect details window instance
            self.connc_details = vmmConnectionDetails(self.app)
            # Open the open connection details window
            self.connc_details.open_connection_details()
            self.connc_details.add_pool_type_dir(self.connc_details.rootwindow, 
                                                 DEFAULT_POOLNAME) 
        
            # check created dir pool
            find_pattern(self.connc_details.rootwindow, DEFAULT_POOLNAME, "table cell")

            # check the status of the pool
            (name,
            ignore,
            location,
            autostart,
            ignore) = self.connc_details.get_pool_status_all(self.connc_details.rootwindow, 
                                                             DEFAULT_POOLNAME)
            self.assertEqual(name, DEFAULT_POOLNAME)
            self.assertEqual(autostart, "On Boot")
            self.assertEqual(location, DEFAULT_PATH + DEFAULT_POOLNAME)
        except Exception as e:
            screenshot(get_current_function_name())
            exception_log(e)
            raise
        finally:
            # clean created dir pool
            self.connc_details.del_pool(DEFAULT_POOLNAME)
            

if __name__ == '__main__':
    unittest.main()
