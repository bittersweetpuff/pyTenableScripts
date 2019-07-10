

class File:
    def __init__(self, nessus_connection):
        self.nessus = nessus_connection


    def execute(self, *args, **kwargs):
        """proxy method"""
        return self.nessus.execute(*args, **kwargs)


    def upload(self, fobj):
        '''
        Uploads a file into SecurityCenter and returns the file identifier
        to be used for subsequent calls.

        :sc-api:`file: upload <File.html#FileRESTReference-/file/upload>`

        Args:
            fobj (FileObj): The file object to upload into SecurityCenter.

        Returns:
            :obj:`str`:
                The filename identifier to use for subsequent calls in
                Tenable.sc.
        '''
        return self.execute("POST", f"/file/upload", data=fobj)
