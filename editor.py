

class Editor:

    def __init__(self, nessus_connection):
        self.nessus = nessus_connection


    def execute(self, *args, **kwargs):
        """proxy method"""
        return self.nessus.execute(*args, **kwargs)


    def list(self, type):
        return self.execute('GET', f'/editor/{type}/templates')


    def details(self, type, template_uuid):
        return self.execute('GET', f'/editor/{type}/templates/{template_uuid}')


    def plugin_description(self, policy_id, family_id, plugin_id):
        return self.execute('GET', f'/editor/policy/{policy_id}/families/{family_id}/plugins/{plugin_id}')  #NOT TESTED YET


    def get_uuid_by_name(self, type, name):
        result = self.list(type)
        for a in result['templates']:
            if a['name'] == name:
                return a['uuid']
        return None


    def get_uuid_by_title(self, type, title):
        result = self.list(type)
        for a in result['templates']:
            if a['title'] == title:
                return a['uuid']
        return None
