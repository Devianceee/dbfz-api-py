# dbfz-api-py
 Async library for interfacing with the replay REST API of Dragonball FighterZ

## How the API works
The API works by sending a POST request to https://dbf.channel.or.jp/api/catalog/get_replay. 
The header needs to contain ```Content Type: application/x-www-form-urlencoded``` as you need to pass a hex (non-escaped) encoded messagepack to the server.

The server will then give a response back in hex encoded messagepack which can be unpacked.

## Making request
### JSON Structure
```python
[
  [
    "180205073302944623", # player ID doing request(?)
    "6365a8c972d62", # timestamp which is always around 2-3 years ahead, can mostly ignore (current timestamp = Friday, 30 May 2025 13:39:53.938)
    2, # unknown
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
      102, # query for play mode, [all modes: -1 , ranked: 102 , casual: 104, arena: 103, ring: 105, ring party match: 107, tournament: 110]
      1, # queries from this number downwards up to 10(?) ranks (starts at 1(?))
      -1,
      []
    ]
  ]
]
```

### Workflow to Send Request
The workflow for sending to api is:
1) Get json and pack to msgpack
2) Add to another json and add to the key "data", and transform the escaped hex to hex. For example: ```binascii.hexlify(msgpack.packb(jsonData))```
3) POST to the api as ```data=``` and response will be plaintext msgpack to be decoded using ```msgpack.unpackb()```

OR
1) Get msgpack data (such as ```exampleData``` variable inside of main.py)
2) Add to another json and add to the key "data"
3) POST to the api as ```data=``` and response will be plaintext msgpack to be decoded using ```msgpack.unpackb()```


## Parsing response
### Converting from Messagepack to JSON
You can unpack the messagepack using ```msgpack.unpackb()```, however each item in the JSON will be encoded so manually decoding 
via the functions provided (```decode_list``` and subsequently ```decode_dict```) helps it be parsed as a json

### JSON Structure

The JSON always has 10 matches inside it with the first player always being the winner. A shortened example with only one match is annotated below:
```python
[
    [
        "6365b7aff20b5",
        0,
        "2022/11/05 10:09:03", # time it was queried (irrelevant to the actual match stats)
        "0.0.3",
        "0.0.3",
        "0.0.3",
        "",
        ""
    ],
    [
        0, 
        10,
        [
            [
                221105064149496874,
                28,
                "WIN_RkmRVer028",
                [ # characters for player who won
                    0,
                    39,
                    38
                ],
                [# characters for player who lost
                    0,
                    31,
                    19
                ],
                [ # person who won
                    [
                        "211127010233268016",
                        "Deviance",
                        "76561199013492555",
                        "11000013ec6f74b",
                        856119
                    ],
                    [
                        "0",
                        "",
                        "",
                        "",
                        0
                    ],
                    [
                        "0",
                        "",
                        "",
                        "",
                        0
                    ]
                ],
                [ # person who lost
                    [
                        "210319054513269637",
                        "paddu",
                        "76561199080463934",
                        "110000142c4de3e",
                        829720
                    ],
                    [
                        "0",
                        "",
                        "",
                        "",
                        0
                    ],
                    [
                        "0",
                        "",
                        "",
                        "",
                        0
                    ]
                ],
                1,
                "2022-11-05 20:41:43", # timestamp of the match (UTC? or Japan time?)
                102,
                0,
                1,
                "",
                "",
                ""
            ]
        ]
    ]
]
```
