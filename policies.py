from base import TypeCheck
import numbers
import time
import json


class ScanPolicy:
    def __init__(self, nessus_connection):
        self.nessus = nessus_connection

    def execute(self, *args, **kwargs):
        """proxy method"""
        return self.nessus.execute(*args, **kwargs)

    def copy(self, policy_id):
        """
        Clones the specified scan policy

        Args:
            id (int): The unique identifier for the source policy to clone.

        Returns:
            :obj:`dict`:
                The scan policy resource record for the newly created policy.

        Examples:
            >>> policy = nessus.policies.copy(10001)
            >>> pprint(policy)
        """
        return self.execute("POST", f"/policies/{policy_id}/copy")

    def delete(self, policy_id):
        """
        Removes a configured scan policy.

        Args:
            id (int): The unique identifier for the source policy to clone.

        Returns:
            :obj:`str`:
                The empty response from the API.

        Examples:
            >>> nessus.policies.delete(10001)
        """
        return self.execute("DELETE", f"/policies/{policy_id}")

    def details(self, policy_id, fields=None):
        """
        Retrieves the details for a specified policy.

        Args:
            id (int): The unique identifier for the policy
            fields (list, optional):
                The list of fields that are desired to be returned.  For details
                on what fields are available, please refer to the details on the
                request within the policy details API doc.

        Returns:
            :obj:`dict`:
                Details about the scan policy template

        Examples:
            >>> policy = nessus.policies.details(10001)
            >>> pprint(policy)
        """

        det = dict()
        pol = self.execute("GET", f"/policies/{policy_id}")

        if fields:
            for f in fields:
                det[f] = []
                det[f].append(pol.get(f, "n/a"))
                return det

        else:
            return pol

    def export_policy(self, policy_id, fobj):
        """
        Export the specified scan policy

        Args:
            id (int): The unique identifier for the scan policy to export.
            fobj (FileObject, optional):
                The file-like object to write the resulting file into.  If
                no file-like object is provided, a BytesIO objects with the
                downloaded file will be returned.  Be aware that the default
                option of using a BytesIO object means that the file will be
                stored in memory, and it's generally recommended to pass an
                actual file-object to write to instead.

        Returns:
            :obj:`FileObject`:
                The file-like object with the resulting export.

        Examples:
            >>> with open('example_policy.nessus', 'wb') as fobj:
            ...     nessus.policies.export_policy(10001, fobj)
        """
        assert isinstance(policy_id, numbers.Integral)

        resp = self.execute("GET", f"/policies/{policy_id}/export/prepare")
        try:
            token = resp["token"]
        except Exception:
            print(resp)
            return ""
        out = "waiting"
        i = 200
        while i > 0 and out != "ready":
            rq = f"/tokens/{token}/status"
            print(rq, token)
            out = self.execute("GET", rq)["status"]
            time.sleep(1)
            i -= 1
        rq = f"/tokens/{token}/download"
        out = self.execute("GET", rq)
        # LOGGER.info(f'{out}')
        fobj.write(out)
        return out

    def list(self, fields=None):
        """
        Retrieved the list of Scan policies configured.

        Args:
            fields (list, optional):
                The list of fields that are desired to be returned.  For details
                on what fields are available, please refer to the details on the
                request within the policy list API doc.

        Returns:
            :obj:`dict`:
                scan policies.

        Examples:
            >>> policies = nessus.policies.list()

        """
        det = dict()
        ls = self.execute("GET", "/policies")

        if fields:
            for f in fields:
                det[f] = []
                det[f].append(ls.get(f, "n/a"))
                return det

        else:
            return ls

    def template_details(self, fields=None, **kw):
        """
        Retrieves the details for a specified policy template.

        Args:
            id (int): The unique identifier for the policy template
            fields (list, optional):
                The list of fields that are desired to be returned.  For details
                on what fields are available, please refer to the details on the
                request within the policy template details API doc.
            uuid (str, optional):
                Templates uuid. At least one of the arguments (uuid, title, name
                ) cant be empty
            title (str, optional):
                Templates title. At least one of the arguments (uuid, title, name
                ) cant be empty
            name (str, optional):
                Templates name. At least one of the arguments (uuid, title, name
                ) cant be empty

        Returns:
            :obj:`dict`:
                Details about the scan policy template

        Examples:
            >>> template = nessus.policies.template_details(name="advanced")
            >>> pprint(template)
        """
        uuid = None
        if "uuid" in kw:
            uuid = kw["uuid"]
        elif "name" in kw:
            name = kw["name"]
            uuid = self.nessus.editor.get_uuid_by_name("policy", name)
        elif "title" in kw:
            title = kw["title"]
            uuid = self.nessus.editor.get_uuid_by_title("policy", title)
        else:
            raise Exception("Error: Bad Argument")

        details = self.nessus.editor.details("policy", uuid)

        if fields:
            det = dict()
            for f in fields:
                det[f] = details.get(f, "n/a")
                return det

        else:
            return details

    def template_list(self, fields=None):
        """
        Retrieved the list of scan policy templates.

        Args:
            fields (list, optional):
                The list of fields that are desired to be returned.  For details
                on what fields are available, please refer to the details on the
                request within the policy template list API doc.

        Returns:
            :obj:`list`:
                List of available policy templates

        Examples:
            >>> templates = nessus.policies.template_list()
            >>> for policy in templates:
            ...     pprint(policy)
        """
        result = self.nessus.editor.list("policy")
        buffer = dict()
        det = []
        if fields:
            for item in result["templates"]:
                for f in fields:
                    buffer[f] = item.get(f, "n/a")
                det.append(buffer.copy())
            return det
        else:
            return result
