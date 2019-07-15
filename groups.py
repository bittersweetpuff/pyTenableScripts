from base import TypeCheck


class Group:
    def _constructor(self, **kw):
        '''
        Handles parsing the keywords and returns a group definition document
        '''
        if 'name' in kw:
            TypeCheck('name', kw['name'], str)
        return kw


    def __init__(self, nessus_connection):
        self.nessus = nessus_connection


    def execute(self, *args, **kwargs):
        """proxy method"""
        return self.nessus.execute(*args, **kwargs)


    def list(self, fields=None):
        '''
        Retrieves the list of scan zone definitions.

        Args:
            fields (list, optional):
                A list of attributes to return for each group.

        Returns:
            :obj:`list`:
                A list of group resources.

        Examples:
            >>> for group in sc.groups.list():
            ...     pprint(group)
        '''
        det = dict()
        grp = self.execute('GET', '/groups')

        if fields:
            for f in fields:
                det[f] = []
                det[f].append(grp.get(f, "n/a"))
                return det

        else:
            return grp


    def delete(self, group_id):

            return self.execute('DELETE', f'/groups/{group_id}')


    def create(self, **kw):

        payload = self._constructor(**kw)

        return self.execute('POST', '/groups', payload = payload)


    def edit(self, group_id, **kw):

        payload = self._constructor(**kw)

        return self.execute('PUT', f'/groups/{group_id}', payload = payload)
