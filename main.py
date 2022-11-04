import base64
import json
import struct
from sqlite3 import converters
from urllib import request
import msgpack
import requests
import binascii

get_replay = "https://dbf.channel.or.jp/api/catalog/get_replay"
data_load = "https://dbf.channel.or.jp/api/replay/data_load"
get_ranking = "https://dbf.channel.or.jp/api/ranking/my_ranking_all"


def decode_list(l):
  result = []
  for item in l:
    if isinstance(item, bytes):
      result.append(item.decode())
      continue
    if isinstance(item, list):
      result.append(decode_list(item))
      continue
    if isinstance(item, dict):
      result.append(decode_dict(item))
      continue
    result.append(item)
  return result


def decode_dict(d):
  result = {}
  for key, value in d.items():
    if isinstance(key, bytes):
      key = key.decode()
    if isinstance(value, bytes):
      value = value.decode()
    if isinstance(value, list):
      value = decode_list(value)
    elif isinstance(value, dict):
      value = decode_dict(value)
    result.update({key: value})
  return result

# workflow for sending to api is:
#  1) get json and pack to msgpack
#    2) add to another json and add to the key "data", and transform the escaped hex to hex "binascii.hexlify(msgpack.packb(jsonData))"
#    3) post to the api as "data=" and response will be plaintext msgpack

#    2) get msgpack data (such as exampleData variable)
#    3) add to another json and add to the key "data"
#    4) post to the api as "data=" and response will be plaintext msgpack

exampleData = '9295b2313830323035303733333032393434363233ad3633356661306433313734303802a5302e302e3303950701000a961cffff01ff90' # https://dbf.channel.or.jp/api/catalog/get_replay
data2 = '9295b2313830323035303733333032393434363233ad3633356661306433313734303802a5302e302e330391cf031142a57cd4b99d'

headers = {
    "Host": "dbf.channel.or.jp",
    'Content-Type': 'application/x-www-form-urlencoded',
}

jsonData = [
  [
    "180205073302944623",
    "6365982c410af",
    2,
    "0.0.3",
    3
  ],
  [
    "202211"
  ]
]

session = requests.Session()
payloadJson = {
  # "data": bytes.fromhex("9295b2313830323035303733333032393434363233ad3633363539383263343130616602a5302e302e330391a6323032323131") #doesnt work
  "data": "9295b2313830323035303733333032393434363233ad3633363539383263343130616602a5302e302e3303950701000a961cffff01ff90" #works
  # "data": binascii.hexlify(msgpack.packb(jsonData)) #works
}

r1 = session.post(get_replay, headers=headers, data=payloadJson, verify=False)
print("Get_replay status code:", r1.status_code)
print()
print("Printing hexlify'ed response from server:\n")
temp = binascii.hexlify(r1.content).decode("utf-8")
print(temp)
print()
print("Printing unpacked response from server:\n")
# print(msgpack.unpackb(r1.content))
unpackedJson = decode_list(msgpack.unpackb(r1.content))
print(json.dumps(unpackedJson, indent=4))
with open('data.json', 'w') as f:
  json.dump(unpackedJson, f, indent=4)
print("\n\nEnding...")