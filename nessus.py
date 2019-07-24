"""Nessus connector class to get reports"""

from jsonreader import *
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
from scans import *
from scaninstances import *
from files import *
from plugins import *
from uuidencoder import *
from policies import *
from groups import *
from users import *
from editor import *
from NessusDataKeeper import *


LOGGER = logging.getLogger()
ssl_context = urllib.request.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))
opener = urllib.request.build_opener(ssl_context)
urllib.request.install_opener(opener)
requests.packages.urllib3.disable_warnings()

LOGGER.info("starting Nessus module")

putout = " "

class Connector:
    """class to connect nessus with tenable sc api"""

    def __init__(self, url, port=None):
        self.scan_instances = ScanInstances(self)
        self.scans = Scans(self)
        self.file = File(self)
        self.policies = ScanPolicy(self)
        self.plugins = Plugin(self)
        self.groups = Group(self)
        self.users = User(self)
        self.editor = Editor(self)
        self.dataKeeper = NessusDataKeeper(self)
        self.res = None
        self.login_data = None
        self.token = None
        if port is not None:
            self.url = "{0}:{1}".format(url, port)
        else:
            self.url = url
        if not self.url.startswith("https://"):
            self.url = "https://%s" % self.url

    def __enter__(self):
        LOGGER.debug("entering debug mode")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if "token" in self.__dict__ and self.token is not None:
            self.logout()

    def execute(self, method, resource, data=None):
        """
        Send a request
        Send a request to Nessus based on the specified data. If the session token
        is available add it to the request. Specify the content type as JSON and
        convert the data to JSON format.
        """
        if data is None:
            data = {}
        method = method.upper()
        headers = {"X-Cookie": "token={0}".format(self.token)}
        headers.update({"Content-type": "application/json"})
        verify = False
        datar = json.dumps(data, cls=UUIDEncoder)
        if method == "POST":
            r = requests.post(
                self._build_url(resource), data=datar, headers=headers, verify=verify
            )
        elif method == "PUT":
            r = requests.put(
                self._build_url(resource), data=datar, headers=headers, verify=verify
            )
        elif method == "DELETE":
            r = requests.delete(
                self._build_url(resource), data=datar, headers=headers, verify=verify
            )
        else:
            r = requests.get(
                self._build_url(resource), params=datar, headers=headers, verify=verify
            )

        if r.status_code != 200:
            e = r.json()
            print("\t!!!", e.get("error", ""), e)
            return e.get("error", "n/a")
        if "download" in resource:
            self.res = r.content
        elif method == "DELETE":
            self.res = r
        else:
            try:
                self.res = r.json()
            except ValueError:
                print(r.content)
                self.res = {}
        return self.res

    def login(self, usr, pwd):
        """
        Login to nessus.
        """
        self.token = ""
        llogin = {"username": usr, "password": pwd}
        data = self.execute("POST", "/session", data=llogin)
        self.login_data = data
        # print(data)
        if isinstance(data, str):
            return data
        self.token = data["token"]
        return data["token"]

    def logout(self):
        """
        Logout of nessus.
        """
        self.execute("DELETE", "/session")
        LOGGER.debug("logged out")
        return "logged out"

    def _build_url(self, resource):
        return "{0}{1}".format(self.url, resource)






if __name__ == "__main__":
    import pprint
    import getpass

    #gpwd = getpass.getpass("provide nessus password")
    gpwd = GetPass()
    #guser = getpass.getuser()
    guser = GetUser()
    FMT = "%(asctime)-15s %(levelname)s	%(module)s %(lineno)d %(message)s"
    logging.basicConfig(format=FMT)
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.debug("starting")
    conektor = Connector(GetNessusConsole())
    my_fields = {'uuid', 'name', 'title'}


    with conektor:
        LOGGER.debug(f"{guser}")
        conektor.login(guser, gpwd)
        #pprint.pprint(conektor.scan_instances.list(gfields))
        #pprint.pprint(
        #    len(conektor.scan_instances.export_scan(11183, open("skan.nessus", "wb")))
        #)
        #pprint.pprint(conektor.scan_instances.details(11183, my_fields))
        #pprint.pprint(conektor.scan_instances.delete(11181))
        #pprint.pprint(conektor.scan_instances.pause(11183))
        #pprint.pprint(conektor.scans.create(template_name='advanced', name='Skan test1234', policy_id=11212, targets='127.0.0.1', description='opis skanu'))
        #pprint.pprint(conektor.scans.launch(11251))
        #pprint.pprint(conektor.scans.list())
        #conektor.dataKeeper.Prepare()
        #pprint.pprint(conektor.dataKeeper.BuildUUIDDict())
        #pprint.pprint(conektor.editor.list('scan'))
        #pprint.pprint(conektor.scans.resume(11251))
        #pprint.pprint(conektor.scans.stop(11251))
        #pprint.pprint(conektor.scans.delete(scan_id=11256))


        #result = conektor.scans.details(scan_id=11241, fields={'info'})


        #pprint.pprint(result['info'][0]['name'])
        #pprint.pprint(conektor.policies.create(template_title="Web Application Tests", name="Another Policy Bites the Dust"))

        #pprint.pprint(conektor.scan_instances.uploadTest(open("skan.nessus", "rb")))
