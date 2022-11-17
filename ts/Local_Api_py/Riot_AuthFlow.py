import asyncio
import sys
import json
import riot_auth
import time
import ssl

file_current = __file__[:-16]

def Auth_Riot():
    f = open(rf'{file_current}Riot_Auth.json')
    j = json.load(f)
    
    if time.time() - float(j["Riot_Auth"][0]["Time"]) > 3600:
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # endregion
    
        CREDS = "Lvl23Crook", "amanaman13"

        auth = riot_auth.RiotAuth()
        try:
            asyncio.run(auth.authorize(*CREDS))
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
            pass
        else:
    # Handle target environment that doesn't support HTTPS verification
            ssl._create_default_https_context = _create_unverified_https_context
    
        data = {'Riot_Auth':[{'Acess_Token': f'{auth.access_token}', 'Entitlment_token': f'{auth.entitlements_token}','PUUID':f'{auth.user_id}','Time':f'{time.time()}'}]} 
        with open(f'{file_current}Riot_Auth.json', 'w') as outfile:
            json.dump(data, outfile,indent=4)
    
   
 
        print(f"Access Token Type: {auth.token_type}\n")
        print(f"Access Token: {auth.access_token}\n")
        print(f"Entitlements Token: {auth.entitlements_token}\n")
        print(f"User ID: {auth.user_id}")

# Reauth using cookies. Returns a bool indicating whether the reauth attempt was successful.
        asyncio.run(auth.reauthorize())

    else:
        print("Acess token hasn't expired yet")

    ## add timer with expiration n shit man, on json
    

Auth_Riot()