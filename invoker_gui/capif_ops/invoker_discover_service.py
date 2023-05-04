from dis import dis
import requests
import json
import configparser
import redis
import os
from termcolor import colored


class DiscoverService():

    def __discover_service_apis(self, capif_ip, api_invoker_id, jwt_token, ccf_url, log_level):

        print(colored("Discover Service", "yellow"))
        url = "https://{}/{}{}".format(capif_ip, ccf_url, api_invoker_id)

        payload = {}
        files = {}
        headers = {
            'Content-Type': 'application/json'
        }

        try:

            if log_level == "debug":
                print(colored("''''''''''REQUEST'''''''''''''''''", "blue"))
                print(colored(f"Request: to {url}", "blue"))
                print(colored(f"Request Headers: {headers}", "blue"))
                print(colored(f"''''''''''REQUEST'''''''''''''''''", "blue"))

            response = requests.request("GET", url, headers=headers, data=payload, files=files, cert=(
                'capif_ops/certs/dummy.crt', 'capif_ops/certs/invoker_private_key.key'), verify='capif_ops/certs/ca.crt')
            response.raise_for_status()
            response_payload = json.loads(response.text)

            if log_level == "debug":
                print(colored("''''''''''RESPONSE'''''''''''''''''", "green"))
                print(colored(f"Response to: {response.url}", "green"))
                print(colored(f"Response Headers: {response.headers}", "green"))
                print(colored(f"Response: {response.json()}", "green"))
                print(
                    colored(f"Response Status code: {response.status_code}", "green"))
                print(colored("''''''''''RESPONSE'''''''''''''''''", "green"))

            return response_payload
        except requests.exceptions.HTTPError as err:
            print(err.response.text)
            message = json.loads(err.response.text)
            status = err.response.status_code
            raise Exception(message, status)

    def execute_discover_service(self, log_level):


        with open('capif_ops/config_files/demo_values.json', 'r') as demo_file:
            demo_values = json.load(demo_file)

        capif_ip = os.getenv('CAPIF_HOSTNAME')

        try:
            if 'invokerID' in demo_values:
                invokerID = demo_values['invokerID']
                capif_access_token = demo_values['capif_access_token']
                ccf_discover_url = demo_values['ccf_discover_url']
                discovered_apis = self.__discover_service_apis(
                    capif_ip, invokerID, capif_access_token, ccf_discover_url, log_level)
                print(colored(json.dumps(discovered_apis, indent=2), "yellow"))

                count = 0
                api_list = discovered_apis["serviceAPIDescriptions"]
                for api in api_list:
                    getAEF_profiles = api["aefProfiles"][0]
                    getAEF_interfaces = getAEF_profiles["interfaceDescriptions"][0]
                    getAEF_versions = getAEF_profiles["versions"][0]
                    getAEF_resources = getAEF_versions["resources"][0]
                    demo_values[f'api_id_{count}'] = api["apiId"]
                    demo_values[f'api_name_{count}'] = api["apiName"]
                    demo_values[f'aef_id_{count}'] = getAEF_profiles["aefId"]
                    demo_values[f'demo_ipv4_addr_{count}'] = getAEF_interfaces["ipv4Addr"]
                    demo_values[f'demo_port_{count}'] = getAEF_interfaces["port"]
                    demo_values[f'demo_url_{count}'] = getAEF_resources['uri']
                    count += 1

                print(colored("Discovered APIs", "yellow"))
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

