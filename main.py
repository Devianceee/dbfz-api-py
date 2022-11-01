import base64
from sqlite3 import converters
from urllib import request
import msgpack
import requests

get_replay = "https://dbf.channel.or.jp/api/catalog/get_replay"
data_load = "https://dbf.channel.or.jp/api/replay/data_load"

# workflow for sending to api is:
#  1) get json and pack to msgpack
#    2) add to another json and add to the key "data"
#    3) post to the api as "data=" and response will be plaintext msgpack

#    2) get msgpack data (such as exampleData variable) and encode to hex
#    3) add to another json and add to the key "data"
#    4) post to the api as "data=" and response will be plaintext msgpack

exampleData = '9295b2313830323035303733333032393434363233ad3633356661306433313734303802a5302e302e3303950701000a961cffff01ff90'
data2 = '9295b2313830323035303733333032393434363233ad3633356661306433313734303802a5302e302e330391cf031142a57cd4b99d'

headers = {
    "Accept": "*/*",
    "User-Agent": "Steam",
    "Host": "dbf.channel.or.jp",
    'Content-Type': 'application/x-www-form-urlencoded',
    "Cache-Control": "no-cache"
}


jsonData = [['180205073302944623', '635fa0d317408', 0, '0.0.3', 3], [7, 1, 0, 10, [28, 1, 1, 1, 1, []]]]

session = requests.Session()
payloadJson = {
  # "data": bytes.fromhex("9295b2313830323035303733333032393434363233ad3633356661306433313734303802a5302e302e330391cf031142a57cd4b99d  ")
  "data": msgpack.packb(jsonData)
  # "data": json
}



r1 = session.post(get_replay, headers=headers, data=payloadJson)
print("Get_replay status code:", r1.status_code)
print(r1.content)
print()
unp = msgpack.unpackb(r1.content)
print("Printing unpacked response from server:\n")
print(unp)
print("\n\nEnding...")