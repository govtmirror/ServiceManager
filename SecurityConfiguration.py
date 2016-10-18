#-------------------------------------------------------------------------------

#   SecurityConfiguration.py
#
#   Configuration parameters for ArcGIS Online AGOL security
#
#
#   Prerequisites/Inputs:
#       ArcGIS Online URL
#
#
#   Outputs:
#       Dictionary of security configuration values
#
#   Created by:  NPS Inventory and Monitoring Division Staff
#   Update date: 20161017
#
#-------------------------------------------------------------------------------

class SecurityConfiguration(object):
    '''
    INFO
    ----
    Configuration dictionary used to request and return token for
    ArcGIS Online (AGOL) connection

    '''
    securityConfig = {}

    def __init__(self, stype, url, user, pwd, referer):
        self.securityConfig['security_type'] = stype
        self.securityConfig['org_url'] = url
        self.securityConfig['username'] = user
        self.securityConfig['password'] = pwd
        self.securityConfig['referer_url'] = referer
