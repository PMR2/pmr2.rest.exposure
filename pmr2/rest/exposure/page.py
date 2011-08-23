import json
import zope.component
from zope.publisher.browser import BrowserView

from Products.CMFCore.utils import getToolByName
from pmr2.rest.workspace.base import JsonGetView
from pmr2.app.exposure.interfaces import IExposureSourceAdapter
from pmr2.app.exposure.browser.browser import ExposurePort
from pmr2.app.exposure.browser.browser import ExposurePortCommitIdForm
from pmr2.app.exposure.browser.util import fieldvalues


class ExposureContentsView(JsonGetView):
    """\
    Exposure contents.
    """

    def render(self):
        # XXX figure out how to simplify this
        exposure = self.context.context
        catalog = getToolByName(exposure, 'portal_catalog')

        query = {
            'portal_type': 'ExposureFile',
            'path': [
                u'/'.join(exposure.getPhysicalPath()),
            ],
            'sort_on': 'sortable_title',
        }
        results = catalog(**query)

        keys = ['Title', 'URI']
        values = ([(i.Title, i.getURL(),) for i in results])
        result = {
            'keys': keys,
            'values': values,
        }
        return self.dumps(result)


class ExposureInfoView(JsonGetView):
    """
    """

    def render(self):
        exposure = self.context.context
        helper = zope.component.queryAdapter(exposure,
            IExposureSourceAdapter)
        if not helper:
            # XXX exception of some sort
            return False
        exposure, workspace, path = helper.source()
        keys = ('title', 'workspace', 'commit_id',)
        title = exposure.title
        workspace = workspace.absolute_url()
        node = exposure.commit_id

        values = (title, workspace, node,)
        result = dict(zip(keys, values))
        return self.dumps(result)


class ExposureExportView(JsonGetView):

    def render(self):
        exposure = self.context.context
        port = ExposurePort(exposure, self.request)
        result = list(port.export())
        return self.dumps(result)


# Exposure File

class ExposureFileInfoView(JsonGetView):
    """
    """

    target_view = 'rawfile'

    def render(self):
        exposurefile = self.context.context
        helper = zope.component.queryAdapter(exposurefile,
            IExposureSourceAdapter)
        if not helper:
            # XXX exception of some sort
            return False
        exposure, workspace, path = helper.source()
        keys = ('source_uri', 'file_type', 'views',)

        source_uri = '%s/@@%s/%s/%s' % (workspace.absolute_url(),
            self.target_view, exposure.commit_id, path)
        file_type = exposurefile.file_type
        views = exposurefile.views

        values = (source_uri, file_type, views,)
        result = dict(zip(keys, values))
        return self.dumps(result)


class ExposureFileViewerView(JsonGetView):
    """
    """

    def render(self):
        view = self.request.get('view', None)
        if not view:
            return self.defaultRender()
        
        key = self.request.get('key', None)
        if not key:
            return self.renderViewKeys(view)

    def renderViewKeys(self, name):
        """\
        Render a list of keys for this view.
        """

        exposurefile = self.context.context
        note = zope.component.queryAdapter(exposurefile, name=name)
        if not note:
            # XXX maybe some sort of error instead?
            return
        fields = fieldvalues(note)
        return fields

    def defaultRender(self):
        exposurefile = self.context.context

        keys = ('views',)

        views = exposurefile.views

        values = (views,)
        result = dict(zip(keys, values))
        return self.dumps(result)
