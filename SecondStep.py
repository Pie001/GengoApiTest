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

    #URL = "http://api.gengo.com/v2/translate/jobs"
    URL = "http://api.sandbox.gengo.com/v2/translate/jobs"
    header = {"Accept": "application/json"}

    #error msg: {'code': 2700, 'msg': 'not enough credits'}


    data = {
        "api_key": PUBLIC_KEY,
        "api_sig": PRIVATE_KEY,
        "ts": str(int(time.time()))
    }
    # use your private_key to create an hmac
    data["api_sig"] = hmac.new(
        bytes(data["api_sig"] , 'utf-8'),
        bytes(data["ts"], 'utf-8'),
        sha1
    ).hexdigest()

    job1 = {
        'slug': 'job test 1',
        'body_src': 'one two three four',
        'lc_src': 'en',
        'lc_tgt': 'ja',
        'tier': 'standard',
        'auto_approve': 1,
        'custom_data': 'some custom data untouched by Gengo.',
    }
    job2 = {
        'slug': 'job test 2',
        'body_src': 'five six seven eight',
        'lc_src': 'en',
        'lc_tgt': 'ja',
        'tier': 'standard',
        'comment': 'This one has a comment',
    }

    jobs = {'job_1': job1, 'job_2': job2}
    data["data"] = json.dumps({'jobs': jobs}, separators=(',', ':'))

    post_job = requests.post(URL, data=data, headers=header)
    res_json = json.loads(post_job.text)
    if not res_json["opstat"] == "ok":
        msg = "API error occured.\nerror msg: {0}".format(
            res_json["err"]
        )
        raise AssertionError(msg)
    else:
        print(res_json)
