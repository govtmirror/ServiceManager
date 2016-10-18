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
#   Update date: 20161017
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
    Configuration object (ItemParameter) used to manage a feature service in
    ArcGIS Online (AGOL)

    '''
    serviceConfig = {}

    def __init__(self, itype, title, description, url, overwrite="True", tags="National Park Service, NPS, NPS Inventory and Monitoring"):
        itemParams = arcrest.manageorg.ItemParameter()
        itemParams.type = itype
        itemParams.title = title
        itemParams.description = description
        itemParams.tags = tags
        itemParams.overwrite = overwrite
        #print type(itemParams)

        ip = str(itemParams)
        print ip
        self.serviceConfig["itemParameters"] = (ip.replace("'{","{")).replace("}'","}")
        self.serviceConfig["url"] = url
        self.serviceConfig["overwrite"] = overwrite
        self.serviceConfig["serviceProxyParams"] = ""
        self.serviceConfig["metadata"] = ""
