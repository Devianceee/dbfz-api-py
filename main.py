import base64
from sqlite3 import converters
from urllib import request
import msgpack
import requests

get_replay = "https://dbf.channel.or.jp/api/catalog/get_replay"
data_load = "https://dbf.channel.or.jp/api/replay/data_load"

data = '9295b2313830323035303733333032393434363233ad3633356661306433313734303802a5302e302e3303950701000a961cffff01ff90'

headers = {
    "User-Agent": "Steam",
    "Host": "dbf.channel.or.jp",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cache-Control": "no-cache"
}

# base = base64.b64decode('OTI5NWIyMzEzODMwMzIzMDM1MzAzNzMzMzMzMDMyMzkzNDM0MzYzMjMzYWQzNjMzMzU2NjYxMzA2NDMzMzEzNzM0MzAzODAyYTUzMDJlMzAyZTMzMDM5NTA3MDEwMDBhOTYxY2ZmZmYwMWZmOTA=').hex
# base = format(data, '#X ')
convertedHex = (bytearray.fromhex(data))
# print(convertedHex)
# print(msgpack.unpackb(convertedHex))

jsonData = [['180205073302944623', '635fa0d317408', 2, '0.0.3', 3], [7, 1, 0, 10, [28, -1, -1, 1, -1, []]]]

packedMsg = (msgpack.packb(jsonData))

session = requests.Session()

foo = session.post(data_load, headers=headers, data=packedMsg, verify=False)
print("Get_replay status code:", foo.status_code)
print(foo.content)
# unp = msgpack.unpackb(foo.content)
# print(unp)
print("\n\nEnding...")