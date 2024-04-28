import requests
import json
import sys
import requests
import re
import json

def find_cpes(component, version):
    base_url = "https://nvd.nist.gov/products/cpe/search/results"
    params = {
        "namingFormat": "2.3",
        "keyword": f"{component} {version}"
    }

    response = requests.get(base_url, params=params)
    content = response.text

    cpe_matches = re.findall(r'cpe:(.*?)<', content)
    return cpe_matches


filename = "/home/kali/ost/output/"+sys.argv[1]+"/httpx_toolkit_status_title.json"
data = []

try:
    with open(filename, "r") as f:
    
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: File '{filename}' not found!")
else:
    print("cevfinder: Data loaded successfully!")
    for i in range(0,len(data)):
        if 'wapple' in data[i]:
            data[i]['cpe'] = []
            try:
                print("subdomain: ",data[i]['input'])
                for j in range(0,len(data[i]['wapple'][0])):
                    if data[i]['wapple'][0][j]['version'] != "nil":
                        print("Finding CPE: ",data[i]['wapple'][0][j]['identifier'])
                        product = (data[i]['wapple'][0][j]['identifier'])
                        version = (data[i]['wapple'][0][j]['version'])
                        data[i]['cpe'].append(find_cpes(product,version))
                    else:
                        print(data[i]['wapple'][0][j]['identifier']+" version NA")
            except:
                print('error')
        else:
            pass


with open("/home/kali/ost/output/"+sys.argv[1]+"/final.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("cvefinder: data saved successfully in ouput/"+sys.argv[1]+"/final.json")