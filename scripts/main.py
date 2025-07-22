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

import requests
from bs4 import BeautifulSoup
import re

import requests
from bs4 import BeautifulSoup
import re
import os

def get_app_details(app_url):
    response = requests.get(app_url)
    soup = BeautifulSoup(response.content, "html.parser")

    app_name = soup.find("h1").text

    about_section = soup.find("div", {"class": "bARER"})
    description = about_section.text.strip() if about_section else ""

    icon_url = soup.find("img", {"class": "T75of"})["src"]

    return {
        "name": app_name,
        "description": description,
        "icon_url": icon_url,
    }

def main():
    developer_url = "https://play.google.com/store/apps/developer?id=%E6%A0%AA%E5%BC%8F%E4%BC%9A%E7%A4%BE%E3%82%AD%E3%82%A4%E3%83%AD%E4%B9%83%E3%82%AB%E3%83%A2"
    response = requests.get(developer_url)
    soup = BeautifulSoup(response.content, "html.parser")

    app_urls = []
    for a in soup.find_all("a", href=True):
        if a["href"].startswith("/store/apps/details?id="):
            app_urls.append(f"https://play.google.com{a['href']}")

    # Remove duplicates
    app_urls = sorted(list(set(app_urls)))

    for url in app_urls:
        print(f"Scraping {url}")
        app_id = url.split("id=")[1]
        app_id_hyphenated = app_id.replace(".", "-")

        details = get_app_details(url)

        # Create markdown file
        content_dir = f"src/content/apps"
        os.makedirs(content_dir, exist_ok=True)
        with open(f"{content_dir}/{app_id_hyphenated}.md", "w") as f:
            f.write(f"---\n")
            f.write(f"title: {details['name']}\n")
            f.write(f"---\n\n")
            f.write(details["description"])

        # Download images
        assets_dir = f"src/assets/apps/{app_id_hyphenated}"
        os.makedirs(assets_dir, exist_ok=True)

        # Icon
        icon_response = requests.get(details["icon_url"])
        with open(f"{assets_dir}/icon.webp", "wb") as f:
            f.write(icon_response.content)


if __name__ == "__main__":
    main()

