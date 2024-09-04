import json
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

import requests
from requests_ntlm import HttpNtlmAuth

# Sets logging level for logs coming out of requests library
# import logging
# logging.getLogger("requests").setLevel(logging.WARNING)

# This disables all warnings for urllib3 which maybe something that we do not want
# requests.packages.urllib3.disable_warnings() 
# So the following might be the more sensible approach; Disabled only the ones we do not want to see
disable_warnings(InsecureRequestWarning)

# Functions declaration

def save_credentials_to_file(username, password):
    credentials_json = json.dumps({
        'username': username,
        'password': password
    })

    with open('credentials.json', 'w') as out_file:
        out_file.write(credentials_json)


def load_credentials_from_file():
    with open('credentials.json', 'r') as in_file:
        credentials_json = json.load(in_file)
        return credentials_json

def call_api(credential):
    session = requests.Session()
    session.auth = HttpNtlmAuth(credential['username'], credential['password'])
    response = session.get('https://ah-1165446-001.corp.asdda.asd/service/api/notification/getnotification', verify=False)

    if (response.ok):
        json_data = response.json()
        #print(f'Result is {json_data}')
        print(f"Call is successful {response.status_code} ({response.reason})")
    else:
        print(f"Failed: Returned HTTP code is {response.status_code} ({response.reason})")

def call_post_checkout_api(credential, post_data_path):
    with open(post_data_path, 'r') as in_file:
        post_data = in_file.read()

    request_headers = {'Content-type': 'application/json'}
    session = requests.Session()
    session.auth = HttpNtlmAuth(credential['username'], credential['password'])
    response = session.post('https://ah-1165446-001.corp.asd.com//service/api/ShoppingCart/Checkout', headers=request_headers, data=post_data, verify=False)

    if (response.ok):
        json_data = response.json()
        #print(f'Result is {json_data}')
        print(f"Call is successful {response.status_code} ({response.reason})")
    else:
        print(f"Failed: Returned HTTP code is {response.status_code} ({response.reason})")


# Main script

if __name__ == "__main__":
    # save_credentials_to_file('CORP\\zkrs6a9', '<your-pwd')
    credentials = load_credentials_from_file()
    #call_get_notification_api(credentials)
    # with open('H:/notes/temp-json/merge-requests/ShoppingCartDTO-mix.json', 'r') as in_file:
    #     post_data = in_file.read()
    call_post_checkout_api(credentials, 'H:/notes/temp-json/merge-requests/ShoppingCartDTO-mix.json')
    

