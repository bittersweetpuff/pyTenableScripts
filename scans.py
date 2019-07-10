import json
import requests
import ssl
import urllib.request
import requests.packages
import requests.packages.urllib3
import time
import logging
import numbers


class Scans:
    """namespace as scans of Nessus"""




    def __init__(self, nessus_connection):
        self.nessus = nessus_connection


    def execute(self, *args, **kwargs):
        """proxy method"""
        return self.nessus.execute(*args, **kwargs)


    def copy(self, scan_id, name=None):
        """
        Clones the scan instance.
        """
        payload = {
            'name': name
        }

        cpy = self.execute("POST", f"/scans/{scan_id}/copy", data=payload)
        return cpy


    def details(self, scan_id, fields=None):
        """
        Returns the details for a specific scan.
        """

        scan = self.execute("GET", f"/scans/{scan_id}")

        det = dict()

        for f in fields:
            det[f] = []
            det[f].append(scan.get(f, "n/a"))
        return det


    def launch(self, scan_id, diagnostic_target=None, diagnostic_password=None):

        payload = dict()
        if diagnostic_target and diagnostic_passwsord:
            payload['diagnosticTarget'] = self._check(
                'diagnostic_target', diagnostic_target, str)
            payload['diagnosticPassword'] = self._check(
                'diagnostic_password', diagnostic_password, str)

        return self.execute("POST", f"/scans/{scan_id}/launch", data=payload)


    def delete(self, scan_id):

        return self.execute("DELETE", f"/scans/{scan_id}")


    def list(self, fields=None):

        return self.execute("GET", "/scans")
