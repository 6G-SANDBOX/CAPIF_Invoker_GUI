from dis import dis
import requests
import json
import configparser
import os
from termcolor import colored


class RemoveInvoker():


    def __offboard_netapp_to_capif(self, capif_ip,  invoker_id, log_level):

        print(colored("Removing netapp from CAPIF","yellow"))
        url = 'https://{}/api-invoker-management/v1/onboardedInvokers/{}'.format(capif_ip, invoker_id)

        headers = {
            'Content-Type': 'application/json'
        }

        try:

            if log_level == "debug":
                print(colored("''''''''''REQUEST'''''''''''''''''","blue"))
                print(colored(f"Request: to {url}","blue"))
                print(colored(f"Request Headers: {headers}", "blue"))
                print(colored(f"''''''''''REQUEST'''''''''''''''''", "blue"))

            response = requests.request("DELETE", url, headers=headers, cert=(
                'capif_ops/certs/dummy.crt', 'capif_ops/certs/invoker_private_key.key'), verify='capif_ops/certs/ca.crt')
            response.raise_for_status()

            if log_level == "debug":
                print(colored("''''''''''RESPONSE'''''''''''''''''","green"))
                print(colored(f"Response to: {response.url}","green"))
                print(colored(f"Response Headers: {response.headers}","green"))
                print(colored(f"Response: {response.json()}","green"))
                print(colored(f"Response Status code: {response.status_code}","green"))
                print(colored("Success onboard invoker","green"))
                print(colored("''''''''''RESPONSE'''''''''''''''''","green"))

        except requests.exceptions.HTTPError as err:
            raise Exception(err.response.text, err.response.status_code)



    def execute_remove_invoker(self, log_level):


        capif_ip = os.getenv('CAPIF_HOSTNAME')

        with open('capif_ops/config_files/demo_values.json', 'r') as demo_file:
            demo_values = json.load(demo_file)

        try:

            self.__offboard_netapp_to_capif(capif_ip, demo_values["invokerID"], log_level)

            print("ApiInvokerID: {}\n".format(demo_values["invokerID"]))
            demo_values.pop("invokerID")
            demo_values.pop("pub_key")
            with open('capif_ops/config_files/demo_values.json', 'w') as outfile:
                json.dump(demo_values, outfile)

        except Exception as e:
            status_code = e.args[0]
            if status_code == 403:
                print("Invoker already registered.")
                print("Chanage invoker public key in invoker_details.json\n")
            else:
                print(e)
