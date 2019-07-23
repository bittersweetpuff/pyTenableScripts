class NessusDataKeeper:
    def __init__(self, nessus_connection):
        """
        Contructor
        """
        self.scans = []
        self.scansTemplates = []
        self.nessus = nessus_connection
        self.folderID = None

    def Prepare(self):
        """
        Collects and prepares data from nessus.
        """
        early_results = self.nessus.scans.list()
        results = early_results["folders"]
        for folder in results:
            if folder["type"] == "main":
                self.folderID = folder["id"]

        early_results = self.nessus.scans.list()
        results = early_results["scans"]
        for scan in results:
            if scan["folder_id"] == self.folderID:
                self.scans.append(scan)

        self.GetTemplateList()

    def SetFolderID(self, folderType="main"):
        """
        Picks the folder to collect scans data from
        Args:
            folderType (str, optional): The type of the folder. "Main" is default
        """
        early_results = self.nessus.scans.list()
        results = early_results["folders"]
        for folder in results:
            if folder["type"] == folderType:
                return folder["id"]

    def GetScansList(self):
        """
        Gathers scan data
        """
        self.scans = []
        early_results = self.nessus.scans.list()
        results = early_results["scans"]
        for scan in results:
            if scan["folder_id"] == self.folderID:
                self.scans.append(scan)

    def FilterScanResults(self, fields):
        """
        Filters scan data
        Args:
            fields (list): Specified fields.
        """
        self.GetScansList()
        result = []
        for scan in self.scans:
            dictionary = dict()
            for field in fields:
                dictionary[field] = scan[field]
            result.append(dictionary.copy())
        return result

    def GetTemplateList(self):
        """
        Returns list of templates from editor module
        """
        self.scansTemplates = []
        results = self.nessus.editor.list("scan")
        for template in results["templates"]:
            self.scansTemplates.append(template)

    def FilterTemplateResultsTitles(self):
        """
        Gets templte names
        """
        result = []
        for template in self.scansTemplates:
            result.append(template["title"])
        return result

    def BuildUUIDDict(self):
        """
        Creates dictionary of UUID and templates names
        """
        result = dict()
        for template in self.scansTemplates:
            result[template["title"]] = template["uuid"]
        return result

    def UpdateFilteredResults(self, fields):
        """
        Collects up to date data from nessus and filters it
        Args:
            fields (list): Specified fields.
        """
        self.GetScansList()
        return self.FilterResults(fields)
