from base import TypeCheck


class User:
    def _constructor(self, **kw):
        '''
        Handles parsing the keywords and returns a user definition document
        '''
        # all of the following keys are string values and do not require any
        # case conversion.  We will simply iterate through them and verify that
        # they are in-fact strings.
        keys = [
            'username', 'password', 'permissions', 'name',
            'email', 'type'
        ]
        for k in keys:
            if k in kw:
                TypeCheck(k, kw[k], str)

        return kw


    def __init__(self, nessus_connection):
        self.nessus = nessus_connection


    def execute(self, *args, **kwargs):
        """proxy method"""
        return self.nessus.execute(*args, **kwargs)


    def create(self, username, password, permissions, type, **kw):
        '''
        Creates a user.

        :sc-api:`user: create <User.html#user_POST>`

        Args:
            username (str):
                The username for the account
            password (str):
                The password for the user to create
            permissions (str):
                The role of the user.
            type (str):
                The type of user.
            name (str, optional):
                The real name of the user.
            email (str, optional):
                The email address of the user

        Returns:
            :obj:`dict`:
                The newly created user.

        Examples:
            >>> user = sc.users.create('username', 'password', 16, 'local')
        '''
        kw['username'] = username
        kw['password'] = password
        kw['permissions'] = permissions
        kw['type'] = type
        payload = self._constructor(**kw)

        return self.execute('POST', '/users', payload = payload)


    def edit(self, user_id, permissions, **kw):
        '''
        Creates a user.

        :sc-api:`user: create <User.html#user_POST>`

        Args:
            user_id (int):
                The unique id of the user.
            permissions (str):
                The role of the user.
            name (str, optional):
                The real name of the user.
            email (str, optional):
                The email address of the user

        Returns:
            :obj:`dict`:
                The newly updated user.

        Examples:
            >>> user = sc.users.edit(1, 16, name='newname')
        '''
        kw['permissions'] = permissions
        payload = self._constructor(**kw)

        return self.execute('PUT', f'/users/{user_id}', payload = payload)



    def delete(self, user_id):
        '''
        Removes a user.

        Args:
            user_id (int): The numeric identifier for the user to remove.

        Returns:
            :obj:`str`:
                An empty response.

        Examples:
            >>> sc.users.delete(1)
        '''

        return self.execute('DELETE', f'/users/{user_id}')


    def details(self, user_id, fields=None):
        '''
        Returns the details for a specific user.

        Args:
            user_id (int): The identifier for the user.
            fields (list, optional): A list of attributes to return.

        Returns:
            :obj:`dict`:
                The user resource record.

        Examples:
            >>> user = sc.users.details(1)
            >>> pprint(user)
        '''
        det = dict()
        usr = self.execute('GET', f'/users/{user_id}')

        if fields:
            for f in fields:
                det[f] = []
                det[f].append(usr.get(f, "n/a"))
                return det

        else:
            return usr


    def list(self, fields=None):
        '''
        Retrieves the list of users.

        Args:
            fields (list, optional):
                A list of attributes to return for each user.

        Returns:
            :obj:`list`:
                A list of user resources.

        Examples:
            >>> for user in sc.users.list():
            ...     pprint(user)
        '''
        det = dict()
        usr = self.execute('GET', '/users')

        if fields:
            for f in fields:
                det[f] = []
                det[f].append(usr.get(f, "n/a"))
                return det

        else:
            return usr
