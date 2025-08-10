---
title: GoogleのAIエージェント「Jules」にFlutterでアプリをつくってもらいました  
description: 2025年、Googleが発表したAIエージェント「**Jules（ジュールズ）**」を使って、実際にFlutterアプリを**ほぼ指示だけで**作ってみました。
date: 2025-08-10
categories: [AI]
author: y-watanabe
tags: [AI, Jules, Flutter]
hideToc: false
complexity: 20
---

#### 結論

- 十分実用可能
- ある程度複雑な仕様でもそれなりに動くものを作ってくれる
  - **それなり**と感じた理由としては
    - UIはあまり洗練されていない
    - 複雑過ぎる仕様はちょっと誤解しちゃう（伝え方の悪さも多分にありそう）
- Julesが書いてくれたものを自分で変更しようとするとリーディングが大変（内部設計をちゃんと伝える必要がありそう）
  - 面倒なので、なんとかJulesに直してもらおうとしてしまうので、逆に労力がかかってるんじゃないか、と感じることがある

---

#### 設定

https://jules.google/ から`Try Jules`をクリックして、

<img src="/images/blog/jules-flutter/img01.png" style="max-height: 200px;"  class="blog-image">

GitHubと連携すれば使い始めることができます。

<img src="/images/blog/jules-flutter/img02.png" style="max-height: 200px;"  class="blog-image">

#### Flutterのための設定

JulesにFlutterアプリ開発を手伝ってもらうには、Julesに環境設定をしてもらわないといけません。

CodeBase（GitHubリポジトリ）の設定画面を開いて、`Configuration`の`Initial setup`にセットアップスクリプト（下記）を貼り付けて、`Run and snapshot`をクリックします。

```sh
#!/bin/bash

# Flutter SDK のバージョン
FLUTTER_VERSION="3.32.4"
FLUTTER_TAR="flutter_linux_${FLUTTER_VERSION}-stable.tar.xz"
FLUTTER_URL="https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/${FLUTTER_TAR}"

# 作業ディレクトリ
mkdir -p ~/development
cd ~/development

# ダウンロードと展開
curl -O ${FLUTTER_URL}
tar xf ${FLUTTER_TAR}
rm ${FLUTTER_TAR}

# パス追加
export PATH="$HOME/development/flutter/bin:$PATH"

# ここらへんはデバッグ用
flutter --version
flutter doctor
```

<img src="/images/blog/jules-flutter/img03.png" style="max-height: 200px;"  class="blog-image">

スクリプトが正しければ設定を保存できます。

これで準備完了です✨

---

#### 作業依頼

プロジェクトの作成は自分でやってもそこまで手間ではないので、`flutter create`コマンドを実行した状態でコミットを打って、そこからJulesに手伝ってもらうことにしました。

プロンプトは色々と試行錯誤しましたが、最終的には下記で進めることにしました。

```md
下記のアプリを作ってください。

# 収支・資産管理・シミュレーション

## Summary

- 収入、支出、投資、借入を登録することで将来の資産をシミュレーションする
- 単純な収支だけでなく、利息や流動性についても登録し、シミュレーションできる

## UI

- 画面は収入、支出、投資、借入、シミュレーションの5つのタブからなる
- デザインはMUIでthemeを柔軟に変更できるように実装する

### 収入画面

- 登録した収入が一覧で表示される
  - ListTileウィジェット
  - titleに金額（¥でカンマ区切りフォーマット）とタイトル
  - subtitleに頻度
  - trailingに編集ボタン
  - 編集ボタンは登録と同じボトムシートが表示される
    - 最下部に削除ボタンがあり、タップすると確認ダイアログが表示され、OKとキャンセルのボタンがある
- 初期状態は何も登録されておらず、「まずは収入を登録してみよう」というテキストとともに「収入を登録」ボタンが表示される
- 画面右下にFABば表示されており、タップすると収入登録フォームがボトムシートで表示される
- 収入登録フォームは以下の項目
  - タイトル
  - 金額
  - 期間：年月日で登録（未指定の場合、全期間）
  - 頻度：毎月or毎年
  - 流動性：いつでも引き出し可能、N年M月L日以降引き出し可能
  - 登録画面で「追加」ボタンをタップするとボトムシートが非表示になり、一覧に登録した収入が表示される

### 支出画面

（長くなるので省略）

### 投資画面

（長くなるので省略）

### 借入画面

（長くなるので省略）

### シミュレーション

（長くなるので省略）

## ライブラリ

- データストアとして`hive: ^2.1.0`（hive_generator）を使用する
- 状態管理は`hooks_riverpod: ^2.5.1`を使用する
- シミュレーションのグラフは`fl_chart: ^1.0.0`を使用する

## ディレクトリ

- lib/domain: 収支や支出のエンティティを配置
- lib/ui/component: 再利用可能なウィジェットを配置
- lib/ui/page: 各画面のウィジェットを配置
- lib/provider: 状態管理のプロバイダを配置
```

---

ポイントとしては、

- 画面デザインをテキストで伝えないといけないので、使うWidgetが決まっている場合はWidgetを指定すると欲しいものに近づく
- UIさえ正確に伝えられれば、挙動はよしなに実装してくれる（どのボタンをタップしたらどうなるか、まで書かなくてもOKだった）
- ライブラリはバージョンを指定しないと古いのを使っちゃう（flutterをインストールしているので、コマンドでライブラリ追加してほしいが、pubspecに直接書いてしまう模様）

---

14分後、完成の通知が来ました。

<img src="/images/blog/jules-flutter/img04.png" style="max-height: 200px;"  class="blog-image">


この画面でも実装内容を確認できるのですが、GitHubの方が見慣れているので、pushしてもらいます。

全部のコードを掲載すると長くなってしまうので、収入画面のコードを公開します！
素晴らしいクオリティですね✨

```dart
import 'package:flutter/material.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:intl/intl.dart';
import 'package:money/domain/income.dart';
import 'package:money/provider/income_provider.dart';
import 'package:money/ui/component/income_form.dart';

class IncomePage extends HookConsumerWidget {
  const IncomePage({super.key});

  void _showIncomeForm(BuildContext context, Income? income) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true, // Important for longer forms
      builder: (context) => IncomeForm(incomeToEdit: income),
    );
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final incomeBoxAsync = ref.watch(incomeBoxProvider);

    return Scaffold(
      body: incomeBoxAsync.when(
        data: (box) {
          // Box is ready, now use the notifier that depends on this box
          final incomeListAsync = ref.watch(incomeNotifierFamilyProvider(box));

          return incomeListAsync.when(
            data: (incomes) {
              if (incomes.isEmpty) {
                return Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text('まずは収入を登録してみよう', style: TextStyle(fontSize: 18)),
                      const SizedBox(height: 16),
                      ElevatedButton.icon(
                        icon: const Icon(Icons.add),
                        label: const Text('収入を登録'),
                        onPressed: () => _showIncomeForm(context, null),
                      ),
                    ],
                  ),
                );
              }

              final currencyFormatter = NumberFormat.currency(locale: 'ja_JP', symbol: '¥');

              return ListView.builder(
                itemCount: incomes.length,
                itemBuilder: (context, index) {
                  final income = incomes[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    child: ListTile(
                      title: Text('${currencyFormatter.format(income.amount)} - ${income.title}'),
                      subtitle: Text('頻度: ${income.frequency.basis.toString().split('.').last}'),
                      onTap: () => _showIncomeForm(context, income),
                    ),
                  );
                },
              );
            },
            loading: () => const Center(child: CircularProgressIndicator()),
            error: (err, stack) => Center(child: Text('Error loading incomes: $err')),
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error opening income database: $err')),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _showIncomeForm(context, null),
        child: const Icon(Icons.add),
        tooltip: 'Add Income',
      ),
    );
  }
}
```

---

手元で実行してみると、

<img src="/images/blog/jules-flutter/img05.png" style="max-height: 400px;"  class="blog-image">

ほぼイメージ通りのものができていました🎉
荒削りと言えば荒削りですが、14分でここまでのものをつくってもらえるのは有り難いです。（自分で書いたら半日はかかりそう。。

AIの進化のスピードには驚かされるばかりです。。
「指示を受けて実装する」という部分はAIに置き換えられていくと実感した瞬間でした。
