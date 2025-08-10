---
title: NetlifyにデプロイしたWebサイトをGoogleにインデックス登録してもらうための設定
description: NetlifyにデプロイしたWebサイトがGoogleのクローリングで504になってしまう場合の解消方法を説明します
date: 2025-07-30
categories: [Web]
author: y-watanabe
tags: [SEO, Netlify, SearchConsole]
hideToc: false
complexity: 10
---

#### 経緯

先日リニューアルした本サイトのSEO対策でGoogleのSearchConsoleからサイトマップを送信したのですが、なかなかインデックス登録されず調査をしはじめました。

状況としては、SearchConsole上はサーバエラー（5XX）が原因とのことでしたが、ブラウザから当該URLにアクセスしても正常に表示される、というものでした。

---

#### 調査

ChatGPTに尋ねると、ユーザエージェントをGoogleのbotのものにしてcURLすると確認できる、とのことだったので、早速下記のコマンドで確認。

```sh
curl -A "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" -I https://ki-iro.co.jp/apps/jp-ktg-eco/
```

```sh
HTTP/2 504
age: 28
cache-control: private,max-age=0
cache-status: "Netlify Edge"; fwd=miss
content-type: text/plain; charset=utf-8
date: Tue, 29 Jul 2025 03:35:11 GMT
server: Netlify
strict-transport-security: max-age=31536000
x-nf-request-id: 01K1A3YBMRZ14FJR4QEZ4ES924
content-length: 0
```

エラーになっていました。

原因は、NetlifyのPrerenderingの設定が有効になっていたためでした。
（2025年7月時点ではデフォルトで有効になっていました）

> Enable prerendering to allow crawlers used by search engines and social networks to see the pages rendered by your app.

本サイトはSSG(Static Site Generator)で作っているため、設定の相性が良くなかったようです。

---

#### 対処

Netlifyの設定画面からPrerenderingを無効にしました。

Build & deploy settings > Post processing > Prerendering 

<img src="/images/blog/netlify-deploy/img01.png" style="max-height: 200px;"  class="blog-image">


すると、

```sh
curl -A "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" -I https://ki-iro.co.jp/apps/jp-ktg-eco/
```

```sh
HTTP/2 200
accept-ranges: bytes
age: 0
cache-control: public,max-age=0,must-revalidate
cache-status: "Netlify Edge"; fwd=miss
content-type: text/html; charset=UTF-8
date: Tue, 29 Jul 2025 03:49:54 GMT
etag: "9100b60e9fd7b76d445492f8f3e90667-ssl"
server: Netlify
strict-transport-security: max-age=31536000
x-nf-request-id: 01K1A4T52B07NZR7ZW7KM6JC6Z
content-length: 36103
```

200を返すようになりました🎉
