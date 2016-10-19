#-------------------------------------------------------------------------------

#   ServiceManager.py
#
#   Purpose: Creates, updates, deletes services in ArcGIS Online
#
#
#   Prerequisites/Inputs:
#       TokenManager: authentication token for NPS ArcGIS Online
#       ServiceConfiguration: service configuration structure
#       ServiceSource: service content
#
#       XML metadata template in known subfolder (<somewhere>/Templates/Metadata)
#       Working Folder/Workspace
#
#   Outputs:
#       Create: feature service in ArcGIS Online repository
#       Manage: updated feature service in ArcGIS Online repository
#       Delete: log of deleted service(s)
#
#   Created by:  NPS Inventory and Monitoring Division Staff
#   Update date: 20161017
#
#
#
#-------------------------------------------------------------------------------

import TokenManager
from TokenManager import TokenManager
import ServiceConfiguration
from ServiceConfiguration import ServiceConfiguration
import ServiceSource
#import requests
import urllib
import urllib2
import arcrest

class ServiceManager(object):
    '''
    INFO
    ----
    Object to manage ArcGIS Online feature services

    '''
    token = None
    serviceConfiguration = None
    admin = None

    def __init__(self):
        tm = TokenManager("Portal", "https://nps.maps.arcgis.com", "IMDGISTeam", "G3010g!c2016", "https://irma.nps.gov")
        tm.getToken()
        self.token = tm.token
        self.admin = tm.admin
        sc = ServiceConfiguration(itype="Map Service", url="http://irmaservices.nps.gov/arcgis/rest/services/Inventory_Geology/Digital_Geologic_Map_of_Long_Island_New_York/MapServer", title="Test Service", description="This is a test service")
        self.serviceConfiguration = sc.serviceConfig

if __name__=='__main__':
    sm = ServiceManager()
    serviceToken = sm.token
    admin = sm.admin
    print serviceToken
    serviceInfo = sm.serviceConfiguration
    print serviceInfo
    content = admin.content
    userInfo = content.users.user()
    for folder in userInfo.folders:
        if folder['title'] == 'NPS_NaturalResource_Inventories':
            targetFolder = folder['id']
    #targetFolder = userInfo.folders
    # Code below posts via ArcRest generic technique - guessing this works when hitting AGS - does not work when hitting AGOL but
    # active adminURL response returns a list of every service on the server... so it is getting somewhere
    # see http://gis.stackexchange.com/questions/178127/arcgis-rest-api-using-additem-with-secure-service for info
    ##payload = {'token': serviceToken, 'url': 'http://irmaservices.nps.gov/arcgis/rest/services/Inventory_Geology/Digital_Geologic_Map_of_Long_Island_New_York/MapServer', 'title': 'IMD_TestService', 'type': 'Map Service'}
    ##adminURL = 'https://services1.arcgis.com/fBc8EJBxQRMcHlei/content/users/{}/{}/addItem'.format('IMDGISTeam', 'NPS_NaturalResource_Inventories')
    #adminURL = 'https://services1.arcgis.com/fBc8EJBxQRMcHlei/arcgis/rest/admin/addItem'#.format('IMDGISTeam', 'NPS_NaturalResource_Inventories')
    #adminURL = 'https://nps.maps.arcgis.com/sharing/rest/{}/{}/addItem'.format('IMDGISTeam', 'NPS_NaturalResource_Inventories')
    #adminURL = 'https://nps.maps.arcgis.com/sharing/rest/content/users/{}/{}/addItem'.format('IMDGISTeam', 'NPS_NaturalResource_Inventories')
    #adminURL = 'https://nps.maps.arcgis.com/content/users/{}/{}/addItem'.format('IMDGISTeam', 'NPS_NaturalResource_Inventories')
    ##data = urllib.urlencode(payload)
    ##req = urllib2.Request(adminURL, data)
    ##resp = urllib2.urlopen(req)
    ##a = resp.read()
    #test = {'url': 'http://irmaservices.nps.gov/arcgis/rest/services/Inventory_Geology/Digital_Geologic_Map_of_Long_Island_New_York/MapServer', 'serviceProxyParams': None, 'itemParameters': {"title": "Test Service", "type": "Map Service", 'overwrite': True, "description": "This is a test service", "tags": "National Park Service, NPS, NPS Inventory and Monitoring"}, 'metadata': None}
    #item = userInfo.addItem(test)
    itemParams = arcrest.manageorg.ItemParameter()
    itemParams.type = "Map Service"
    itemParams.title = "IMD Test"
    itemParams.description = "Test"
    itemParams.tags = "NPS"
    itemParams.overwrite = True
    #print type(itemParams)

    ip = str(itemParams)
    print ip
    serviceConfig = {}
    serviceConfig["itemParameters"] = str(itemParams)#ip.replace("'{","{").replace("}'","}")
    serviceConfig["url"] = "http://irmaservices.nps.gov/arcgis/rest/services/Inventory_Geology/Digital_Geologic_Map_of_Long_Island_New_York/MapServer"
    serviceConfig["overwrite"] = "True"
    serviceConfig["serviceProxyParams"] = ""
    serviceConfig["metadata"] = ""
    #item = userInfo.addItem(serviceInfo)
    print str(serviceConfig).replace("'", '\"')
    # This direct request works although the overwrite and folder params are ignored
    item = userInfo.addItem(itemParameters=itemParams,url="http://irmaservices.nps.gov/arcgis/rest/services/Inventory_Geology/Digital_Geologic_Map_of_Long_Island_New_York/MapServer", overwrite=True, folder=targetFolder)
    #item = userInfo.addItem(str(serviceConfig).replace("'", '\"'))
    print item.title

