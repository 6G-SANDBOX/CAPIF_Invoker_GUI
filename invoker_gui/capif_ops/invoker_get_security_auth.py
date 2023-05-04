from dis import dis
from email import charset
import requests
import json
import configparser
import redis
import os
from termcolor import colored


class InvokerGetSecurityAuth():

    def __get_security_token(self, capif_ip, api_invoker_id, jwt_token, ccf_url, aef_id, api_name, log_level):

    
        url = "https://{}/capif-security/v1/securities/{}/token".format(capif_ip, api_invoker_id)

        with open('capif_ops/config_files/token_request.json', "rb") as f:
            payload = json.load(f)

        payload["client_id"] = api_invoker_id
        payload["scope"] = "3gpp#"+aef_id+":"+api_name

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        
        payload_dict = json.dumps(payload, indent=2)

        print(colored(f"Request Body: {payload_dict}", "yellow"))

        try:

            if log_level == "debug":
                print(colored("''''''''''REQUEST'''''''''''''''''","blue"))
                print(colored(f"Request: to {url}","blue"))
                print(colored(f"Request Headers: {headers}", "blue"))
                print(colored(f"''''''''''REQUEST'''''''''''''''''", "blue"))

            response = requests.post(url, headers=headers, data=payload, cert=('capif_ops/certs/dummy.crt', 'capif_ops/certs/invoker_private_key.key'), verify='capif_ops/certs/ca.crt')
            print(response.request.body)
            response.raise_for_status()
            response_payload = json.loads(response.text)

            if log_level == "debug":
                print(colored("''''''''''RESPONSE'''''''''''''''''","green"))
                print(colored(f"Response to: {response.url}","green"))
                print(colored(f"Response Headers: {response.headers}","green"))
                print(colored(f"Response: {response.json()}","green"))
                print(colored(f"Response Status code: {response.status_code}","green"))
                print(colored("''''''''''RESPONSE'''''''''''''''''","green"))

            return response_payload
        except requests.exceptions.HTTPError as err:
            print(err.response.text)
            message = json.loads(err.response.text)
            status = err.response.status_code
            raise Exception(message, status)

    def execute_get_security_auth(self, log_level):

        with open('capif_ops/config_files/demo_values.json', 'r') as demo_file:
            demo_values = json.load(demo_file)

        config = configparser.ConfigParser()
        config.read('credentials.properties')

        capif_ip = os.getenv('CAPIF_HOSTNAME')
        invokerID = demo_values['invokerID']
        capif_access_token = demo_values['capif_access_token']
        ccf_discover_url = demo_values['ccf_discover_url']

        try:
            if 'aef_id_0' in demo_values and 'api_name_0' in demo_values:
                token = self.__get_security_token(capif_ip, invokerID, capif_access_token, ccf_discover_url, demo_values['aef_id_0'], demo_values['api_name_0'],log_level)
                print(colored(json.dumps(token, indent=2),"yellow"))
                demo_values["netapp_service_token"] = token["access_token"]
                print(colored("Obtained Security Token","yellow"))

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
