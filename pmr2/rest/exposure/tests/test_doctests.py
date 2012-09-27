import unittest
import doctest

from Testing import ZopeTestCase as ztc

from pmr2.app.exposure.tests import base

def test_suite():
    return unittest.TestSuite([

        ztc.ZopeDocFileSuite(
            'README.txt', package='pmr2.rest.exposure',
            test_class=base.CompleteDocTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
        ),

    ])
