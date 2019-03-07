import subprocess
import requests


get_adapter = """airmon-ng | awk '{ if ($4 == "Ralink") print $2 }'"""
p = subprocess.Popen(get_adapter, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
interface = output.decode('utf-8').replace('\n', '')

cmd = 'iwlist ' + interface + ' scanning'
p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
result = p.communicate()[0]

networks = result.decode('utf-8').split('Cell')

json_data = {}
data = {}
json_data["networks"] = networks

for idx, network in enumerate(json_data["networks"]):
    json_data["networks"][idx] =\
        network.split('\n')

get_mac_address = """cat /sys/class/net/eth0/address"""
p = subprocess.Popen(get_mac_address, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
mac_address = output.decode('utf-8')
params = {'mac': mac_address, 'location': '0, 0'}
requests.get(url='IPADDRESS:8080/network', params=params)

# print(json_data["networks"][1])
