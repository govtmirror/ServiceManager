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
#from arcrest.security.security import AGSTokenSecurityHandler
from arcrest.manageags import AGSAdministration
#import SecurityConfiguration
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
    securityType = None
    securityConfiguration = None
    token = None
    admin = None

    def __init__(self, securityType, url, user, pwd, referer):
        self.agolURL = url
        self.agolUser = user
        self.agolPassword = pwd
        self.securityType = securityType
        if securityType is not None and securityType == 'AGS':
            sc = SecurityConfiguration(stype = securityType, url = url, user=user, pwd=pwd, referer=referer, proxy_url = None, proxy_port=None)
        elif securityType is not None:
            sc = SecurityConfiguration(stype = securityType, url = url, user=user, pwd=pwd, referer=referer)
        self.securityConfiguration = sc.securityConfig

    '''
    INFO
    ----
    With agolURL, user, and password, requests and returns
    a token object.

    See for refactoring ideas: http://anothergisblog.blogspot.com/2015/04/arcrest-basics-authentication.html

    RETURNS
    -------
    token object

    '''
    def getToken(self):
        if self.securityType == 'AGS':
            sh = arcrest.AGSTokenSecurityHandler(token_url=self.securityConfiguration['org_url'] + ':6443/arcgis/admin/generateToken'
                    , username=self.securityConfiguration['username']
                    , password=self.securityConfiguration['password'])
                    #, proxy_url=self.securityConfiguration['proxy_url']
                    #, proxy_port=self.securityConfiguration['proxy_port'])
            ags = arcrest.ags.server.Server(url=self.securityConfiguration['org_url'].replace('https','http') + ':6080/arcgis'
                    , securityHandler=sh)

            if sh.valid == False:
                print sh.message
            else:
                self.admin = ags
                self.token = sh.token

        else: # security type == Portal or ArcGIS
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
