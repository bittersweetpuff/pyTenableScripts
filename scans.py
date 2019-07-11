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
            '''
            Handles parsing the keywords and returns a scan definition document
            '''
            if 'name' in kw:
                # simply verify that the name attribute is a string.
                TypeCheck('name', kw['name'], str)

            if 'type' in kw:
                # If the scan type is manually specified, then we will want to make
                # sure that its a valid input.
                TypeCheck('type', kw['type'], str, choices=['plugin', 'policy'])

            if 'description' in kw:
                # The description should always be a string value.
                TypeCheck('description', kw['description'], str)

            if 'repo' in kw:
                # as we accept input as a integer, we need to expand the repository
                # attribute to be a dictionary item with just the ID (per API docs)
                kw['repository'] = {'id': TypeCheck(
                    'repo', kw['repo'], int)}
                del(kw['repo'])

            if 'scan_zone' in kw:
                # similarly to the repository, the API expects the zone to be
                # defined as a sub-dictionary with just the id field.
                kw['zone'] = {'id': TypeCheck(
                    'scan_zone', kw['scan_zone'], int, default=0)}
                del(kw['scan_zone'])

            if 'email_complete' in kw:
                # As emailOnFinish is effectively a string interpretation of a bool
                # value, if the snake case equivalent is used, we will convert it
                # into the expected parameter and remove the snake cased version.
                kw['emailOnFinish'] = str(TypeCheck(
                    'email_complete', kw['email_complete'], bool, default=False)).lower()
                del(kw['email_complete'])

            if 'email_launch' in kw:
                # As emailOnLaunch is effectively a string interpretation of a bool
                # value, if the snake case equivalent is used, we will convert it
                # into the expected parameter and remove the snake cased version.
                kw['emailOnLaunch'] = str(TypeCheck(
                    'email_launch', kw['email_launch'], bool, default=False)).lower()
                del(kw['email_launch'])

            if 'timeout' in kw:
                # timeout is the checked version of timeoutAction.  If timeout is
                # specified, we will check to make sure that the action is a valid
                # one, put the result into timeoutAction, and remove timeout.
                kw['timeoutAction'] = TypeCheck('timeout', kw['timeout'], str,
                    choices=['discard', 'import', 'rollover'], default='import')
                del(kw['timeout'])

            if 'vhosts' in kw:
                # As scanningVirtualHosts is effectively a string interpretation of
                # a bool value, if the snake case equivalent is used, we will
                # convert it into the expected parameter and remove the snake cased
                # version.
                kw['scanningVirtualHosts'] = str(TypeCheck(
                    'vhosts', kw['vhosts'], bool, default=False)).lower()
                del(kw['vhosts'])

            if 'rollover' in kw:
                # The scan rolloverType parameter simply shortened to better conform
                # to pythonic naming convention.
                kw['rolloverType'] = TypeCheck('rollover', kw['rollover'], str,
                    choices=['nextDay', 'template'], default='template')
                del(kw['rollover'])

            if 'targets' in kw:
                # targets is list representation of a comma-separated string of
                # values for the ipList attribute.  By handling as a list instead of
                # the raw string variant the API expects, we can ensure that there
                # isn't any oddities, such as extra spaces, between the commas.
                kw['ipList'] = ','.join([TypeCheck('target', i.strip(), str)
                    for i in TypeCheck('targets', kw['targets'], list)])
                del(kw['targets'])

            if 'max_time' in kw:
                # maxScanTime is a integer encased in a string value.  the snake
                # cased version of that expects an integer and converts it into the
                # string equivalent.
                kw['maxScanTime'] = str(TypeCheck('max_time', kw['max_time'], int))
                del(kw['max_time'])

            if 'auto_mitigation' in kw:
                # As classifyMitigatedAge is effectively a string interpretation of
                # an int value, if the snake case equivalent is used, we will
                # convert it into the expected parameter and remove the snake cased
                # version.
                kw['classifyMitigatedAge'] = str(TypeCheck(
                    'auto_mitigation', kw['auto_mitigation'], int, default=0)).lower()
                del(kw['auto_mitigation'])

            # hand off the building the schedule sub-document to the schedule
            # document builder.
            if 'schedule' in kw:
                kw['schedule'] = self._schedule_constructor(kw['schedule'])

            if 'reports' in kw:
                # as the reports list should already be in a format that the API
                # expects, we will simply verify that everything looks like it should.
                for item in TypeCheck('reports', kw['reports'], list):
                    TypeCheck('report:id', item['id'], int),
                    TypeCheck('reportSource', item['reportSource'], str, choices=[
                        'cumulative',
                        'patched',
                        'individual',
                        'lce',
                        'archive',
                        'mobile'
                    ])

            if 'asset_lists' in kw:
                # asset_lists is the collapsed list of id documents that the API
                # expects to see.  We will check each item in the list to make sure
                # its in the right type and then expand it into a sub-document.
                kw['assets'] = [{'id': TypeCheck('asset_list:id', i, int)}
                    for i in TypeCheck('assets_lists', kw['asset_lists'], list)]
                del(kw['asset_lists'])

            if 'creds' in kw:
                # creds is the collapsed list of id documents that the API expects
                # to see.  We will check each item in the list to make sure its in
                # the right type and then expand it into a sub-document.
                kw['credentials'] = [{'id': TypeCheck('cred:id', i, int)}
                    for i in TypeCheck('creds', kw['creds'], list)]
                del(kw['creds'])

            # Lastly, we need to handle the scan types automatically...
            if 'plugin_id' in kw and 'policy_id' in kw:
                # if both are specified, something is wrong here and we should throw
                # an exception.
                raise UnexpectedValueError(
                    'specify either a plugin_id or a policy_id for a scan, not both.')

            elif 'plugin_id' in kw:
                # If just the plugin_id is specified, then we are safe to assume
                # that this is a plugin-based scan.  set the pluginID attribute as
                # the API would expect and remove the snake cased variant that was
                # inputted.
                kw['type'] = 'plugin'
                kw['pluginID'] = TypeCheck('plugin_id', kw['plugin_id'], int)
                del(kw['plugin_id'])

            elif 'policy_id' in kw:
                # If just the policy_id is specified, then we are safe to assume
                # that this is a policy-based scan.  set the policy id attribute
                # within the policy document as the API would expect and remove the
                # snake cased variant that was inputted.
                kw['type'] = 'policy'
                kw['policy'] = {'id': TypeCheck('policy_id', kw['policy_id'], int)}
                del(kw['policy_id'])

            return kw


    def __init__(self, nessus_connection):
        self.nessus = nessus_connection


    def execute(self, *args, **kwargs):
        """proxy method"""
        return self.nessus.execute(*args, **kwargs)


    def create(self, name, repo, **kw):
        '''
        Creates a scan definition.
        '''
        kw['name'] = name
        kw['repo'] = repo

        # If the policy_id or plugin_id is set (as one or the other generally
        # should be) then we will automatically set the scan type based on
        # which of the values is defined.
        if 'policy_id' in kw:
            kw['type'] = 'policy'
        elif 'plugin_id' in kw:
            kw['type'] = 'plugin'

        scan = self._constructor(**kw)
        return self.execute("POST", "/scans", data=scan )



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
        if fields:
            for f in fields:
                det[f] = []
                det[f].append(scan.get(f, "n/a"))
            return det
        else:
            return scan



    def launch(self, scan_id, diagnostic_target=None, diagnostic_password=None):

        payload = dict()
        if diagnostic_target and diagnostic_passwsord:
            payload['diagnosticTarget'] = TypeCheck(
                'diagnostic_target', diagnostic_target, str)
            payload['diagnosticPassword'] = TypeCheck(
                'diagnostic_password', diagnostic_password, str)

        return self.execute("POST", f"/scans/{scan_id}/launch", data=payload)


    def delete(self, scan_id):

        return self.execute("DELETE", f"/scans/{scan_id}")


    def list(self, fields=None):

        return self.execute("GET", "/scans")
