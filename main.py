#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests, sys, re, json

def getlok(unit):                               #Make konzern-apps request (stopps/drivebys)
    url = f'https://konzern-apps.web.oebb.at/lok/index/{unit}/'
    r = requests.get(url)
    return(r.text)

print("-"*30)
print("Welcome to lokfinder-cli!")
print("-"*30)

if((re.match("-[AB][st]$", sys.argv[1]) and len(sys.argv) == 3) or (re.match("-h$|--help$", sys.argv[1]) and len(sys.argv) == 2)):
    print("Valid Command")
else:
    print("Command not valid")
    print('Exiting...')
    exit()

print("-"*30)

if(re.match("-h$|--help$", sys.argv[1]) and len(sys.argv) == 2):                          #Help menu
    print("Displaying help-menu")
    print("  -h               Show help-menu")
    print("  -A               All Trains")
    print("  -B               Branding Trains")
    print("  -s <station>     Search for trains by station")
    print("  -t <unit-nmb>    Search for trains by unit number")

if(re.match("-B", sys.argv[1]) and len(sys.argv) == 3):
    url = 'https://lokfinder.oebb.at/'              #For getting trainids
    print('GET:',url)
    r = requests.get(url)
    msoup = BeautifulSoup(r.text, 'html.parser')    #Main soup

    if(str(r.status_code)=='200'):                       #Test for 200 answer
        print('Returned:', r.status_code, "OK")
    else:
        print('Statuscode not 200!')
        print('Exiting...')
        exit()
    print("-"*30)

    a = msoup.find_all('oebb-lokfinder-lok')

    print("Getting stopps for every train")
    hits = []
    for x, y in enumerate(a):
        response = getlok(y.get('unit-number'))
        jsondata = json.loads(response)
        for stop in jsondata:
            if(str(sys.argv[2]) in stop["name"]):
                hits.append(str(y.get("label")) + "|" + str(stop["arrival"]) + "|" + stop["departure"])
        print(f"{x+1}/{len(a)}", y.get('label'), end="\r")
    print("\n")
    print("-"*30)

    for k in hits:
        print(k)



#1116.0012

