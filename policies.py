from base import TypeCheck
import numbers
import time

class ScanPolicy:
    def _constructor(self, **kw):
        '''
        Document constructor for scan policies.
        '''
        if 'name' in kw:
            # Verify that the name attribute is a string.
            TypeCheck('name', kw['name'], str)

        if 'context' in kw:
            # Verify the context if supplied.
            TypeCheck('context', kw['context'], str, choices=['scan', ''])

        if 'description' in kw:
            # Verify that the description is a string
            TypeCheck('description', kw['description'], str)

        if 'tags' in kw:
            # Verify that the tags keyword is a string.
            TypeCheck('tags', kw['tags'], str)

        if 'preferences' in kw:
            # Validate that all of the preferences are K:V pairs of strings.
            for key in TypeCheck('preferences', kw['preferences'], dict):
                TypeCheck('preference:{}'.format(key), key, str)
                TypeCheck('preference:{}:value'.format(key),
                    kw['preferences'][key], str)

        if 'audit_files' in kw:
            # unflatten the audit_files list into a list of dictionaries.
            kw['auditFiles'] = [{'id': TypeCheck('auditfile_id', a, int)}
                for a in TypeCheck('audit_files', kw['audit_files'], list)]
            del(kw['audit_files'])

        if 'template_id' in kw:
            # convert the policy template id into the appropriate sub-document.
            kw['policyTemplate'] = {
                'id': TypeCheck('template_id', kw['template_id'], int)
            }
            del(kw['template_id'])

        if 'profile_name' in kw:
            # convert the snake-cased "profile_name" into the CamelCase
            # policyProfileName.
            kw['policyProfileName'] = TypeCheck(
                'profile_name', kw['profile_name'], str)
            del(kw['profile_name'])

        if 'xccdf' in kw:
            # convert the boolean xccdf flag into the string equivalent of
            # generateXCCDFResults.
            kw['generateXCCDFResults'] = str(TypeCheck(
                'xccdf', kw['xccdf'], bool)).lower()
            del(kw['xccdf'])

        if 'owner_id' in kw:
            # Convert the owner integer id into CamelCase equiv.
            kw['ownerID'] = TypeCheck('owner_id', kw['owner_id'], int)
            del(kw['owner_id'])
        return kw


    def __init__(self, nessus_connection):
        self.nessus = nessus_connection


    def execute(self, *args, **kwargs):
        """proxy method"""
        return self.nessus.execute(*args, **kwargs)


    def copy(self, policy_id):

        return self.execute('POST', f'/policies/{policy_id}/copy')


    def delete(self, policy_id):

        return self.execute('DELETE', f'/policies/{policy_id}')


    def details(self, policy_id, fields=None):

        det = dict()
        pol = self.execute('GET', f'/policies/{policy_id}')

        if fields:
            for f in fields:
                det[f] = []
                det[f].append(pol.get(f, "n/a"))
                return det

        else:
            return pol


    def export_policy(self, policy_id, fobj):
        """
        export policy by id to file-like object
        :param policy_id:
        :param fobj:
        :return:
        """
        assert isinstance(policy_id, numbers.Integral)

        resp = self.execute("GET", f"/policies/{policy_id}/export/prepare")
        try:
            token = resp['token']
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

        det = dict()
        ls = self.execute('GET', '/policies')

        if fields:
            for f in fields:
                det[f] = []
                det[f].append(ls.get(f, "n/a"))
                return det

        else:
            return ls
