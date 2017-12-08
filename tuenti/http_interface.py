from .constants import Constants
from .utils import Utils
from .exceptions.tuenti_exception import TuentiException
import requests
import json

class HttpInterface:
    """
    HttpInterface class.

    This class contains all functions related to headers,
    preparing data and sending requests.
    """

    def __init__(self, tuenti, debug = False):
        """ Constructor.

        Args:
            tuenti: Instance of TuentiAPI class.
            debug:  Show requests and responses in CLI (Optional, default False).

        """
        self.tuenti = tuenti
        self.debug = debug
        self.authToken = Utils.check_if_auth_token_exists_and_return(self.tuenti)

    def send_request(self, url, payload):
        """ Sends a request.

        Args:
            url:        URL we use to do the request.
            payload:    Data sent to Tuenti.

        Return:
            List/Dict.

        """

        headers = self.get_headers(url)
        payload = json.dumps(payload)

        response = requests.post(url, data=payload, headers=headers)

        if self.debug is True:
            Utils.printDebug(url, payload, response.text)
            print("\n")

        ##
        # HTTP CODE 401 = token_invalid. Tuenti internal error 101.
        # HTTP CODE 401 = session_invalid. Tuenti internal error 301.
        # HTTP CODE 409 = must-revalidate. Tuenti internal error 201.
        if response.status_code != 200 and response.status_code != 401 and response.status_code != 409:
            raise TuentiException('Request failed. Got {0} http code.'.format(response.status_code))
            return
        elif response.status_code == 401 or response.status_code == 409:
            raise TuentiException('Login required. Got {0} http code.'.format(response.status_code))
            return

        if url == Constants.LOGIN_URL:
            if self.authToken != False:
                sessionToken = response.headers["X-Tuenti-Authorization"].replace("sess-token=", "")
            else:
                sessionHeader = response.headers["X-Tuenti-Authorization"].split(",")
                sessionToken = sessionHeader[0].replace("sess-token=", "")
                self.authToken = sessionHeader[1].replace("auth-token=", "")
            Utils.save_session(self.tuenti, sessionToken, self.authToken)

        return response.json

    def get_headers(self, url):
        """ Get headers.

        Args:
            url: URL we use to do the request.

        Return:
            Dict.

        """

        headers = {
            "User-Agent": Constants.USER_AGENT,
            "Content-Type": Constants.CONTENT_TYPE,
            "Accept-Language": Constants.ACCEPT_LANGUAGE,
            "Connection": Constants.CONNECTION,
            "Accept": Constants.ACCEPT,
            "Accept-Encoding": Constants.ACCEPT_ENCODING,
        }

        sessionToken = Utils.check_if_session_token_exists_and_return(self.tuenti)
        if url == Constants.LOGIN_URL:
            if self.authToken == False:
                headers["X-Tuenti-Authentication"] = Utils.build_auth_string(self.tuenti)
            else:
                headers["X-Tuenti-Authentication"] = Utils.build_auth_string(self.tuenti, self.authToken)
        else:
            if sessionToken != False or sessionToken != "":
                headers["X-Tuenti-Authorization"] = "sess-token="+sessionToken
            else:
                raise TuentiException("Login required.")

        return headers

    def encapsulate_request(self, requests):
        """ Encapsulates the request along with other information.

        Args:
            requests: List of requests

        Return:
            Dict.

        """
        data = {
                    "version": Constants.VERSION,
                    "requests": requests,
                    "screen": Constants.SCREEN
                }
        return data
