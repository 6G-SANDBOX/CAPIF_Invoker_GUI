import requests
import json
import configparser
import os
from termcolor import colored

class PreviousAuth():

    def __get_capif_auth(self, register_ip, register_port, username, password):

            #print("Geting Auth to exposer")
            #url = "https://register:8084/getauth".format(capif_port)
            url = "https://{}:{}/getauth".format(register_ip, register_port)

            payload = dict()
            payload['username'] = username
            payload['password'] = password

            headers = {
                'Content-Type': 'application/json'
            }

            try:
                response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False)

                response.raise_for_status()
                response_payload = json.loads(response.text)

                return response_payload['access_token']

            except requests.exceptions.HTTPError as err:
                raise Exception(err.response.text, err.response.status_code)


    def execute_get_auth(self, log_level):

        config = configparser.ConfigParser()
        config.read('capif_ops/config_files/credentials.properties')

        username = config.get("credentials", "invoker_username")
        password = config.get("credentials", "invoker_password")

        register_ip = os.getenv('REGISTER_HOSTNAME')
        register_port = os.getenv('REGISTER_PORT')

        if os.path.exists("capif_ops/config_files/demo_values.json"):
            #os.remove("capif_ops/config_files/demo_values.json")
            with open('capif_ops/config_files/demo_values.json', 'r') as demo_file:
                demo_values = json.load(demo_file)
        else:
            demo_values = {}

        #First we need register exposer in CAPIF
        try:
            if 'netappID' in demo_values:
                access_token = self.__get_capif_auth(register_ip, register_port, username, password)
                demo_values['capif_access_token'] = access_token

            with open('capif_ops/config_files/demo_values.json', 'w') as outfile:
                json.dump(demo_values, outfile)

            print("Invoker auth Success!")
        except Exception as e:
            status_code = e.args[0]
            if status_code == 409:
                print("User already registed. Continue with token request\n")
            else:
                print(e)

        return True
