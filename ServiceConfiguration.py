#-------------------------------------------------------------------------------

#   ServiceConfiguration.py
#
#   Configuration parameters for feature service
#
#
#   Prerequisites/Inputs:
#       Item type
#       Target folder (if applicable)
#
#
#       XML metadata template in known subfolder (<somewhere>/Templates/Metadata)
#       Working Folder/Workspace
#
#   Outputs:
#       Configuration as arcrest.manageorg.ItemParameter() object
#
#   Created by:  NPS Inventory and Monitoring Division Staff
#   Update date: 20161019
#
#
#
#-------------------------------------------------------------------------------

import arcrest
from arcrest import manageorg

class ServiceConfiguration(object):
    '''
    INFO
    ----
    Configuration object (ItemParameter) used to manage a service in
    ArcGIS Online (AGOL)

    '''
    itemParams = None
    #serviceConfig = {}

    def __init__(self, itype, title, description, url, overwrite=True, tags="National Park Service, NPS, NPS Inventory and Monitoring"):
        self.itemParams = arcrest.manageorg.ItemParameter()
        self.itemParams.type = itype
        self.itemParams.url = url # required in itemParameters if posting a map service
        self.itemParams.title = title
        self.itemParams.description = description
        self.itemParams.tags = tags
        self.itemParams.overwrite = overwrite
        #print type(itemParams)

        # 20161019: addItem lacks a metadata parameter
        #self.serviceConfig["metadata"] = ""
