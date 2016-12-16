#!/usr/bin/env python

import os
import sys
import warnings
import unittest

from cases.storage import storageManagerTest
from cases.installation import installationTest

# Dogtail is noisy with GTK and GI deprecation warnings
warnings.simplefilter("ignore")

# Ignores pylint error since dogtail doesn't specify this
import gi
gi.require_version('Atspi', '2.0')

import dogtail.config


# Turn off needlessly noisy debugging
DOGTAIL_DEBUG = True
dogtail.config.config.logDebugToStdOut = DOGTAIL_DEBUG
#dogtail.config.config.logDebugToFile = False

# Needed so labels are matched in english
os.environ['LANG'] = 'en_US.UTF-8'

# TBD 
# Wanna control all global args here, for example, when run from this script,
# DEFAULT_URI in this file will be used.
# If run cases/* directly, the DEFAULT_URI values in cases scripts will be used.

# DEFAULT_URI = "qemu:///system"
# DEFAULT_POOLNAME = "autotestpoolname"
# ...

if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromTestCase(storageManagerTest)
    suite = unittest.TestLoader().loadTestsFromTestCase(installationTest)
    #alltests = unittest.TestSuite([suite, suite2])
    unittest.TextTestRunner(verbosity=2).run(suite)
