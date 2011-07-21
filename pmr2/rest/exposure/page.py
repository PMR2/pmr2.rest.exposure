import json
import zope.component
from zope.publisher.browser import BrowserView

from Products.CMFCore.utils import getToolByName
from pmr2.rest.workspace.base import JsonGetView
from pmr2.rest.workspace.base import JsonPostView
from pmr2.app.exposure.interfaces import IExposureSourceAdapter
from pmr2.app.exposure.browser.browser import ExposurePort
from pmr2.app.exposure.browser.browser import ExposurePortCommitIdForm


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


class ExposureRolloverPostView(JsonPostView):
    """\
    Exposure edits.
    """

    def render(self):
        # XXX mocking up the form fields until I can figure out a better
        # way to pass in the values and have them prepared internally.
        exposure = self.context.context
        self.request.form['form.widgets.commit_id'] = self.request['commit_id']
        self.request.form['form.buttons.apply'] = 1
        form = ExposurePortCommitIdForm(exposure, self.request)
        form.disableAuthenticator = True
        form.update()
        # XXX there may be errors
        # XXX need error handling, return error status code on failures
        location = form.nextURL()
        result = {
            'location': location,
        }
        return self.dumps(result)
