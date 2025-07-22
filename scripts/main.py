from dataclasses import dataclass

@dataclass
class App:
    name: str
    ios_url: str
    ggl_url: int

# apps = [
#     App(
#         name="eco",
#         ios_url="https://apps.apple.com/us/app/eco%E6%A4%9C%E5%AE%9A-%E5%95%8F%E9%A1%8C%E9%9B%86%E3%82%A2%E3%83%97%E3%83%AA-%E3%82%A8%E3%82%B3%E6%A4%9C%E5%AE%9A-%E7%92%B0%E5%A2%83%E7%A4%BE%E4%BC%9A%E6%A4%9C%E5%AE%9A%E8%A9%A6%E9%A8%93/id6443938132",
#         ggl_url="https://play.google.com/store/apps/details?id=jp.ktg.eco",
#     ),
#     App(
#         name="eco-text",
#         ios_url="https://apps.apple.com/us/app/eco%E6%A4%9C%E5%AE%9A-%E9%87%8D%E8%A6%81%E8%AA%9E%E5%8F%A5%E3%82%A2%E3%83%97%E3%83%AA-%E3%82%A8%E3%82%B3%E6%A4%9C%E5%AE%9A-%E7%92%B0%E5%A2%83%E7%A4%BE%E4%BC%9A%E6%A4%9C%E5%AE%9A%E8%A9%A6%E9%A8%93/id6449150376",
#         ggl_url="https://play.google.com/store/apps/details?id=jp.ktg.ecotextbook",
#     ),
# ]

# TODO: https://play.google.com/store/apps/developer?id=%E6%A0%AA%E5%BC%8F%E4%BC%9A%E7%A4%BE%E3%82%AD%E3%82%A4%E3%83%AD%E4%B9%83%E3%82%AB%E3%83%A2 からスクレイピングして以下の処理を行う
# - アプリの詳細URL（ /store/apps/details?id=[アプリID]）を取得
# - アプリのフィーチャー画像（.Shbxxd の中のimg）を取得

# TODO: 各アプリの詳細画面に対して、以下の処理を行う
# for app in apps:
    # TODO: ggl_urlからスクレイピングして、以下の処理をする
    # - アプリ名、「このアプリについて」（ class=bARER ）を取得し、src/content/apps/{アプリIDのドットをハイフンに変換した文字列}.md
    # - アプリアイコン画像を取得し、f’/src/assets/apps/{アプリIDのドットをハイフンに変換した文字列}/icon.webp’に保存する
    # - アプリの巣クイーンショット画像を取得し、f’/src/assets/apps/{アプリIDのドットをハイフンに変換した文字列}/ss{00から始まる画像の連番}.webp’に保存する

