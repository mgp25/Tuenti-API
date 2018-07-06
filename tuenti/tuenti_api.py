from .constants import Constants
from .utils import Utils
from .http_interface import HttpInterface
import os

class TuentiAPI:
    """
    TuentiAPI class.

    This class contains all requests that can be done.
    """

    def __init__(self, user, password, installationId, appsFlyersKey = None, dataFolder = None, debug = False):
        """ Constructor.

        Args:
            user:           Your mobile phone number with country code.
            password:       The password of your account.
            installationId: Installation ID. Captured from Tuenti requests.
            appsFlyersKey:  Apps Flyers Key for stastistics (Optional, default None).
            dataFolder:     Path to save session data (Optional, default None. Uses already created `session` folder).
            debug:          Show requests and responses in CLI (Optional, default False).

        """
        self.user = user
        self.password = password
        self.installationId = installationId
        self.appsFlyersKey = appsFlyersKey

        if dataFolder == None:
            self.dataFolder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'session'))
        else:
            self.dataFolder = dataFolder
        self.http = HttpInterface(self, debug)

    def set_auth_token(self, authToken):
        """ Set your own captured auth token.

        Args:
            authToken: Auth token. Used to refresh session token.

        """
        Utils.save_session(self, "", authToken)

    def login(self):
        """ Authenticates to Tuenti.

        Return:
            List/Dict.
        """
        url = Constants.LOGIN_URL
        requests = [
                        [
                            "Auth_getSessionInfo",
                            {
                                "appsFlyerKey": self.appsFlyersKey,
                                "osVersion": Constants.OS_VERSION,
                                "deviceName": Constants.DEVICE_NAME,
                                "os": Constants.OS,
                                "model": Constants.MODEL,
                                "manufacturer": Constants.MANUFACTURER,
                                "installationId": self.installationId,
                                "refreshExternalSession": False
                            }
                        ],
                ]

        return self.http.send_request(url, self.http.encapsulate_request(requests))

    def get_user_data(self):
        """ Get account data.

        Return:
            List/Dict.
        """
        url = Constants.TUENTI_URL
        requests = [
                        [
                            "User_getUsersData",
                            {
                            }
                        ],
                    ]

        return self.http.send_request(url, self.http.encapsulate_request(requests))

    def getBalance(self):
        """ Get account balance.

        Return:
            List/Dict.
        """
        url = Constants.TUENTI_URL
        requests = [
                        [
                            "AccountDashboard_getAccountDashboard",
                            {
                                "forceUpdate": False,
                                "fragments":
                                    ["balance","unbilledConsumption","overallConsumption","subscriptionBundles","tariff","operations","billing","upgrades","tariffName","previousUsageSection","devicePlan"]
                            }
                        ],
                    ]

        return self.http.send_request(url, self.http.encapsulate_request(requests))

    def get_sync_info(self):
        """ Get contact sync information and settings.

        Return:
            List/Dict.

        """
        url = Constants.TUENTI_URL
        requests = [
                    [
                        "Cloudcontacts_getSyncInfo",
                        {
                            "installationId": self.installationId,
                        }
                    ],
                ]

        return self.http.send_request(url, self.http.encapsulate_request(requests))

    def get_synced_contacts(self):
        """ Get synced contacts.

        Return:
            List/Dict.

        """
        url = Constants.TUENTI_URL
        requests = [
                        [
                            "Cloudcontacts_getCloudContactsChanges",
                            {
                                "discardNonUsers": False,
                                "installationId": self.installationId,
                                "includeLuid": True
                            }
                        ],
                    ]

        return self.http.send_request(url, self.http.encapsulate_request(requests))

    def get_voip_config(self):
        """ Get VOIP configuration to establish a connection.

        Return:
            List/Dict.

        """
        url = Constants.TUENTI_URL
        requests = [
                        [
                            "Voip_getVoipConfig",
                            {
                                "capability_version": 1,
                                "installationId": self.installationId
                            }
                        ],
                    ]

        return self.http.send_request(url, self.http.encapsulate_request(requests))

    def get_voip_flags(self):
        """ Shows the minimum required network to do VOIP calls (Default 3G).

        Return:
            List/Dict.

        """
        url = Constants.TUENTI_URL
        requests = [
                        [
                            "Voip_voipFlags",
                            {
                            "flags":{
                                "list":[
                                    "bridgingCalls",
                                    "app2appCalls",
                                    "gsmCalls",
                                    "callRating",
                                    "callFilters",
                                    "callSaving",
                                    "network"
                                ]
                            },
                        "installationId": self.installationId,
                        "capability_version": 1
                     }
                  ]
               ]

        return self.http.send_request(url, self.http.encapsulate_request(requests))

    def get_conversations_latest_activity(self):
        """ Get conversations latest activity.

        Return:
            List/Dict.

        """
        url = Constants.TUENTI_URL
        requests = [
                        [
                            "Chat_getConversationsLatestActivity",
                            {
                                "addExtendedConversationData": True
                            }
                        ]
                    ]

        return self.http.send_request(url, self.http.encapsulate_request(requests))

    def get_chat_groups(self):
        """ Get chat groups.

        Return:
            List/Dict.

        """
        url = Constants.TUENTI_URL
        requests = [
                        [
                            "Chat_getGroups",
                            {
                            }
                        ]
                    ]

        return self.http.send_request(url, self.http.encapsulate_request(requests))

    def get_if_new_update_available(self):
        """ Get if there is a new app version available.

        Return:
            List/Dict.

        """
        url = Constants.TUENTI_URL
        requests = [
                        [
                            "Appupdate_checkUpdate",
                            {
                                "installationId": self.installationId,
                                "version": Constants.APP_VERSION
                            }
                        ]
                    ]

        return self.http.send_request(url, self.http.encapsulate_request(requests))

    def get_default_encoding_valid_chars(self):
        """ Get default encoding valid chars.

        Return:
            List/Dict.

        """
        url = Constants.TUENTI_URL
        requests = [
                        [
                            "Shortmessage_getDefaultEncodingValidChars",
                            {
                            }
                        ]
                    ]

        return self.http.send_request(url, self.http.encapsulate_request(requests))
