import json
import requests
import ssl
import urllib.request
import requests.packages
import requests.packages.urllib3
import time
import logging
import numbers
import uuid
from base import TypeCheck


class Scans:
    """namespace as scans of Nessus"""

    def _constructor(self, **kw):
        """
            Handles parsing the keywords and returns a scan settings document
            """
        if "name" in kw:
            TypeCheck("name", kw["name"], str)

        if "description" in kw:
            TypeCheck("description", kw["description"], str)

        if "policy_id" in kw:
            TypeCheck("policy_id", kw["policy_id"], int)

        if "folder_id" in kw:
            TypeCheck("folder_id", kw["folder_id"], int)

        if "scanner_id" in kw:
            TypeCheck("scanner_id", kw["scanner_id"], int)

        if "enabled" in kw:
            TypeCheck("enabled", kw["enabled"], bool)

        if "launch" in kw:
            TypeCheck("launch", kw["launch"], str)

        if "starttime" in kw:
            TypeCheck("starttime", kw["starttime"], str)

        if "rrules" in kw:
            TypeCheck("rrules", kw["rrules"], str)

        if "timezone" in kw:
            TypeCheck("timezone", kw["timezone"], str)

        if "text_targets" in kw:
            TypeCheck("text_targets", kw["text_targets"], str)

        if "agent_group_id" in kw:
            TypeCheck("agent_group_id", kw["agent_group_id"], list)

        if "file_targets" in kw:
            TypeCheck("file_targets", kw["file_targets"], str)

        if "emails" in kw:
            TypeCheck("emails", kw["emails"], str)

        if "acls" in kw:
            TypeCheck("acls", kw["acls"], list)

        return kw

    def __init__(self, nessus_connection):
        self.nessus = nessus_connection

    def execute(self, *args, **kwargs):
        """proxy method"""
        return self.nessus.execute(*args, **kwargs)

    def create(self, name, targets, **kw):
        """
        Creates a scan definition.

        Args:
            uuid (str, optional):
                Templates uuid. At least one of the arguments (uuid, title, name
                ) cant be empty
            template_title (str, optional):
                Templates title. At least one of the arguments (uuid, title, name
                ) cant be empty
            template_name (str, optional):
                Templates name. At least one of the arguments (uuid, title, name
                ) cant be empty
            name (str):
                The name of the scan.
            description (str, optional):
                The description of the scan.
            policy_id (int, optional):
                The unique id of the policy to use.
            folder_id (int, optional):
                The unique id of the destination folder for the scan.
            scanner_id (int, optional):
                The unique id of the scanner to use.
            enabled (bool):
                If true, the schedule for the scan is enabled.
            launch (str, optional):
                When to launch the scan. (i.e. ON_DEMAND, DAILY, WEEKLY, MONTHLY, YEARLY)
            starttime (str, optional):
                The starting time and date for the scan (i.e. YYYYMMDDTHHMMSS).
            rrules (str, optional):
                Expects a semi-colon delimited string comprised of three values.
                The frequency (FREQ=ONETIME or DAILY or WEEKLY or MONTHLY or YEARLY),
                the interval (INTERVAL=1 or 2 or 3 ... x), and the days of the
                week (BYDAY=SU,MO,TU,WE,TH,FR,SA). To create a scan that runs
                every three weeks on Monday Wednesday and Friday the string
                would be 'FREQ=WEEKLY;INTERVAL=3;BYDAY=MO,WE,FR'
            timezone (str, optional):
                The timezone for the scan schedule.
            targets (str):
                Targets to scan.
            agent_group_id (list, optional):
                The list of agent group IDs to scan; only valid for Agent scans.
            file_targets (str, optional):
                The name of a file containing the list of targets to scan.
            emails (str, optional):
                A comma separated list of accounts who will recieve the email summary report.
            acls (list, optional):
                An array containing permissions to apply to the scan.

        Returns:
            :obj:`dict`:
                The scan resource for the created scan.

        Examples:
            Creating a scan for a single host:

            >>> sc.scans.create('Example scan', 1, policy_id=1001,
            ...     targets=['127.0.0.1'])
        """

        uuid = None
        if "uuid" in kw:
            uuid = kw["uuid"]
        elif "template_name" in kw:
            uuid = self.nessus.editor.get_uuid_by_name("scan", kw["template_name"])
        elif "template_title" in kw:
            uuid = self.nessus.editor.get_uuid_by_title("scan", kw["template_title"])
        else:
            raise Exception("Error: Bad Argument")

        kw["name"] = name
        kw["text_targets"] = targets
        kw["enabled"] = True

        payload = dict()
        payload["uuid"] = uuid
        payload["settings"] = self._constructor(**kw)

        return self.execute("POST", "/scans", data=payload)


    def edit(self, scan_id, **kw):
        """
        Creates a scan definition.

        Args:
            uuid (str, optional):
                Templates uuid.
            template_title (str, optional):
                Templates title.
            template_name (str, optional):
                Templates name.
            name (str, optional):
                The name of the scan.
            description (str, optional):
                The description of the scan.
            policy_id (int, optional):
                The unique id of the policy to use.
            folder_id (int, optional):
                The unique id of the destination folder for the scan.
            scanner_id (int, optional):
                The unique id of the scanner to use.
            enabled (bool):
                If true, the schedule for the scan is enabled.
            launch (str, optional):
                When to launch the scan. (i.e. ON_DEMAND, DAILY, WEEKLY, MONTHLY, YEARLY)
            starttime (str, optional):
                The starting time and date for the scan (i.e. YYYYMMDDTHHMMSS).
            rrules (str, optional):
                Expects a semi-colon delimited string comprised of three values.
                The frequency (FREQ=ONETIME or DAILY or WEEKLY or MONTHLY or YEARLY),
                the interval (INTERVAL=1 or 2 or 3 ... x), and the days of the
                week (BYDAY=SU,MO,TU,WE,TH,FR,SA). To create a scan that runs
                every three weeks on Monday Wednesday and Friday the string
                would be 'FREQ=WEEKLY;INTERVAL=3;BYDAY=MO,WE,FR'
            timezone (str, optional):
                The timezone for the scan schedule.
            targets (str):
                Targets to scan.
            agent_group_id (list, optional):
                The list of agent group IDs to scan; only valid for Agent scans.
            file_targets (str, optional):
                The name of a file containing the list of targets to scan.
            emails (str, optional):
                A comma separated list of accounts who will recieve the email summary report.
            acls (list, optional):
                An array containing permissions to apply to the scan.

        Returns:
            :obj:`dict`:
                The scan resource for the created scan.

        Examples:
            Creating a scan for a single host:

            >>> nessus.scans.edit(scan_id=11241, enabled=True, targets='127.0.0.1', description='Another scan was just edited')
        """
        uuid = None
        if "uuid" in kw:
            uuid = kw["uuid"]
        elif "template_name" in kw:
            uuid = self.nessus.editor.get_uuid_by_name("scan", kw["template_name"])
        elif "template_title" in kw:
            uuid = self.nessus.editor.get_uuid_by_title("scan", kw["template_title"])

        payload = dict()
        if uuid:
            payload["uuid"] = uuid

        if "name" not in kw:
            getter = self.details(scan_id, fields={'info'})
            kw["name"] = getter['info'][0]['name']

        kw["text_targets"] = kw["targets"]
        payload["settings"] = self._constructor(**kw)

        return self.execute("PUT", f"/scans/{scan_id}", data=payload)


    def copy(self, scan_id, name=None):
        """
        Clones the scan instance.
        """
        payload = {"name": name}

        cpy = self.execute("POST", f"/scans/{scan_id}/copy", data=payload)
        return cpy

    def details(self, scan_id, fields=None):
        """
        Returns the details for a specific scan.

        Args:
            scan_id (int):
                The identifier for the scan.
            fields (list, optional):
                A list of attributes to return.

        Returns:
            :obj:`dict`:
                The alert resource record.

        Examples:
            >>> details = nessus.scans.detail(10001)
            >>> pprint(details)
        """
        scan = self.execute("GET", f"/scans/{scan_id}")
        det = dict()
        if fields:
            for f in fields:
                det[f] = []
                det[f].append(scan.get(f, "n/a"))
            return det
        else:
            return scan

    def launch(self, scan_id, alt_targets=None):
        """
        Launches a scan definition.

        Args:
            id (int):
                The id of the scan to launch.
            alt_targets (list, optional):
                If specified, these targets will be scanned instead of the
                default. Value can be an list where each index is a target, or
                an list with a single index of comma separated targets.

        Returns:
            :obj:`dict`:
                A scan result resource for the newly launched scan.

        Examples:
            >>> sc.scans.launch(100001)
        """
        payload = dict()
        if alt_targets:
            payload["alt_targets"] = alt_targets

        return self.execute("POST", f"/scans/{scan_id}/launch", data=payload)

    def pause(self, scan_id):
        '''
        Pauses a running scan instance.
        Args:
            scan_id (int): The identifier for the scan to pause.
        '''
        ret = dict()
        ret["response"] = []
        pause = self.execute("POST", f"/scans/{scan_id}/pause")
        return type(pause)


    def resume(self, scan_id):
        '''
        Resumes a paused scan instance.
        Args:
            scan_id (int): The identifier for the scan to resume.
        '''
        res = self.execute("POST", f"/scans/{scan_id}/resume")

        return res


    def stop(self, scan_id):
        '''
        Stops a running scan instance.
        Args:
            scan_id (int): The identifier for the scan to stop.
        '''
        stp = self.execute("POST", f"/scans/{scan_id}/stop")

        return stp

    def delete(self, scan_id):
        """
        Removes the specified scan from Nessus.

        Args:
            scan_id (int): The identifier for the scan to delete.

        Returns:
            :obj:`list`:
                The list of scan id removed.

        Examples:
            >>> nessus.scans.delete(10001)
        """
        return self.execute("DELETE", f"/scans/{scan_id}")

    def list(self, fields=None):
        """
        Retrieves the list of scan definitions.

        Args:
            fields (list, optional):
                A list of attributes to return for each scan.

        Returns:
            :obj:`list`:
                A list of scan resources.

        Examples:
            >>> for scan in nessus.scans.list():
            ...     pprint(scan)
        """
        return self.execute("GET", "/scans")
