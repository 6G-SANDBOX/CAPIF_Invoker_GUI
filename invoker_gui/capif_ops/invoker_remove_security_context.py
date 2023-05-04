from dis import dis
from email import charset
import requests
import json
import configparser
import redis
import os
from termcolor import colored


class InvokerRemoveSecurityContext():

    def __remove_security_service(self, capif_ip, api_invoker_id, jwt_token, ccf_url, demo_values, log_level):


        url = "https://{}/capif-security/v1/trustedInvokers/{}".format(capif_ip, api_invoker_id)

        headers = {
            'Content-Type': 'application/json'
        }

        try:

            if log_level == "debug":
                print(colored("''''''''''REQUEST'''''''''''''''''","blue"))
                print(colored(f"Request: to {url}","blue"))
                print(colored(f"Request Headers: {headers}", "blue"))
                print(colored(f"''''''''''REQUEST'''''''''''''''''", "blue"))

            response = requests.delete(url, cert=('capif_ops/certs/dummy.crt', 'capif_ops/certs/invoker_private_key.key'), verify='capif_ops/certs/ca.crt')
            response.raise_for_status()

            if log_level == "debug":
                print(colored("''''''''''RESPONSE'''''''''''''''''","green"))
                print(colored(f"Response to: {response.url}","green"))
                print(colored(f"Response Headers: {response.headers}","green"))
                print(colored(f"Response: {response.json()}","green"))
                print(colored(f"Response Status code: {response.status_code}","green"))
                print(colored("''''''''''RESPONSE'''''''''''''''''","green"))

            return 
        except requests.exceptions.HTTPError as err:
            print(err.response.text)
            message = json.loads(err.response.text)
            status = err.response.status_code
            raise Exception(message, status)

    def execute_remove_security_context(self, log_level):

        with open('capif_ops/config_files/demo_values.json', 'r') as demo_file:
            demo_values = json.load(demo_file)

        config = configparser.ConfigParser()
        config.read('credentials.properties')

        capif_ip = os.getenv('CAPIF_HOSTNAME')
        invokerID = ""
        capif_access_token = ""
        ccf_discover_url = ""

        try:

            invokerID = demo_values['invokerID']
            capif_access_token = demo_values['capif_access_token']
            ccf_discover_url = demo_values['ccf_discover_url']
            security_information = self.__remove_security_service(capif_ip, invokerID, capif_access_token, ccf_discover_url, demo_values,log_level)
            print(colored(json.dumps(security_information, indent=2),"yellow"))
            print(colored("Register Security context","yellow"))

            with open('capif_ops/config_files/demo_values.json', 'w') as outfile:
                json.dump(demo_values, outfile)


        except Exception as e:
            status_code = e.args[0]
            if status_code == 401:
                print("API Invoker is not authorized")
            elif status_code == 403:
                print("API Invoker does not exist. API Invoker id not found")
            else:
                print(e)

