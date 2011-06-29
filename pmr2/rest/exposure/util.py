from Products.CMFCore.utils import getToolByName

def WorkspaceExposureJsonField(context):
    # return list of exposures from this workspace

    catalog = getToolByName(context, 'portal_catalog')

    query = {
        'portal_type': 'Exposure',
        'pmr2_exposure_workspace': [
            u'/'.join(context.getPhysicalPath()),
        ],
        'sort_on': 'sortable_title',
    }
    results = catalog(**query)

    keys = ['title', 'uri', 'commit_id', 'state']
    values = ([(
            i.Title,
            i.getURL(),
            i.pmr2_exposure_commit_id,
            i.pmr2_review_state,
        ) for i in results])

    result = {
        'keys': keys,
        'values': values,
    }
    return result
