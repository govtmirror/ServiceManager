#-------------------------------------------------------------------------------

#   TokenManager.py
#
#   Token configuration and content for access to ArcGIS Online (AGOL)
#
#
#   Prerequisites/Inputs:
#       Account username and password
#       AGOL token URL
#
#
#   Outputs:
#       Token
#
#   Created by:  NPS Inventory and Monitoring Division Staff
#   Update date: 20161017
#
#
#
#-------------------------------------------------------------------------------

import arcrest
from arcresthelper import securityhandlerhelper
import SecurityConfiguration
#reload(SecurityConfiguration)
from SecurityConfiguration import SecurityConfiguration

class TokenManager(object):
    '''
    INFO
    ----
    Object to request and return token for AGOL connection

    '''
    agolURL = None
    agolUser = None
    agolPassword = None
    securityConfiguration = None
    token = None
    admin = None

    def __init__(self, securityType, url, user, pwd, referer):
        self.agolURL = url
        self.agolUser = user
        self.agolPassword = pwd
        sc = SecurityConfiguration(stype = securityType, url = url, user=user, pwd=pwd, referer=referer)
        self.securityConfiguration = sc.securityConfig

    '''
    INFO
    ----
    With agolURL, user, and password, requests and returns
    a token object.

    RETURNS
    -------
    token object

    '''
    def getToken(self):
        shh = securityhandlerhelper.securityhandlerhelper(self.securityConfiguration)

        if shh.valid == False:
            print shh.message
        else:
            self.admin = arcrest.manageorg.Administration(url=self.agolURL, securityHandler=shh.securityhandler)
            content = self.admin.content
            userInfo = content.users.user()

            self.token = shh.securityhandler.token


if __name__=='__main__':
    # service type = ArcGIS works if logged into AGOL via ArcMap or ArcGIS Administrator
    tm = TokenManager("Portal", "https://nps.maps.arcgis.com", "IMDGISTeam", "G3010g!c2016", "https://irma.nps.gov")

    tm.getToken()
    print tm.token
