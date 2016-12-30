#!/usr/bin/env python

import os
import sys
import warnings
import unittest

from dogtail.logging import debugLogger as vmmlogger

from testcases.storage import storageManagerTest
from testcases.installation import installationTest
from testcases.test import testTest 

# Dogtail is noisy with GTK and GI deprecation warnings
warnings.simplefilter("ignore")

# Ignores pylint error since dogtail doesn't specify this
import gi
gi.require_version('Atspi', '2.0')

import dogtail.config

# Turn off needlessly noisy debugging
DOGTAIL_DEBUG = False
dogtail.config.config.logDebugToStdOut = DOGTAIL_DEBUG
#dogtail.config.config.logDebugToFile = False
# if output test result to stdout
STD_OUTPUT = False

# Needed so labels are matched in english
os.environ['LANG'] = 'en_US.UTF-8'

if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromTestCase(storageManagerTest)
    suite = unittest.TestLoader().loadTestsFromTestCase(testTest)
    #suite = unittest.TestLoader().discover('./testcases', pattern='*.py')
    #suite2 = unittest.TestLoader().loadTestsFromTestCase(storageManagerTest)
    #suite = unittest.TestLoader().loadTestsFromTestCase(installationTest)
    #alltests = unittest.TestSuite([suite, suite2])
    #unittest.TextTestRunner(verbosity=2).run(alltests)
    if STD_OUTPUT:
        fp = sys.stderr
    else:
        fp = open('./vm_autotest_result.txt', 'ab+')

    from datetime import datetime
    fp.write('='*10 + " %s " % datetime.now() + '='*10 + '\n')
    test_result = unittest.TextTestRunner(stream=fp, verbosity=2).run(suite)

    if not STD_OUTPUT:
        fp.close()

