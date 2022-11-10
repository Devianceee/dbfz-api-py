import binascii
import json

import msgpack
import requests

get_replay_url = "https://dbf.channel.or.jp/api/catalog/get_replay"
login_url = "https://dbf.channel.or.jp/api/user/login"

data_load_url = "https://dbf.channel.or.jp/api/replay/data_load"
get_ranking_url = "https://dbf.channel.or.jp/api/ranking/my_ranking_all"
read_profile_url = "https://dbf.channel.or.jp/api/tus/read"

headers = {
    "Host": "dbf.channel.or.jp",
    'Content-Type': 'application/x-www-form-urlencoded',
}

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

def timestampCalculator():
  loginJson = [["", "", 2,"0.0.3", 3],["76561198077238939", "110000106f8de9b", 256, 0]]
  loginResponse = requests.Session().post(login_url, headers=headers, data={"data": binascii.hexlify(msgpack.packb(loginJson))})
  print("login_url status code:", loginResponse.status_code)
  return decode_list(msgpack.unpackb(loginResponse.content))[0][0]

jsonData = [
  [
    "180205073302944623", # player ID doing request(?)
    timestampCalculator(), # timestamp which is taken from the login_url response
    2,
    "0.0.3", # game version
    3
  ],
  [
    7, #???
    1, # order by [1: newest, 2: views, etc]
    0, # number of replay pages scrolled (starts at 0), max is 50000 upwards but gets very slow so best to stick to 5000 or less
    1, # number of matches queried, can be more than 10000
    [
      28, #???
      -1, # character list, [all character: -1, ssj goku: 0, ssj vegeta: 1, etc] always goes upwards (easy to make enum)
      102, # query for play mode, [-1: all modes, 102: ranked, 104: casual, 103: arena, 105: ring, 107: ring party match, 110: tournament]
      11, # queries from this number downwards up to 10 ranks (starts at 1), can go up to 50000 upwards but gets very slow so best to stick to 5000 or less
      -1, #???
      []
    ]
  ]
]

getReplayRequest = requests.Session().post(get_replay_url, headers=headers, data={"data": binascii.hexlify(msgpack.packb(jsonData))})
print("Get_replay status code:", getReplayRequest.status_code)
print()
print("Writing unpacked response from server...")
print(json.dumps(decode_list(msgpack.unpackb(getReplayRequest.content)), indent=4))

print("\n\nEnding...")