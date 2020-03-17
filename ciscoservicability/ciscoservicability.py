"""
Class to interface with cisco ucm axl api.
Author: Jeff Levensailor
Version: 0.1
Dependencies:
 - zeep: https://python-zeep.readthereqcs.io/en/master/

Links:
 - https://developer.cisco.com/site/axl/
"""

import sys
from pathlib import Path
import os
from pexpect import pxssh
from requests import Session 
from requests.auth import HTTPBasicAuth 
import re
import urllib3 
from zeep import Client, Settings, Plugin 
from zeep.transports import Transport 
from zeep.cache import SqliteCache 
from zeep.plugins import HistoryPlugin 
from zeep.exceptions import Fault 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class sxml(object):
    """
    The AXL class sets up the connection to the call manager with methods for configuring UCM.
    Tested with environment of;
    Python 3.6
    """

    def __init__(self, username, password, cucm, osusername='', ospassword=''):
        """
        :param username: axl username
        :param password: axl password
        :param cucm: UCM IP address

        example usage:
        >>> from ciscoservicability import SXML
        >>> ucm = SXML('axl_user', 'axl_pass', '192.168.200.10')
        """

        cwd = os.path.dirname(os.path.abspath(__file__))
        if os.name == "posix":
            wsdl = Path(f"{cwd}/ControlCenterServices.wsdl").as_uri()
        else:
            wsdl = str(Path(f"{cwd}/ControlCenterServices.wsdl").absolute())
        session = Session() 
        session.verify = False 
        session.auth = HTTPBasicAuth(username, password) 
        settings = Settings(strict=False, xml_huge_tree=True, xsd_ignore_sequence_order=True) 
        transport = Transport(session=session, timeout=10, cache=SqliteCache()) 
        sxml_client = Client(wsdl, settings=settings, transport=transport) 

        self.wsdl = wsdl
        self.username = username
        self.password = password
        self.osusername = osusername
        self.ospassword = ospassword
        self.cucm = cucm
        self.client = sxml_client.create_service("{http://schemas.cisco.com/ast/soap}ControlCenterServicesBinding", f"https://{cucm}:8443/controlcenterservice2/services/ControlCenterServices")

    def list_products(self):
        try:
            products = []
            resp = self.client.getProductInformationList( '' )
            for item in resp.Products.item:
                products.append(item)
            return products
        except Fault as e:
            return e

    def list_services(self):
        try:
            resp = self.client.soapGetStaticServiceList( '' )
            return resp.item
        except Fault as e:
            return e

    def status(self, service=''):
        statuses = []
        try:
            resp = self.client.soapGetServiceStatus(service)
            for item in resp.ServiceInfoList.item:
                if item.UpTime < 1:
                    item.UpTime = 0
                statuses.append(item)
            return statuses
        except Fault as e:
            return e

    def restart(self, node, service):
        if service == 'Cisco Tomcat':
            try:
                s = pxssh.pxssh()
                hostname = node
                username = self.osusername
                password = self.ospassword
                s.PROMPT = 'admin:'
                s.login(hostname, username, password, auto_prompt_reset=False, login_timeout=10)
                s.expect('admin:')
                s.sendline(f'''utils service restart {service}''')
                s.prompt()
                return s.before.decode()
            except pxssh.ExceptionPxssh as e:
                return e
        else:
            service_list = []
            services = {}
            services['item'] = service
            req = {}
            req['NodeName'] = node
            req['ControlType'] = 'Restart'
            req['ServiceList'] = [services]
            try:
                return self.client.soapDoControlServices(req)
            except Fault as e:
                return e

    def stop(self, node, service):
        if service == 'Cisco Tomcat':
            try:
                s = pxssh.pxssh()
                hostname = node
                username = self.osusername
                password = self.ospassword
                s.login(hostname, username, password, login_timeout=10)
                s.expect('admin:')
                s.sendline(f'''utils service stop {service}''')
                s.prompt()
                return s.before.decode()
            except pxssh.ExceptionPxssh as e:
                return e
        else:
            service_list = []
            services = {}
            services['item'] = service
            req = {}
            req['NodeName'] = node
            req['ControlType'] = 'Stop'
            req['ServiceList'] = [services]
            try:
                return self.client.soapDoControlServices(req)
            except Fault as e:
                return e

    def start(self, node, service):
        if service == 'Cisco Tomcat':
            try:
                s = pxssh.pxssh()
                hostname = node
                username = self.osusername
                password = self.ospassword
                s.login(hostname, username, password, login_timeout=10)
                s.expect('admin:')
                s.sendline(f'''utils service start {service}''')
                s.prompt()
                return s.before.decode()
            except pxssh.ExceptionPxssh as e:
                return e
        else:
            service_list = []
            services = {}
            services['item'] = service
            req = {}
            req['NodeName'] = node
            req['ControlType'] = 'Start'
            req['ServiceList'] = [services]
            try:
                return self.client.soapDoControlServices(req)
            except Fault as e:
                return e

    def activate(self, node, service):
        service_list = []
        services = {}
        services['item'] = service
        req = {}
        req['NodeName'] = node
        req['DeployType'] = 'Deploy'
        req['ServiceList'] = [services]
        try:
            resp = self.client.soapDoServiceDeployment(req)
            return resp.ServiceInfoList.item[0].ServiceStatus
        except Fault as e:
            return e

    def deactivate(self, node, service):
        service_list = []
        services = {}
        services['item'] = service
        req = {}
        req['NodeName'] = node
        req['DeployType'] = 'UnDeploy'
        req['ServiceList'] = [services]
        try:
            resp = self.client.soapDoServiceDeployment(req)
            return resp.ServiceInfoList.item[0].ServiceStatus
        except Fault as e:
            return e