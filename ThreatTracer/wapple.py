import sys
from Wappalyzer import Wappalyzer, WebPage
import requests
from colorama import Fore, Back, Style
import warnings
import json

adata = {}

def find_version(a):
    if a == []:
        return 'nil'
    else:
        return a[0]
    
def find_techs(url):
    if '.' in url and 'http' not in url:
        t = 'http://'+url
        try:
            url = requests.head(t,allow_redirects=True).url
            print("Resolving "+url)
        except:
            print("Resolving error "+url)
            return
    try:
        webpage = WebPage.new_from_url(url)
        wappalyzer = Wappalyzer.latest()
        techs = wappalyzer.analyze_with_versions_and_categories(webpage)
    except:
        return "ERROR"+url
    
    nurl = url.split("//")[1].rstrip("/")

    data = []
    for i in techs:
        if find_version(techs[i]['versions']) != 'nil' or True:
            tech_info = {
                "category":techs[i]['categories'][0],
                "identifier":i,
                "version":find_version(techs[i]['versions'])
            }
            data.append(tech_info)
    return data

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Path to your JSON file
filename = "/home/kali/ost/output/"+sys.argv[1]+"/httpx_toolkit_status_title.txt"
data = []
wappel = []
# Open the file in read mode
try:
    with open(filename, "r") as f:
    # Load the JSON data from the file
        for line in f:
            data.append(json.loads(line.strip()))
except FileNotFoundError:
    print(f"Error: File '{filename}' not found!")
else:
    print("JSON data loaded successfully!")
    for i in range(0,len(data)):
        if 'technologies' in data[i]:
            data[i]['wapple'] = []
            #print(data[i]['input'])
            data[i]['wapple'].append(find_techs(data[i]['input']))
            
        else:
            pass
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#with open("/home/kali/ost/wappalyzer-cli/src/techs", "r") as json_file:
#    data = json.load(json_file)

# Get all keys
#keys = list(data.keys())
#print(keys)

with open("/home/kali/ost/output/"+sys.argv[1]+"/httpx_toolkit_status_title.json", "w") as json_file:
    # Serialize the data into a JSON string using json.dumps
    json.dump(data, json_file, indent=4)  # Optional: indent for readability

print("JSON data saved successfully!")