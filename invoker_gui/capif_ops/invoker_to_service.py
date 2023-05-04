from dis import dis
import requests
import json
import configparser
import redis
import os
import argparse
from termcolor import colored

# Get environment variables


class InvokerToService():
    def __demo_to_aef(self, demo_ip, demo_port, demo_url, jwt_token, name, log_level):

        print(colored("Using AEF Service API","yellow"))
        url = "http://{}:{}{}".format(demo_ip, demo_port, demo_url)
        #url = "http://python_aef:8086/hello"


        json_file = open('capif_ops/config_files/service_request_body.json', 'rb')
        payload_dict = json.load(json_file)
        payload = json.dumps(payload_dict, indent=2)

        files = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+jwt_token
        }

        print(colored(f"Request Body: {payload}", "yellow"))

        try:
            if log_level == "debug":
                print(colored("''''''''''REQUEST'''''''''''''''''","blue"))
                print(colored(f"Request: to {url}","blue"))
                print(colored(f"Request Headers: {headers}", "blue"))
                print(colored(f"Request Body: {json.dumps(payload, indent=2)}", "blue"))
                print(colored(f"''''''''''REQUEST'''''''''''''''''", "blue"))
            response = requests.request("POST", url, headers=headers, data=payload, files=files, cert=('capif_ops/certs/dummy.crt', 'capif_ops/certs/invoker_private_key.key'), verify=False)
            response.raise_for_status()
            response_payload = json.loads(response.text)

            if log_level == "debug":
                print(colored("''''''''''RESPONSE'''''''''''''''''","green"))
                print(colored(f"Response to: {response.url}","green"))
                print(colored(f"Response Headers: {response.headers}","green"))
                print(colored(f"Response: {response.json()}","green"))
                print(colored(f"Response Status code: {response.status_code}","green"))
                print(colored("Success to invoke service","green"))
                print(colored(response_payload,"green"))
                print(colored("''''''''''RESPONSE'''''''''''''''''","green"))
            return response_payload
        except requests.exceptions.HTTPError as err:
            print(err.response.text)
            message = json.loads(err.response.text)
            status = err.response.status_code
            raise Exception(message, status)


    def execute_invoker_to_service(self, log_level):

        # parser = argparse.ArgumentParser()
        # parser.add_argument('--name', metavar= "name", type=str, default="Evolve5G", help="Name to send to the aef service")
        # args = parser.parse_args()
        input_name = "prueba"

        with open('capif_ops/config_files/demo_values.json', 'r') as demo_file:
            demo_values = json.load(demo_file)

        try:
            if 'netapp_service_token' in demo_values:

                print(colored("Doing test","yellow"))
                jwt_token = demo_values['netapp_service_token']
                invokerID = demo_values['invokerID']
                demo_ip = demo_values['demo_ipv4_addr_0']
                demo_port = demo_values['demo_port_0']
                demo_url = demo_values['demo_url_0']
                result = self.__demo_to_aef(demo_ip, demo_port, demo_url, jwt_token, input_name, log_level)
                print(colored(f"Response: {json.dumps(result, indent=2)}", "yellow"))
                print(colored("Success","yellow"))
        except Exception as e:
            status_code = e.args[0]
            if status_code == 401:
                print("API Invoker is not authorized")
            elif status_code == 403:
                print("API Invoker does not exist. API Invoker id not found")
            else:
                print(e)