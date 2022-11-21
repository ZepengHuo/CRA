
# ---------------------------------------------------------
# Initialization
# ---------------------------------------------------------

import e3db
import json
import requests

# Required to generate random client id 
import os
import binascii
from datetime import datetime


def register_user():
    # A registration token is required to set up a client. If no 
    # registration token is known/available then register at
    # www.innovault.io and save your credentials.json to
    # the same directory as this script.
    print ("The system you are accessing may contain CUI.  Unauthorized or misuse of the data is prohibited.")


    token = "05cf11de8c8fa20dfa714ebec7c7b80119e1df80d5e8f893ff6ff80d453363fb" 
    uniqueClient = ""
    baseurl = "https://wash.fedramp.tozny.com/api/registerclient?verification=8f39804b-7cdc-468d-95dc-673960679036" 

    print ("Using Registration Token: {0}".format(token))

    public_key, private_key = e3db.Client.generate_keypair()



    # Clients must be registered with a name unique to your account 
    client_name = "client_{0}".format(binascii.hexlify(os.urandom(16)))





    #
    # Client credentials are not backed up by default.
    #
    # client_info = e3db.Client.register(token, client_name, public_key, private_key=private_key, backup=True)

    client_info = e3db.Client.register(token, client_name, public_key, api_url = "https://api.fedramp.e3db.com")

    api_key_id = client_info.api_key_id
    api_secret = client_info.api_secret
    client_id = client_info.client_id
    r = requests.post(baseurl, data={'client_id' : client_id})
    print (r.content)
    print ("Your client ID has been sent for approval.")
    print ("Your client id is {0}".format(client_id))
    print ("Do not lose, share, or send the generated credentials.json created in the directory.")
    print ("The system you are accessing may contain CUI.  Unauthorized or misuse of the data is prohibited.")




    # ---------------------------------------------------------
    # Usage
    # ---------------------------------------------------------

    # Once the client is registered, you can use it immediately to create the
    # configuration used to instantiate a Client that can communicate with
    # e3db directly.

    creds = {
        "version": 1,
        "api_url": "https://api.fedramp.e3db.com",
        "api_key_id": client_info.api_key_id,
        "api_secret": format(api_secret),
        "client_id": format(client_id),
        "client_email": "",
        "public_key": public_key,
        "private_key": private_key
    }
    with open('credentials.json','w') as outfile:
        json.dump(creds, outfile)

# If a credentials file exists, use it
# else try and register a client for the user
if os.path.exists("credentials.json"): 
    # user has already created the credentials.  Do not create another set.
    print ("Your credentials are already established.")
    print ("The program data administrator will need to authorize your account for data access.")
    print ("For query support please visit the WASH Data Portal") 

else:
    register_user()



  