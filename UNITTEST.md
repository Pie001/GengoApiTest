# Unittestを触ってみた

別記事：[Gengo APIの検証環境「Sandbox」を利用して仮の認証と注文を行う](README.md)

------------------

[gengo-python](https://github.com/gengo/gengo-python)では単体テスト用コードを提供しているので、```/tests/tests.py```を使って単体テストをやってみた。

Pythonは動的型言語(dynamic programming language)なので、実行のタイミングにエラーが発覚する可能性が多いため(特にType Error...)、C#やJavaみたいにコンパイルできればある程度は動作に対する保証(?)ができる静的型言語(statically typed language)とは異なる。

参考：[26.4. unittest — ユニットテストフレームワーク](https://docs.python.jp/3/library/unittest.html)

## 事前準備
- tests.pyを作業フォルダーにコピーしてGengoUnitTests.pyに名前を変更
- 私の場合、実行はPython3で行う

## 単体テスト

### TestGengoCoreを検証してみた
ターミナルで下記コマンドを入力(対象ファイルはGengoUnitTests.py)

```python3 -m unittest -v GengoUnitTests.TestGengoCore```

結果
```
test_GengoAuthBadCredentials (GengoUnitTests.TestGengoCore) ... /usr/local/lib/python3.6/site-packages/urllib3/connectionpool.py:858: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
  InsecureRequestWarning)
ok
test_GengoAuthNoCredentials (GengoUnitTests.TestGengoCore) ... ok
test_MethodDoesNotExist (GengoUnitTests.TestGengoCore) ... ok

----------------------------------------------------------------------
Ran 3 tests in 2.089s

OK
```

### TestAccountMethodsを検証してみた
実行

```python3 -m unittest -v GengoUnitTests.TestAccountMethods```

結果
```
test_getAccountBalance (GengoUnitTests.TestAccountMethods) ... ok
test_getAccountStats (GengoUnitTests.TestAccountMethods) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.002s

OK
```

なるほど。こんな感じなのね。

## まとめ
Pythonのunittest機能はあまり知識がなかったので、こうやってやってみるとなんとなく分かりそうな気がして楽しかった。

p.s.<br/>
自分でコードを書いて勉強せねばと思います。
