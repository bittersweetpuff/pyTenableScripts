import json
import requests
import ssl
import urllib.request
import requests.packages
import requests.packages.urllib3
import time
import logging
import numbers



class ScanInstances:
    """namespace as scan_instances of the SC"""

    def __init__(self, nessus_connection):
        self.nessus = nessus_connection

    def execute(self, *args, **kwargs):
        """proxy method"""
        return self.nessus.execute(*args, **kwargs)

    def export_scan(self, scan_id, fobj):
        """
        export nessus scan by id to file-like object
        :param scan_id:
        :param fobj:
        :return:
        """
        assert isinstance(scan_id, numbers.Integral)

        resp = self.execute("post", "/scans/%s/export" % scan_id, {"format": "nessus"})
        try:
            to_download = resp["file"]
        except Exception:
            print(resp)
            return ""
        out = "waiting"
        i = 200
        while i > 0 and out != "ready":
            rq = "/scans/%s/export/%s/status" % (scan_id, to_download)
            print(rq, to_download)
            out = self.execute("get", rq)["status"]
            time.sleep(1)
            i -= 1
        rq = "/scans/%s/export/%s/download" % (scan_id, to_download)
        out = self.execute("get", rq)
        # LOGGER.info(f'{out}')
        fobj.write(out)
        return out

    def details(self, scan_id, fields):
        """
        Retreives the details for the specified scan instance.
        """
        det = dict()
        scan = self.execute("GET", f"/scans/{scan_id}")
        for f in fields:
            det[f] = []
            det[f].append(scan.get(f, "n/a"))

        return det


    def pause(self, scan_id):
        '''
        Pauses a running scan instance.
        '''
        ret = dict()
        ret["response"] = []
        pause = self.execute("POST", f"/scans/{scan_id}/pause")
        return type(pause)


    def resume(self, scan_id):
        '''
        Resumes a paused scan instance.
        '''
        res = self.execute("POST", f"/scans/{scan_id}/resume")

        return res


    def stop(self, scan_id):
        '''
        Stops a running scan instance.
        '''
        stp = self.execute("POST", f"/scans/{scan_id}/stop")

        return stp


    def delete(self, id):
        """
        Removes the scan instance from Nessus.
        """
        str = ''
        self.execute("DELETE", f"/scans/{id}")

        return str


    def uploadTest(self, fobj):
        return self.execute("POST", "/file/upload", data = fobj)


    def list(self, fields):
        """list scans available to user"""
        rv = dict()
        rv["usable"] = []
        for scan in self.execute("GET", "/scans")["scans"]:
            sta = {f: scan.get(f, "n/a") for f in fields}
            sta["startTime"] = scan.get("creation_date", "n/a")
            sta["finishTime"] = scan.get("last_modification_date", "n/a")

            rv["usable"].append(sta)
        return rv
