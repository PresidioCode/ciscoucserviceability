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

 - See examples.py for complete code examples for each operation