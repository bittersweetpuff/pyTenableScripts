from base import TypeCheck


class Plugin:
    def _constructor(self, **kw):
        '''
        Constructs the plugin query.
        '''

        if 'fields' in kw:
            kw['fields'] = ','.join([TypeCheck('field', f, str)
                for f in TypeCheck('fields', kw['fields'], list)])

        if 'filter' in kw:
            # break down the filter tuple into the various query parameters
            # that the plugin api expects.
            TypeCheck('filter', kw['filter'], tuple)
            if len(kw['filter']) != 3:
                raise UnexpectedValueError(
                    'the filter tuple must be name, operator, value.')
            kw['filterField'] = TypeCheck('filter:field', kw['filter'][0], str)
            kw['op'] = TypeCheck('filter:operator', kw['filter'][1], str,
                choices=['eq', 'gt', 'gte', 'like', 'lt', 'lte'])
            kw['value'] = TypeCheck('filter:value', kw['filter'][2], str)
            del(kw['filter'])

        if 'sort_field' in kw:
            # convert the snake_cased variant of the parameter to the camelCased
            # variant that the API expects to see.
            kw['sortField'] = TypeCheck(
                'sort_field', kw['sort_field'], str)
            del(kw['sort_field'])

        if 'sort_direction' in kw:
            # convert the snake_cased variant of the parameter to the camelCased
            # variant that the API expects to see.
            kw['sortDirection'] = TypeCheck(
                'sort_direction', kw['sort_direction'], str,
                choices=['ASC', 'DESC'], case='upper')
            del(kw['sort_direction'])

        if 'since' in kw:
            # The since parameter should be an integer.
            TypeCheck('since', kw['since'], int)

        if 'type' in kw:
            # Validate that the plugin type is whats expected.
            TypeCheck('type', kw['type'], str, choices=[
                    'active', 'all', 'compliance', 'custom',
                    'lce', 'notPassive', 'passive'
                ], default='all')


        # While the iterator will handle the offset & limits, a raw json result
        # may be requested instead.
        if 'offset' in kw:
            kw['startOffset'] = TypeCheck('offset', kw['offset'], int)
            del(kw['offset'])

        if 'limit' in kw:
            kw['endOffset'] = TypeCheck(
                'limit', kw['limit'], int) + kw.get('startOffset', 0)
            del(kw['limit'])

        # Pages and json_result paramaters should be removed from the document
        # if they exist.
        if 'pages' in kw:
            del(kw['pages'])

        if 'json_result' in kw:
            del(kw['json_result'])

        # Return the modified keyword dict to the caller.
        return kw


    def __init__(self, nessus_connection):
        self.nessus = nessus_connection


    def execute(self, *args, **kwargs):
        """proxy method"""
        return self.nessus.execute(*args, **kwargs)


    def details(self, id, fields=None):
        det = dict()
        plg = self.execute('GET', f'/plugins/plugin/{id}')

        if fields:
            for f in fields:
                det[f] = []
                det[f].append(plg.get(f, "n/a"))
                return det

        else:
            return plg
