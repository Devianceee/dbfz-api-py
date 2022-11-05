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
read_profile = "https://dbf.channel.or.jp/api/tus/read"


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

# json only queries ranks from

exampleData = '9295b2313830323035303733333032393434363233ad3633356661306433313734303802a5302e302e3303950701000a961cffff01ff90' # https://dbf.channel.or.jp/api/catalog/get_replay
ranked_1st_to_10th = "9295b2313830323035303733333032393434363233ad3633363561386339373264363202a5302e302e3303950701000a961cff6601ff90"
ranked_91st_to_100th = "9295b2313830323035303733333032393434363233ad3633363561386339373264363202a5302e302e3303950701000a961cff665bff90"

headers = {
    "Host": "dbf.channel.or.jp",
    'Content-Type': 'application/x-www-form-urlencoded',
}

jsonData = [
  [
    "180205073302944623", # player ID doing request(?)
    "6365a8c972d62", # timestamp which is always around 2-3 years ahead, can mostly ignore (current timestamp = Friday, 30 May 2025 13:39:53.938)
    2,
    "0.0.3", # game version
    3
  ],
  [
    7,
    1, # order by [1: newest, 2: views, etc]
    0, # number of replay pages scrolled (starts at 0), max is 50000 upwards but gets very slow so best to stick to 5000 or less
    10,
    [
      28,
      -1, # character list, [all character: -1, ssj goku: 0, ssj vegeta: 1, etc] always goes upwards (easy to make enum)
      102, # query for play mode, [-1: all modes, 102: ranked, 104: casual, 103: arena, 105: ring, 107: ring party match, 110: tournament]
      1, # queries from this number downwards up to 10 ranks (starts at 1(?))
      -1,
      []
    ]
  ]
]

session = requests.Session()
payloadJson = {
  # "data": bytes.fromhex("9295b2313830323035303733333032393434363233ad3633363539383263343130616602a5302e302e330391a6323032323131") #doesnt work
  # "data": "9295b2313830323035303733333032393434363233ad3633363539383263343130616602a5302e302e3303950701000a961cffff01ff90" #works
  "data": binascii.hexlify(msgpack.packb(jsonData)) #works
  # "data": ranked_91st_to_100th
}

r1 = session.post(get_replay, headers=headers, data=payloadJson, verify=False)
print("Get_replay status code:", r1.status_code)
print()
# print("Printing hexlify'ed response from server:\n")
# temp = binascii.hexlify(r1.content).decode("utf-8")
# print(temp)
# print()
print("Writing unpacked response from server...")
# print(msgpack.unpackb(r1.content))
unpackedJson = decode_list(msgpack.unpackb(r1.content))
# print(json.dumps(unpackedJson, indent=4))
with open('testing_reduced_query.json', 'w') as f:
  json.dump(unpackedJson, f, indent=4)
print("\n\nEnding...")