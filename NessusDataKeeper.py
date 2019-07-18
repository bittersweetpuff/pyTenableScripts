class NessusDataKeeper:

    def __init__(self, nessus_connection):
        self.scans = []
        self.nessus = nessus_connection
        self.folderID = None


    def Prepare(self):
        early_results = self.nessus.scans.list()
        results = early_results['folders']
        for folder in results:
            if folder['type'] == 'main':
                self.folderID = folder['id']

        early_results = self.nessus.scans.list()
        results = early_results['scans']
        for scan in results:
            if scan['folder_id'] == self.folderID:
                self.scans.append(scan)


    def SetFolderID(self, folderType='main'):
        early_results = self.nessus.scans.list()
        results = early_results['folders']
        for folder in results:
            if folder['type'] == folderType:
                return folder['id']


    def GetScansList(self):
        self.scans = []
        early_results = self.nessus.scans.list()
        results = early_results['scans']
        for scan in results:
            if scan['folder_id'] == self.folderID:
                self.scans.append(scan)


    def FilterResults(self, fields):

        result = []
        for scan in self.scans:
            dictionary = dict()
            for field in fields:
                dictionary[field] = scan[field]
            result.append(dictionary.copy())

        return result

    def UpdateFilteredResults(self, fields):
        self.GetScansList()
        return self.FilterResults(fields)
