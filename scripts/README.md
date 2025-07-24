# Appsページcontent取得スクリプト

## 使い方

- `python3 scripts/main.py`
- `iOS URL Not set [アプリID]`が出力された場合、`ios_urls`にレコードを追加して再実行
- PlayStoreのデベロッパページから取得しているが、このページがコンテンツを動的に追加読み込みする形なので、ブラウザで全アプリの情報を読み込んだ上、デベロッパツールで`body`を`Copy Element`し、`scripts/source.txt`にペーストして、それを読み込んでいる

## 新規アプリリリース時

- https://play.google.com/store/apps/developer?id=%E6%A0%AA%E5%BC%8F%E4%BC%9A%E7%A4%BE%E3%82%AD%E3%82%A4%E3%83%AD%E4%B9%83%E3%82%AB%E3%83%A2 を開く（デベロッパツール起動）
- 一番下までスクロール
- デベロッパツールの`Element`タブで`body`を選択して`Copy Element`
- `scripts/source.txt`にペースト
- `python3 scripts/main.py`
- `iOS URL Not set [アプリID]`が表示されるので、該当のiOSアプリのURLを調べてdict（`ios_urls`）にレコードを追加
- `python3 scripts/main.py`
