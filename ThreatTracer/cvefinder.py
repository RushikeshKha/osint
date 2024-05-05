import requests
import json
import sys
import requests
import re
import json
import subprocess

def run_naabu(target):
    command = ["naabu", "-host", target]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Error occurred: {stderr.decode()}")
        return []

    open_ports = []
    for line in stdout.decode().split("\n"):
        print(line)
        match = re.search(r"{}:(\d+)".format(target), line)
        if match:
            open_ports.append(int(match.group(1)))

    return open_ports


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


filename = "output/"+sys.argv[1]+"/httpx_toolkit_status_title.json"
data = []

try:
    with open(filename, "r") as f:
    
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: File '{filename}' not found!")
else:
    print("cevfinder: Data loaded successfully!")
    for i in range(0,len(data)):
        data[i]['naabu'] = []
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
            print('=================')
            print('Running Naabu\n')
            data[i]['naabu'] = run_naabu(data[i]['input'])
        else:
            pass


with open("output/"+sys.argv[1]+"/final.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("cvefinder: data saved successfully in ouput/"+sys.argv[1]+"/final.json")