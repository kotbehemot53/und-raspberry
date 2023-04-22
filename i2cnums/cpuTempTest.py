from urllib.request import urlopen
import json

json_url = urlopen('http://192.168.1.118:8085/data.json') #todo temp stuff
data = json.loads(json_url.read())
tempStrRaw = data["Children"][0]["Children"][1]["Children"][3]["Children"][0]["Value"]
newTempStr = "  " + tempStrRaw[:2] + tempStrRaw[3:4] + "0"

print("jajo")
print(newTempStr)