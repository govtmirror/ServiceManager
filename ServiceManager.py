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
#import TokenManager
from TokenManager import TokenManager
import ServiceConfiguration
from ServiceConfiguration import ServiceConfiguration
#import ServiceSource
from ServiceSource import ServiceSource

class ServiceManager(object):
    '''
    INFO
    ----
    Object to manage ArcGIS Online feature services

    '''
    token = None
    admin = None

    def __init__(self):
        if self.token == None:
            tm = TokenManager("Portal", "https://nps.maps.arcgis.com", "IMDGISTeam", "G3010g!c2016", "https://irma.nps.gov")
            tm.getToken()
            self.token = tm.token
        if self.admin == None:
            self.admin = tm.admin

    def getConfiguration(self, itype, title, description, url=None, tags=None, snippet=None, accessInformation=None, metadata=None):
        sc = ServiceConfiguration(itype=itype, title=title
        , description=description
        , url=url
        , tags=tags
        , snippet=snippet
        , accessInformation=accessInformation
        , metadata=metadata)
        return sc.itemParams

if __name__=='__main__':
    sm = ServiceManager()
    serviceToken = sm.token
    admin = sm.admin
    print serviceToken
    content = admin.content
    userInfo = content.users.user()

    ss = ServiceSource()
    # Data Store/ServCat example
    ss.sourceFilter = ss.dsscConnection("GRI", "GeospatialDataset")
    ss.sourceList = ss.getDSSCSources("http://irmaservices.nps.gov/datastore/v4/rest/AdvancedSearch/Composite?top=2000&format=json")

    # ArcGIS Server example
    #ss.agsConnection("https://inp2300fcvhafo1", "arcgis_admin", "admin2016...")
    #ss.sourceList = ss.getAGSSources(ss.agsServer, "Inventory_Geology")

    # Metadata: may work if convert this to an XML object: , metadata="https://irma.nps.gov/DataStore/DownloadFile/544273"
    for i in range(1, len(ss.sourceList['serviceName'])):
        itemParameters = sm.getConfiguration(itype="Map Service"
                    , title=ss.sourceList['serviceName'][i]
                    , description=ss.sourceList['description'][i]
                    , url=ss.sourceList['serviceURL'][i]
                    #, url=urllib.urlencode(ss.sourceList['serviceURL'][i])
                    , tags="National Park Service (NPS) Geologic Resources Inventory (GRI), Geology"
                    , snippet="Digital Data, Digital Geologic Map"
                    , accessInformation="National Park Service (NPS) Geologic Resources Inventory (GRI) program")
        print ss.sourceList['serviceURL'][i]
        #print str(itemParameters)

        # This request works although the overwrite and folder params are ignored
        item = userInfo.addItem(itemParameters=itemParameters, overwrite=True)
        print item.title

