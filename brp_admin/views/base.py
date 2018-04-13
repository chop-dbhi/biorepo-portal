import requests
import os
import logging

log = logging.getLogger(__name__)


class JenkinsJob(object):
    #########################################################################
    # This object is used to interact with Jenkins through the jenkins API.
    # this object needs a url and parameters(optional)
    # url: must start with '@' character and be the address of the job. This can
    #      be found in the jenkins configuration under 'build triggers' where
    #      'trigger builds remotely' is checked.
    # Parameters: is optional, only use if required for job. should be a dictionary
    # format.
    #########################################################################
    def __init__(self, url, parameters={}):

        self.job_url = url
        self.querystring = parameters

        self.headers = {
            'Cache-Control': "no-cache",
        }

    def __get_credentials(self):

        name = os.environ.get('jenkins_id')
        token = os.environ.get('jenkins_token')

        # if jenkins id or jenkins token is not found, generate an exception.
        if (name is None or token is None):
            log.debug("Jenkins Credentials do not exist.")
            raise Exception("Jenkins_Credentials_DNE")
        else:
            return name + ":" + token

    def trigger_jenkins_job(self):
        try:
            credentials = self.__get_credentials()
            self.url = "https://" + credentials + self.job_url
            response = requests.request("POST", self.url, headers=self.headers, params=self.querystring)
            return response
        except:
            return {'error': 'Jenkins Credentials do not exist'}
