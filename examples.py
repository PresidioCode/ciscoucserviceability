import os
from ciscoservicability import sxml
from py_dotenv import read_dotenv
import datetime
from ciscoaxl import axl
from prettytable import PrettyTable
pt = PrettyTable()

#read environment variables from a .env file in current path
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
read_dotenv(dotenv_path)
cucm = os.getenv('cucm')
web_username = os.getenv('web_username')
web_password = os.getenv('web_password')
os_username = os.getenv('os_username')
os_password = os.getenv('os_password')
cucm_version = os.getenv('cucm_version')

#instantiate axl instance to get a list of the nodes in the cluster
ucm = axl(username=web_username,password=web_password,cucm=cucm,cucm_version=cucm_version)

#instantiate sxml instances for all nodes
service_hosts = []
callmans = ucm.list_process_nodes()
for callman in callmans:
    if callman.name != 'EnterpriseWideData':
        service_hosts.append(
            sxml(
                username=web_username, 
                password=web_password, 
                osusername=os_username,
                ospassword=os_password,
                cucm=callman.name
            )
        )


'''
list_products
returns list
.ProductName: String
.ProductVersion: String
.ProductDescription: String
.ProductID: String
.ShortName: String
'''
def listProducts():
    products = ucm.list_products()
    for product in products:
        print(product.ProductName,': ', product.ProductVersion)

'''
list_services
returns list
.ServiceName: String
.ServiceType: String
.Deployable: Boolean
.GroupName: String
.DependentServices: List
'''

def listServices():
    services = service_hosts[0].list_services()
    for service in services:
        print(service.ServiceName)

'''
status
returns list
.ServiceName: String
.ServiceStatus: String
.ReasonCode: int
.ReasonCodeString: String
.StartTime: DateTime
.UpTime: Seconds
'''

def getStatus(service='', node=''):
    if node == '':
        pt.field_names = ['Host', 'Service', 'Status', 'Uptime']
        pt.align = "l"
        for host in service_hosts:
            statuses = host.status(service)
            for status in statuses:
                row = []
                row.append(host.cucm)
                row.append(status.ServiceName)
                row.append(status.ServiceStatus)
                row.append(str(datetime.timedelta(seconds=status.UpTime)))
                pt.add_row(row)
        print(pt)
    else:
        for host in service_hosts:
            if host.cucm == node:
                statuses = host.status(service)
                for status in statuses:
                    row = []
                    row.append(host.cucm)
                    row.append(status.ServiceName)
                    row.append(status.ServiceStatus)
                    row.append(str(datetime.timedelta(seconds=status.UpTime)))
                    pt.add_row(row)
            print(pt)

'''
restart(node, service)
returns String
'''

def restart(service, node=''):
    if node == '': #restart service on all nodes
        for host in service_hosts:
            req = host.restart(node=host.cucm, service=service)
            print(req)
    else: #find instance of node and restart service on that node only
        for host in service_hosts:
            if host.cucm == node:
                req = host.restart(node=host.cucm, service=service)
                print(req)

'''
start(node, service)
returns String
'''

def start(service, node=''):
    if node == '': #start service on all nodes
        for host in service_hosts:
            req = host.start(node=host.cucm, service=service)
            print(req)
    else: #find instance of node and start service on that node only
        for host in service_hosts:
            if host.cucm == node:
                req = host.start(node=host.cucm, service=service)
                print(req)


'''
stop(node, service)
returns String
'''

def stop(service, node=''):
    if node == '': #stop service on all nodes
        for host in service_hosts:
            req = host.stop(node=host.cucm, service=service)
            print(req)
    else: #find instance of node and stop service on that node only
        for host in service_hosts:
            if host.cucm == node:
                req = host.stop(node=host.cucm, service=service)
                print(req)

'''
activate(node, service)
returns String
'''

def activate(service, node=''):
    if node == '': #activate service on all nodes
        for host in service_hosts:
            req = host.activate(node=host.cucm, service=service)
            print(req)
    else: #find instance of node and activate service on that node only
        for host in service_hosts:
            if host.cucm == node:
                req = host.activate(node=host.cucm, service=service)
                print(req)

'''
deactivate(node, service)
returns String
'''

def activate(service, node=''):
    if node == '': #deactivate service on all nodes
        for host in service_hosts:
            req = host.deactivate(node=host.cucm, service=service)
            print(req)
    else: #find instance of node and deactivate service on that node only
        for host in service_hosts:
            if host.cucm == 'node':
                req = host.deactivate(node=host.cucm, service=service)
                print(req)

def main():
    #restart(service='Cisco Tomcat', node='ccm-tftp-srvr-03.kdhcd.org')
    getStatus(service='Cisco Tomcat')
if __name__ == "__main__":
    main()