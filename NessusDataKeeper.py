class NessusDataKeeper:

    def __init__(self, nessus_connection):
        self.scans = []
        self.scansTemplates = []
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

        self.GetTemplateList()


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


    def FilterScanResults(self, fields):
        self.GetScansList()
        result = []
        for scan in self.scans:
            dictionary = dict()
            for field in fields:
                dictionary[field] = scan[field]
            result.append(dictionary.copy())
        return result


    def GetTemplateList(self):
        self.scansTemplates = []
        results = self.nessus.editor.list('scan')
        for template in results['templates']:
            self.scansTemplates.append(template)


    def FilterTemplateResultsTitles(self):
        result = []
        for template in self.scansTemplates:
            result.append(template['title'])
        return result


    def BuildUUIDDict(self):
        result = dict()
        for template in self.scansTemplates:
            result[template['title']] = template['uuid']
        return result


    def UpdateFilteredResults(self, fields):
        self.GetScansList()
        return self.FilterResults(fields)
