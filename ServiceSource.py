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

class ServiceSource(object):
    '''
    INFO
    ----
    Object to manage service sources

    '''
    serviceSources = {}
    sourceList = [] # array of source identifiers

    def __init__(self, sourceLocation=None, sourceFilter=None):
        # Connect to sourceLocation
        # Example: https://irmaservices.nps.gov/datastore-secure/v4/rest/AdvancedSearch
        #sourceFilter = {}
        sourceFilter = {'units': [{
              "order": '0',
              "logicOperator": 'null',
              "unitCode": "GRKO",
              "linked": 'true',
              "approved": 'false'}]}
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

        reqURL = sourceLocation
        # Request sources using filter
        print reqURL
        print str(sourceFilter)

        data = urllib.urlencode(sourceFilter)
        print data
        req = urllib2.Request(sourceLocation, data, {'Accept':'application/json'})
        resp = urllib2.urlopen(req)
        a = json.loads(resp.read())
        print len(a['items'])
        print [item['referenceId'] for item in a['items']]

    def getSources(self):
        pass

if __name__=='__main__':
    ss = ServiceSource(sourceLocation="http://irmaservices.nps.gov/datastore/v4/rest/AdvancedSearch/Composite?top=1&format=json")
