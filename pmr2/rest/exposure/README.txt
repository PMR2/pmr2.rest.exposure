====================================
Web service access for PMR2 Exposure
====================================

This module provides a web service access for PMR2 exposure.
::

    >>> from pmr2.app.exposure.content import *
    >>> from pmr2.testing.base import TestRequest
    >>> from pmr2.rest.workspace import base
    >>> from pmr2.rest.exposure import view
    >>> from pmr2.rest.exposure import page
    >>> base.JsonGetView.indent = 4
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

    >>> request = TestRequest()
    >>> v = view.ExposureRestView(self.portal.exposure['1'], request)
    >>> p = page.ExposureInfoView(v, request)
    >>> result = p()
    >>> print result
    {
        "commit_id": "2",
        "workspace": "http://nohost/plone/workspace/test",
        "title": ""
    }

Can also retrieve contents from it.
::

    >>> p = page.ExposureContentsView(v, request)
    >>> result = p()
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

    >>> p = page.ExposureExportView(v, request)
    >>> result = p()
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


Instantiate the ExposureFile JSON view, and acquire some info.
::

    >>> request = TestRequest()
    >>> v = view.ExposureFileRestView(self.portal.exposure['1']['test'],
    ...                               request)
    >>> p = page.ExposureFileInfoView(v, request)
    >>> result = p()
    >>> print result
    {
        "file_type": null,
        "source_uri": "http://nohost/plone/workspace/test/@@rawfile/2/test",
        "views": [
            "edited_note"
        ]
    }

The viewer would extract the info
::

    >>> request = TestRequest(form={
    ...     'view': 'edited_note',
    ... })
    >>> v = view.ExposureFileRestView(self.portal.exposure['1']['test'],
    ...                               request)
    >>> p = page.ExposureFileViewerView(v, request)
    >>> result = p()
    >>> print result
    {'note': u'This is added.'}
