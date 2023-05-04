from dis import dis
import requests
import json
import configparser
import redis
import os
from termcolor import colored


from OpenSSL.SSL import FILETYPE_PEM
from OpenSSL.crypto import (dump_certificate_request, dump_privatekey, load_publickey, PKey, TYPE_RSA, X509Req, dump_publickey)


class RegisterInvoker():
    def __create_csr(self,  name):

        # create public/private key
        key = PKey()
        key.generate_key(TYPE_RSA, 2048)

        # Generate CSR
        req = X509Req()
        req.get_subject().CN = name
        req.get_subject().O = 'Telefonica I+D'
        req.get_subject().OU = 'Innovation'
        req.get_subject().L = 'Madrid'
        req.get_subject().ST = 'Madrid'
        req.get_subject().C = 'ES'
        req.get_subject().emailAddress = 'inno@tid.es'
        req.set_pubkey(key)
        req.sign(key, 'sha256')

        csr_request = dump_certificate_request(FILETYPE_PEM, req)

        private_key = dump_privatekey(FILETYPE_PEM, key)

        return csr_request, private_key




    def __onboard_netapp_to_capif(self, capif_ip, capif_callback_ip, capif_callback_port, jwt_token, ccf_url, log_level):

        print(colored("Onboarding netapp to CAPIF","yellow"))
        url = 'https://{}/{}'.format(capif_ip, ccf_url)

        with open('capif_ops/config_files/demo_values.json', 'r') as demo_file:
            demo_values = json.load(demo_file)

        csr_request, private_key = self.__create_csr("invoker")

        if 'pub_key' not in demo_values:
            private_key_file = open("capif_ops/certs/invoker_private_key.key", 'wb+')
            private_key_file.write(bytes(private_key))

        json_file = open('capif_ops/config_files/invoker_details.json', 'rb')
        payload_dict = json.load(json_file)
        if 'pub_key' not in demo_values:
            payload_dict['onboardingInformation']['apiInvokerPublicKey'] = csr_request.decode("utf-8")
        else:
            payload_dict['onboardingInformation']['apiInvokerPublicKey'] = demo_values['pub_key']
        payload_dict['notificationDestination'] = payload_dict['notificationDestination'].replace("X", capif_callback_ip)
        payload_dict['notificationDestination'] = payload_dict['notificationDestination'].replace("Y", capif_callback_port)
        payload = json.dumps(payload_dict, indent=2)

        print(colored(f"Request Body: {payload}", "yellow"))

        headers = {
            'Authorization': 'Bearer {}'.format(jwt_token),
            'Content-Type': 'application/json'
        }

        try:

            if log_level == "debug":
                print(colored("''''''''''REQUEST'''''''''''''''''","blue"))
                print(colored(f"Request: to {url}","blue"))
                print(colored(f"Request Headers: {headers}", "blue"))
                print(colored(f"Request Body: {json.dumps(payload)}", "blue"))
                print(colored(f"''''''''''REQUEST'''''''''''''''''", "blue"))

            response = requests.request("POST", url, headers=headers, data=payload, verify='capif_ops/certs/ca.crt')
            response.raise_for_status()
            response_payload = json.loads(response.text)
            certification_file = open('capif_ops/certs/dummy.crt', 'wb')
            certification_file.write(bytes(response_payload['onboardingInformation']['apiInvokerCertificate'], 'utf-8'))
            certification_file.close()

            if log_level == "debug":
                print(colored("''''''''''RESPONSE'''''''''''''''''","green"))
                print(colored(f"Response to: {response.url}","green"))
                print(colored(f"Response Headers: {response.headers}","green"))
                print(colored(f"Response: {response.json()}","green"))
                print(colored(f"Response Status code: {response.status_code}","green"))
                print(colored("Success onboard invoker","green"))
                print(colored("''''''''''RESPONSE'''''''''''''''''","green"))
            return response_payload['apiInvokerId'],  payload_dict['onboardingInformation']['apiInvokerPublicKey']
        except requests.exceptions.HTTPError as err:
            raise Exception(err.response.text, err.response.status_code)





    def execute_register_invoker(self, log_level):

        config = configparser.ConfigParser()
        config.read('capif_ops/config_files/credentials.properties')

        capif_ip = os.getenv('CAPIF_HOSTNAME')

        capif_callback_ip = config.get("credentials", "capif_callback_ip")
        capif_callback_port = config.get("credentials", "capif_callback_port")

        with open('capif_ops/config_files/demo_values.json', 'r') as demo_file:
            demo_values = json.load(demo_file)

        try:
            capif_access_token = demo_values['capif_access_token']
            ccf_onboarding_url = demo_values['ccf_onboarding_url']
            invokerID, pub_key = self.__onboard_netapp_to_capif(capif_ip, capif_callback_ip, capif_callback_port, capif_access_token, ccf_onboarding_url, log_level)
            demo_values['invokerID'] = invokerID
            demo_values['pub_key'] = pub_key
            print("ApiInvokerID: {}\n".format(invokerID))
            with open('capif_ops/config_files/demo_values.json', 'w') as outfile:
                json.dump(demo_values, outfile)

        except Exception as e:
            status_code = e.args[0]
            if status_code == 403:
                print("Invoker already registered.")
                print("Chanage invoker public key in invoker_details.json\n")
            else:
                print(e)
