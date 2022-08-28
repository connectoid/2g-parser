import random
import requests

proxy_dict = {
    "1":"http://1WQRNoXjZ0:Hm58u4LKq1@194.48.154.228:19552",
    "2":"http://uPF4pjHnv2:HrDBi1wyF7@185.156.75.58:24992",
    "3":"http://8K5niNeyDg:c8U2KxbvTJ@185.5.250.192:20974",
    "4":"http://Tdwrh5iDuE:IYUo023yjl@185.5.250.240:12417",
    "5":"http://YAGrkhisbt:TOF3LXDdnV@185.156.75.144:12091",
    "6":"http://hbRTeEZcOM:Epo1uKUjaX@185.5.251.31:14029",
    "7":"http://YfxCLlkOzi:MVjEAl0xTJ@185.5.250.29:21348",
    "8":"http://1b3N7aCus9:19t6BsPm38@185.58.205.216:13482",
    "9":"http://XnO1Q5KIVv:EjH5VbrnsK@185.58.207.222:24372",
    "0":"http://K7MosZXq5W:LPnOUQ2s3J@194.48.155.27:25323",
}

proxy_value = random.choice(list(proxy_dict.values()))
proxy = {'http': proxy_value}

print(proxy)
url = 'http://icanhazip.com'
response = requests.get(url, proxies=proxy).text
print(response)
