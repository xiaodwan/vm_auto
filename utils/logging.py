#!/usr/bin/env python

import traceback

from dogtail.logging import debugLogger as vmmlogger

def testcase_begin_log(case_name):
    vmmlogger.log("%s" % '='*30)
    vmmlogger.log("Begin run case: %s" % case_name)

def testcase_finish_log(case_name, result):
    vmmlogger.log("Finish run case: %s: [%s]" % (case_name, result))
    vmmlogger.log("%s" % '='*30)

def exception_log(e):
    bt = traceback.format_exc(e)
    vmmlogger.log(bt)
