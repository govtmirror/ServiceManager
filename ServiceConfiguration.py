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

    def __init__(self
            , itype
            , title
            , description
            , url
            , overwrite=True
            , tags=None
            , snippet=None
            , accessInformation=None
            , metadata=None):
        self.itemParams = arcrest.manageorg.ItemParameter()
        self.itemParams.type = itype
        self.itemParams.url = url # required in itemParameters if posting a map service
        self.itemParams.title = title
        self.itemParams.description = description
        if tags is not None:
            tags = "National Park Service, NPS, NPS Inventory and Monitoring" + ", " + tags
        else:
            tags = "National Park Service, NPS, NPS Inventory and Monitoring"
        self.itemParams.tags = tags
        if snippet is not None:
            self.itemParams.snippet = snippet
        self.itemParams.overwrite = overwrite
        if accessInformation is not None:
            self.itemParams.accessInformation = accessInformation
        if metadata is not None:
            self.itemParams.metadata = metadata
        #print type(itemParams)

        # 20161019: addItem lacks a metadata parameter
        #self.serviceConfig["metadata"] = ""
