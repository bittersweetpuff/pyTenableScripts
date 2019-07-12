from base import TypeCheck


class Group:
    def _constructor(self, **kw):
        '''
        Handles parsing the keywords and returns a group definition document
        '''
        if 'name' in kw:
            TypeCheck('name', kw['name'], str)

        if 'description' in kw:
            TypeCheck('description', kw['description'], str)

        mapping = {
            'viewable': 'definingAssets',
            'repos': 'repositories',
            'lce_ids': 'lces',
            'asset_lists': 'assets',
            'scan_policies': 'policies',
            'query_ids': 'queries',
            'scan_creds': 'credentials',
            'dashboards': 'dashboardTabs',
            'report_cards': 'arcs',
            'audit_files': 'auditFiles'
        }
        for k, v in mapping.items():
            if k in kw:
                # For each item in the mapping, expand the kwarg if it exists
                # into a list of dictionaries with an id attribute.  Associate
                # the expanded list to the value of the hash table and delete
                # the original kwarg.
                kw[v] = [{'id': TypeCheck('{}:item'.format(k), i, int)}
                    for i in TypeCheck(k, kw[k], list)]
                del(kw[k])
        return kw


    def __init__(self, nessus_connection):
        self.nessus = nessus_connection


    def execute(self, *args, **kwargs):
        """proxy method"""
        return self.nessus.execute(*args, **kwargs)


    def list(self, fields=None):
        det = dict()
        grp = self.execute('GET', '/groups')

        if fields:
            for f in fields:
                det[f] = []
                det[f].append(grp.get(f, "n/a"))
                return det

        else:
            return grp
