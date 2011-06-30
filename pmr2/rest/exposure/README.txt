====================================
Web service access for PMR2 Exposure
====================================

This module provides a web service access for PMR2 exposure.
::

    >>> from pmr2.app.workspace.content import *
    >>> from pmr2.testing.base import TestRequest
    >>> from pmr2.rest.workspace import base
    >>> base.BaseJsonView.indent = 4
    >>> from pmr2.rest.exposure import view
    >>> request = TestRequest()

Instantiate the Exposure JSON view, and acquire some info.
::

    >>> v = view.ExposureJsonView(self.portal.exposure['1'], request)
    >>> result = v.info()
    >>> print result
    {
        "commit_id": "2",
        "workspace": "http://nohost/plone/workspace/test",
        "title": ""
    }

Can also retrieve contents from it.
::

    >>> result = v.contents()
    >>> print result
    {
        "keys": [
            "Title",
            "URI"
        ],
        "values": []
    }
