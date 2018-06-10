#!/usr/bin/env PYTHONIOENCODING=UTF-8 python3
# -*- coding: utf-8 -*-
from hashlib import sha1
import hmac
import json
import requests
import time

if __name__ == '__main__':
    PUBLIC_KEY = 'PUBLIC_KEY'
    PRIVATE_KEY = 'PRIVATE_KEY'

    #URL = "http://api.gengo.com/v2/translate/service/language_pairs"
    URL = "http://api.sandbox.gengo.com/v2/translate/service/language_pairs"
    header = {"Accept": "application/json"}

    data = {
        "api_key": PUBLIC_KEY,
        "api_sig": PRIVATE_KEY,
        "ts": str(int(time.time()))#,
        #"lc_src": 'ja' #lc_src (optional): Source language code. Submitting this will filter the response to only relevant language pairs.
    }
    print(data["api_sig"])
    print(data["ts"]);
    print(sha1)
    # use your private_key to create an hmac
    data["api_sig"] = hmac.new(
        bytes(data["api_sig"] , 'utf-8'),
        bytes(data["ts"], 'utf-8'),
        sha1
    ).hexdigest()

    get_language_pair = requests.get(URL, headers=header, params=data)
    res_json = json.loads(get_language_pair.text)
    if not res_json["opstat"] == "ok":
        msg = "API error occured.\nerror msg: {0}".format(
            res_json["err"]
        )
        raise AssertionError(msg)
    else:
        print(res_json)
