#-------------------------------------------------------------------------------

#   ServiceSource.py
#
#   Source of feature service
#
#
#   Prerequisites/Inputs:
#       Target source of spatial dataset(s)
#           REST objects
#           Spatial files (GDB, SHP, GeoJSON)
#           etc eventually
#
#       XML metadata template in known subfolder (<somewhere>/Templates/Metadata)
#       Working Folder/Workspace
#
#   Outputs:
#       Dictionary of source content containing:
#           title, description, tag(s),
#           url (if map service)
#
#   Created by:  NPS Inventory and Monitoring Division Staff
#   Update date: 20161019
#
#
#
#-------------------------------------------------------------------------------
import json
import urllib2
import urllib
from TokenManager import TokenManager
#import arcrest

class ServiceSource(object):
    '''
    INFO
    ----
    Object to manage service sources

    '''
    serviceSources = {}
    sourceList = [] # array of source identifiers
    sourceFilter = None
    basicAGSQuery = None
    token = None
    agsServer = None

    def __init__(self, sourceLocation=None, sourceFilter=None):
        # Connect to sourceLocation
        # Example: https://irmaservices.nps.gov/datastore-secure/v4/rest/AdvancedSearch
        #sourceFilter = {}
        self.sourceFilter = {"units": [{
              "order": 0,
              "logicOperator": "null",
              "unitCode": "GRI",
              "linked": "true",
              "approved": "false"}]}
##        units = {'units': [{
##              "order": '0',
##              "logicOperator": 'null',
##              "unitCode": "GRI",
##              "linked": 'false',
##              "approved": 'false'}]}
##        referenceTypes = {'referenceTypes': [{
##              "order": '0',
##              "logicOperator": 'null',
##              "referenceType": "Geospatial Dataset"}]}
##        filter = {'units': [{
##              "order": '0',
##              "logicOperator": 'null',
##              "unitCode": "GRI",
##              "linked": 'false',
##              "approved": 'false'}]},{'referenceTypes': [{
##              "order": '0',
##              "logicOperator": 'null',
##              "referenceType": "Geospatial Dataset"}]}
        #digitalResources = {}
        #units['order'] = 0
        #units['logicOperator'] = "null"
        #units['unitCode'] = "GRI"
        #units['linked'] = "false"
        #units['approved'] = "false"
        #referenceTypes['order'] = 1
        #referenceTypes['logicOperator'] = "null"
        #referenceTypes['referenceType'] = "Geospatial Dataset"
        #digitalResources['type'] = "Web Service"
        #sourceFilter['visibility'] = "public"
        #sourceFilter['legacy'] = "excludeLegacy"
        #sourceFilter.update(units)
        #sourceFilter.update(referenceTypes)
        #sourceFilter['units'] = units
        #sourceFilter['referenceTypes'] = referenceTypes
        #sourceFilter['digitalResources'] = [digitalResources]

##        reqURL = sourceLocation
##        # Request sources using filter
##        print reqURL
##        print str(sourceFilter)
##
##        data = urllib.urlencode(sourceFilter)
##        print data
##        req = urllib2.Request(sourceLocation, data, {'Accept':'application/json'})
##        resp = urllib2.urlopen(req)
##        a = json.loads(resp.read())
##        print len(a['items'])
##        print [item['referenceId'] for item in a['items']]

    def agsConnection(self, serverURL, agsUser, agsPassword, referer='https://irma.nps.gov'):
        # Requires an admin connection
        tm = TokenManager("AGS", serverURL, agsUser, agsPassword, referer)
        tm.getToken()
        self.token = tm.token
        self.agsServer = tm.admin

    def dsscConnection(self, unitCode, referenceType=None):
        if referenceType is None:
            json = {"units": [{
                  "order": 0,
                  "logicOperator": "null",
                  "unitCode": unitCode,
                  "linked": "true",
                  "approved": "false"}]}
        else:
##            json = {"units": [{
##                  "order": 0,
##                  "logicOperator": "null",
##                  "unitCode": unitCode,
##                  "linked": "true",
##                  "approved": "false"}],
##                  "referenceTypes": [{
##                  "order": 0,
##                  "logicOperator": "null",
##                  "referenceType":  referenceType}]
##                  }
              json = {"units": [{
              "order": 0,
              "logicOperator": "null",
              "unitCode": unitCode,
              "linked": "true",
              "approved": "false"}],
              "referenceTypes": [{
              "order": 0,
              "logicOperator": "null",
              "referenceType":  referenceType}],
              "digitalResources": [{
              "order": 0,
              "logicOperator": "null",
              "type": "WebService",
              "fieldName": "Map",
              "searchText": "Inventory_Geology"}]
              }
        return json

    def getAGSSources(self, server, folder):
        services = dict()
        for sFolder in server.folders:
            server.currentFolder = sFolder
            if sFolder == folder:
                print sFolder
                services = dict(serviceName = [item.documentInfo['Title'] for item in server.services]
                , description = [item.description for item in server.services]
                , serviceURL = [item.url.replace('inp2300fcvhafo1:6080','irmaservices.nps.gov') for item in server.services])

                #for service in server.services:
                #    services['serviceName'] = service.documentInfo['Title']
                #    services['serviceURL'] = service.url.replace('inp2300fcvhafo1:6080','irmaservices.nps.gov')
                #    services['description'] = service.description

        return services

    def getDSSCSources(self, sourceLocation):
        reqURL = sourceLocation
        services = dict()
        # Request sources using filter
        print reqURL
        #print str(self.sourceFilter)

        dsLink = '<br/><br/> National Park Service <a href="https://irma.nps.gov/DataStore/Reference/Profile/">Data Store</a> record.'
        serviceNames = []
        serviceDescriptions = []
        serviceURLs = []

        data = json.dumps(self.sourceFilter)
        req = urllib2.Request(sourceLocation, data, {'Content-Type':'application/json'})
        resp = urllib2.urlopen(req)
        a = json.loads(resp.read())
        for item in a['items']:
            serviceURL = [x for x in item['linkedResources'] if x['resourceType'] =='Web Service'][0]['url']
            serviceName = 'IMD ' + (serviceURL.split('/')[7].replace('_',' '))
            serviceNames.append(serviceName)
            serviceDescriptions.append(item['title'].replace(u"\u2019", "'").replace(u"\x92", "'") + dsLink.replace('Profile/','Profile/'+ str(item['referenceId'])))
            serviceURLs.append(serviceURL)

        services['serviceName'] = serviceNames
        services['description'] = serviceDescriptions
        services['serviceURL'] = serviceURLs

        #print services
        return services

if __name__=='__main__':
    # Service source: AGS REST using arcrest security handler logic
    #ss = ServiceSource()
    #ss.agsConnection("https://inp2300fcvhafo1", "arcgis_admin", "admin2016...")
    #ss.sourceList = ss.getAGSSources(ss.agsServer, "Inventory_Geology")
    #print ss.sourceList

    # Service source: DS/SC REST
    ss = ServiceSource()
    ss.sourceFilter = ss.dsscConnection("GRI", "GeospatialDataset")
    sourceList = ss.getDSSCSources("http://irmaservices.nps.gov/datastore/v4/rest/AdvancedSearch/Composite?top=2000&format=json")
