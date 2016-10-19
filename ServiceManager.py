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
#   Update date: 20161019
#
#
#
#-------------------------------------------------------------------------------

import urllib
import urllib2
import arcrest
import TokenManager
from TokenManager import TokenManager
import ServiceConfiguration
from ServiceConfiguration import ServiceConfiguration
import ServiceSource
from ServiceSource import ServiceSource

class ServiceManager(object):
    '''
    INFO
    ----
    Object to manage ArcGIS Online feature services

    '''
    token = None
    #serviceConfiguration = None # this is itemParameters
    admin = None

    def __init__(self):
        if self.token == None:
            tm = TokenManager("Portal", "https://nps.maps.arcgis.com", "IMDGISTeam", "G3010g!c2016", "https://irma.nps.gov")
            tm.getToken()
            self.token = tm.token
        if self.admin == None:
            self.admin = tm.admin

    def getConfiguration(self, itype, title, description, url=None):
        sc = ServiceConfiguration(itype=itype, title=title, description=description, url=url)
        #self.serviceConfiguration = sc.itemParams
        return sc.itemParams

if __name__=='__main__':
    sm = ServiceManager()
    serviceToken = sm.token
    admin = sm.admin
    print serviceToken
    itemParameters = sm.getConfiguration(itype="Map Service", title="IMD Test Service", description="Updated description", url="http://irmaservices.nps.gov/arcgis/rest/services/Inventory_Geology/Digital_Geologic_Map_of_Long_Island_New_York/MapServer")
    #itemParameters = sm.serviceConfiguration
    print str(itemParameters)
    #url="http://irmaservices.nps.gov/arcgis/rest/services/Inventory_Geology/Digital_Geologic_Map_of_Long_Island_New_York/MapServer"
    content = admin.content
    userInfo = content.users.user()

    # This direct request works although the overwrite and folder params are ignored
    item = userInfo.addItem(itemParameters=itemParameters, overwrite=True)
    print item.title

