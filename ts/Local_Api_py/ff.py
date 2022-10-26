import json

file_current = __file__[:-5]

f = open(rf'{file_current}Riot_Auth.json')
j = json.load(f)
    
print(j["Riot_Auth"][0]["Time"])