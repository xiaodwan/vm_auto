import sys
import unittest

from getpass import getuser
from dogtail.utils import screenshot

if __name__ == '__main__':
    sys.path.insert(0, '..')

from utils.uiutils import *
from utils.dogtailutils import *

DEFAULT_POOLNAME="autotestdir"

DEFAULT_URI = "qemu:///session"

if DEFAULT_URI == "qemu:///system":
    DEFAULT_PATH = "/var/lib/libvirt/images/"
elif DEFAULT_URI == "qemu:///session":
    DEFAULT_PATH = "/home/" + getuser() +"/.local/share/libvirt/images/"

class testTest(unittest.TestCase):
    """
    UI tests for virt-manager
    """
    def setUp(self):
        self.app = vmmApp(DEFAULT_URI)
    def tearDown(self):
        try:
            self.app.kill()
        except:
            raise

    ###### Test Cases ######
    # RHEL7-13710
    # [Storage] Add storage pool- dir
    def test_set_feedback(self):
        """ 
        # RHEL7-13710
        # [Storage] Add storage pool- dir
        """
        win_preferences = vmmPreferences(self.app)
        #win_preferences.setconformation("Deleting storage", True)
        win_preferences.setconformation()
        win_preferences.close_preferences()

if __name__ == "__main__":
    unittest.main()
