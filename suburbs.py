import json
import requests
def getSuburbs():
    settings = json.load(open("settings.json"))
    url = "https://v0.postcodeapi.com.au/suburbs?name="+settings["suburb"]+"&postcode="+settings["postcode"]+"&state="+settings["state"]

    payload={}
    headers = {
    'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    suburb = response.json()
    if (len(suburb)!=1):
        print("Check Suburb data in Settings. Must include Suburb Name, Postcode and State (Abrv)")
        quit()

    latitude = suburb[0]["latitude"]
    longitude = suburb[0]["longitude"]
    radius = settings["radius"]*1000

    url = "https://v0.postcodeapi.com.au/radius?latitude="+str(latitude)+"&longitude="+str(longitude)+"&distance="+str(int(radius))

    payload={}
    headers = {
    'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    suburblist = response.json()
    s = []
    for suburb in suburblist:
        s.append(suburb["name"])
    return s