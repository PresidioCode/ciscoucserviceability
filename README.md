# Python SDK for Cisco CUCM Servicability API

## Servicability API Documentation
 - https://developer.cisco.com/docs/sxml/#!control-center-services-api-reference

## Use Cases

 - Retrieve status of services
 - Start/Stop/Restart a service
 - Activate/Deactivate a service

## Notes

 - The API relies on `Cisco Tomcat`, so this is reset via SSH and requires osadmin privileges
 - SDK needs to be instanciated per CUCM node
 - `ciscoaxl` SDK can be used to list the process nodes

## Instructions

 - git clone this repository
 - pip install -r requirements.txt

## Examples

```sh
(ciscoservicability) jlevensailor in ~/Dev/ciscoservicability on master 🌮 python test.py

+----------------------------+--------------+---------+---------+
| Host                       | Service      | Status  | Uptime  |
+----------------------------+--------------+---------+---------+
| ccm-pub-srvr-01.cdpneighbors.com  | Cisco Tomcat | Started | 3:31:04 |
| ccm-sub-srvr-01.cdpneighbors.com  | Cisco Tomcat | Started | 3:40:13 |
| ccm-sub-srvr-02.cdpneighbors.com  | Cisco Tomcat | Started | 3:39:16 |
| ccm-sub-srvr-03.cdpneighbors.com  | Cisco Tomcat | Started | 3:36:11 |
| ccm-sub-srvr-04.cdpneighbors.com  | Cisco Tomcat | Started | 3:33:07 |
| ccm-tftp-srvr-01.cdpneighbors.com | Cisco Tomcat | Started | 3:38:16 |
| ccm-tftp-srvr-02.cdpneighbors.com | Cisco Tomcat | Started | 3:35:10 |
| ccm-tftp-srvr-03.cdpneighbors.org | Cisco Tomcat | Started | 0:36:54 |
+----------------------------+--------------+---------+---------+
```


For a complete list of examples, see `examples.py`