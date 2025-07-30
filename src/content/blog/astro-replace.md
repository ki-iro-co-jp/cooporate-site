---
title: WebサイトをAstroでリニューアルしました
description: プレーンなHTML/CSSで作られた弊社コーポレートサイトをAstroでリプレイスしてみました。
date: 2025-07-22
categories: [Web]
author: y-watanabe
tags: [Astro, React, TypeScript, Netlify]
hideToc: false
complexity: 50
---

#### 静的HTMLからAstroへ ——自社サイトをリプレイス

弊社のコーポレートサイトを「静的なHTML + CSS」から「[Astro](https://astro.build/)」にリプレイスしたお話を共有します。

---

##### なぜリプレイスしたのか？

これまでのサイトは、静的HTMLとCSSで構築されており、以下のような課題がありました。

- ページ共通パーツ（ヘッダー・フッターなど）の管理が煩雑
- ページの追加・修正のたびに同じコードを複数のページにコピペ（情報発信のハードルが高くなってしまっていた）

そこで、**保守性を高めつつ、学習コストが低いフレームワークを導入したい**と考え、Astroを採用しました。

---

##### Astroを選んだ理由

GatsbyやNextとも悩んだのですが、その中でAstroを選んだ理由は以下の通りです。

- 表示速度が高速（と比較）
- コンポーネント分割が簡単で、**再利用性が高い**
- Markdownコンテンツやブログ機能の追加も容易
- Netlifyとの相性が良く、**デプロイがスムーズ**

---

##### リプレイスの進め方

ざっくりですが、手順を説明します。

1. Astroのテーマを選定( https://astro.build/themes/ )

    無料のテンプレートがいくつもあるので、その中から選びました。

    <img src="/images/blog/astro-replace/img01.png" class="blog-image">

2. 選んだテンプレートのGitHubからソースをダウンロードしてプロジェクト直下にコピー

3. **npm install**して**npm run dev**で簡単に起動できます

4. .astroという見慣れない拡張子に戸惑いましたが、VSCodeにastro用の拡張機能があるのでインストールして何とか乗り越えました

    <img src="/images/blog/astro-replace/img02.png" style="max-height: 150px;"  class="blog-image">


5. ホットリロード機能があるので、画面を確認しながら不要な機能やデフォルトのブログサンプルなどを削除して調整

6. pushしてNetlifyへデプロイ

    設定はこんな感じです

    <img src="/images/blog/astro-replace/img03.png" style="max-height: 200px;"  class="blog-image">

    **npm run build**して、公開ディレクトリを **/dist** にすればOK

##### やってよかったこと

- 共通レイアウトのコンポーネント化によって修正が1か所で済むようになった
- ビルドとホットリロードで、更新作業がとてもスムーズ
- Search Console用のサイトマップも自動生成してくれるのでSEO対策が楽
