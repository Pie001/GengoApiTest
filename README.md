# GengoApiTest

別記事：[Unittestを触ってみた](UNITTEST.md)

----------------

## Gengo APIの検証環境「Sandbox」を利用して仮の認証と注文を行う

Pythonの勉強を兼ねて、Gengoというクラウドソーシングの翻訳サービスのAPIの検証環境を使ってみたのでその流れをまとめてみました。

## Gengoとは？
[https://gengo.com/](https://gengo.com/)

クラウドソーシングの翻訳サービスです。

日本最大級のクラウドソーシング翻訳サービス、ゲンゴ。37ヵ国語に対応しており、翻訳を早くリーズナブルに提供しています。英語や中国語の翻訳を実績あるトランスレーターに依頼でき、ECサイト・旅行サイト・記事の翻訳など幅広く対応しています。

## 作業の流れ
参考「[はじめの一歩 | Gengo API](http://developers.gengo.com/ja/v2/first_steps/)」


### 1. sandboxのアカウントを作る

![0021-1](/post/0021-1.png)
[Gengo API Sandbox](http://sandbox.gengo.com/)にアクセスして、「Create a sandbox account」をクリックしてアカウント作成！


![0021-2](/post/0021-2.png)
作成したアカウントでログインすればこの画面が表示されます。

### 2. API Keysの確認
![0021-3](/post/0021-3.png)
右上のアカウント名をクリックして表示されるメニューから「API Settings」をクリックしてAPI Keysを確認します。

GengoのAPI Keysは公開キーと秘密キーの２つで構成されていて、Sandboxでは複数のAPI Keysを作成したり破棄することができます。

### 3. ではAPIにCALLしてみよう

#### 3-1. GET呼び出し
提供している言語ペアを取得してみましょう。

```python
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
        "ts": str(int(time.time()))
    }

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
```

結果はこんな感じでjsonで返されます。
```json
{
	"opstat": "ok",
	"response": [
		{
			"lc_src": "es-la",
			"lc_tgt": "en",
			"tier": "standard",
			"unit_price": "0.0500",
			"currency": "USD"
		},
		...
	]
}
```

基本的にドキュメントにあるコードのままですが、いくつか注意する点がありました。

- urlは必ずapi.sandbox.gengo.comに変更する
- hmacでハッシュ化するパラメーターはstrではなくbytesに変換する

特に2番目ですが、python3以上ではドキュメントのコードをそのままコピペするとTypeErrorになってしまうので、必ずbytesに変換してあげる必要があります。

Gengoライブラリーの中身も確認しましたが、ハッシュ化の際はパラメーターの値をcompatibletextメソッドを使ってbytes(text, 'utf-8')処理をしていました。

##### 日本語の言語ペアのみを取得したい

上記のままだと結果が多すぎて欲しい言語ペアを探すのが難しいですね。

対象言語を絞りたい場合は「lc_src」パラメーターを追加して試すこともできます。

先ほど利用したコードの17行目辺りのdataを下記の内容に修正します。
```python
    data = {
        "api_key": PUBLIC_KEY,
        "api_sig": PRIVATE_KEY,
        "ts": str(int(time.time())),
        "lc_src": 'ja' 
    }
```

"lc_src": 'ja' を設定してリクエストをすると、下のように日本語で絞った結果が返されます。
```json
{
	"opstat": "ok",
	"response": [
		{
			"lc_src": "ja",
			"lc_tgt": "en",
			"tier": "standard",
			"unit_price": "0.0300",
			"currency": "USD"
		},
		...
	]
}
```

#### 3-2. POST呼び出し

次は翻訳の依頼をしてみましょう。

```python
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
```

ドキュメントにあるコードをほぼそのまま、先ほどGET CALLしたときの注意点だけを直してリクエストを出しました。が

```json
AssertionError: API error occured.
error msg: {'code': 2700, 'msg': 'not enough credits'}
```
エラーコード：2700？金が足りない？

[エラーコード一覧](http://developers.gengo.com/ja/v2/api_methods/error_codes/)で確認してみると```2700 : ポイントが不足しています - ポイントを追加購入してください```らしいです。あ、そういうことですか。


![0021-4](/post/0021-4.png)
いそいそとSandboxから「Add credits」をクリックしてポイント($100.53)をチャージしました。

では再度呼び出し！

```json
{
	"opstat": "ok",
	"response": {
		"order_id": 184972,
		"job_count": 2,
		"credits_used": "0.56",
		"currency": "USD"
	}
}
```
今度は正常に動作したようで、期待した値が返されました。

![0021-5](/post/0021-5.png)

SandboxのDashboardに先ほど注文した内容が表示されました〜。

注文した内容を消したい場合は「Delete jobs」をクリックすれば、何回も注文APIを叩いてはさっぱりしたDashboardに戻せます。また、注文した依頼の流れを体験したい場合は「Actions」をいじれば、コメント追加や再検討や進行などの表示変化を確認できます。


#### さいごに
今回はpythonを用いたAPIの呼び出し方の勉強がてらチュートリアルに合わせてやってみました。

もし、実際に開発をする場合は、公式のライブラリーを使う方が良いでしょう。

[Gengo Python Library (for the Gengo API)](https://github.com/gengo/gengo-python)

#### Gengoライブラリーを使って日本語で提供している言語ペアを取得
```
#!/usr/bin/env PYTHONIOENCODING=UTF-8 python3
# -*- coding: utf-8 -*-
from gengo import Gengo

gengo = Gengo(
    public_key='public_key',
    private_key='private_key',
    sandbox=True)

print(gengo.getServiceLanguagePairs(lc_src='ja'))
```
