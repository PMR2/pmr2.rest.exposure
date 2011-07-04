====================================
Web service access for PMR2 Exposure
====================================

This module provides a web service access for PMR2 exposure.
::

    >>> from pmr2.app.exposure.content import *
    >>> from pmr2.testing.base import TestRequest
    >>> from pmr2.rest.workspace import base
    >>> from pmr2.rest.exposure import view
    >>> base.BaseJsonView.indent = 4
    >>> request = TestRequest()
    >>> notetext = u'This is added.'
    >>> ef = ExposureFile('test')
    >>> ef.title = u'Test'
    >>> ef.views = [u'edited_note']
    >>> self.portal.exposure['1']['test'] = ef
    >>> self.portal.exposure['1']['test'].reindexObject()
    >>> note = zope.component.getAdapter(self.portal.exposure['1']['test'], 
    ...                                  name='edited_note')
    >>> note.note = notetext

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
        "values": [
            [
                "Test",
                "http://nohost/plone/exposure/1/test"
            ]
        ]
    }

Lastly extract the exposure profile in JSON format.
::

    >>> result = v.export()
    >>> print result
    [
        [
            "test",
            {
                "views": [
                    [
                        "edited_note",
                        {
                            "note": "This is added."
                        }
                    ]
                ],
                "file_type": null,
                "selected_view": null,
                "docview_gensource": null,
                "docview_generator": null,
                "Subject": []
            }
        ],
        [
            "",
            {
                "commit_id": "2",
                "title": "",
                "curation": null,
                "workspace": "/plone/workspace/test",
                "docview_gensource": null,
                "docview_generator": null,
                "Subject": []
            }
        ]
    ]


-------
Writing
-------

There is also a utility to rollover exposures using the edit form.
::

    >>> request = TestRequest(form={
    ...     'commit_id': '3',
    ... })
    >>> v = view.ExposureJsonEdit(self.portal.exposure['1'], request)
    >>> result = v.rollover()
    >>> print result
    {
        "location": "http://nohost/plone/exposure/...
    }
