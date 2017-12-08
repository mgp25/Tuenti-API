import os
import pickle
import hashlib
from .constants import Constants

class Utils:
    """
    Utils class.

    This class contains all helpful functions.
    """

    def check_if_session_token_exists_and_return(tuenti):
        """ Checks if session token exists and return if so.

        Args:
            tuenti: Instance of TuentiAPI class.

        Return:
            False/string.

        """
        if os.path.exists(tuenti.dataFolder+"/session.dat"):
            try:
                sessionToken = pickle.load(open(tuenti.dataFolder+"/session.dat", "rb"))["sess-token"]
                return sessionToken
            except KeyError as e:
                return False
        else:
            return False

    def check_if_auth_token_exists_and_return(tuenti):
        """ Checks if auth token exists and return if so.

        Args:
            tuenti: Instance of TuentiAPI class.

        Return:
            False/string.

        """
        if os.path.exists(tuenti.dataFolder+"/session.dat"):
            try:
                authToken = pickle.load(open(tuenti.dataFolder+"/session.dat", "rb"))["auth-token"]
                return authToken
            except KeyError as e:
                return False
        else:
            return False

    def save_session(tuenti, sessionToken, authToken):
        """ Saves authToken and sessionToken in a file.

        Args:
            tuenti:         Instance of TuentiAPI class.
            sessionToken:   Session token.
            authToken:      Auth token.

        """
        sessionData = {
            'sess-token': sessionToken,
            'auth-token': authToken
        }
        pickle.dump(sessionData, open(tuenti.dataFolder+"/session.dat", "wb"))


    def build_auth_string(tuenti, authToken = None):
        """ Builds authentication string for login procedure.

        Args:
            tuenti:     Instance of TuentiAPI class.
            authToken:  Auth token.

        Return:
            String.

        """
        if authToken == None:
            password = hashlib.md5(bytes(tuenti.password, encoding='utf-8')).hexdigest()
            return "user="+tuenti.user+",password="+password+",installation-id="+tuenti.installationId+",device-family="+Constants.DEVICE_FAMILY
        else:
            return "user="+tuenti.user+",auth-token="+authToken+",installation-id="+tuenti.installationId+",device-family="+Constants.DEVICE_FAMILY

    def printDebug(url, payload, response):
        """ Prints request and response.

        Args:
            url:        URL we use to do the request.
            payload:    Data sent to Tuenti.
            response:   Tuenti's response.

        """
        print('\033[95m POST: \033[0m {0}'.format(url))
        print('\033[93m DATA: \033[0m {0}'.format(payload))
        print('\033[94m RESPONSE: \033[0m {0}'.format(response))
