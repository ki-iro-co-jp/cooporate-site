import requests
from bs4 import BeautifulSoup
import re
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp",
    "Connection": "keep-alive",
}

ios_urls = {
    "jp.ktg.eco": "https://apps.apple.com/jp/app/eco%E6%A4%9C%E5%AE%9A-%E5%95%8F%E9%A1%8C%E9%9B%86%E3%82%A2%E3%83%97%E3%83%AA-%E3%82%A8%E3%82%B3%E6%A4%9C%E5%AE%9A-%E7%92%B0%E5%A2%83%E7%A4%BE%E4%BC%9A%E6%A4%9C%E5%AE%9A%E8%A9%A6%E9%A8%93/id6443938132",
    "jp.ktg.welfarehouse": "https://apps.apple.com/jp/app/%E7%A6%8F%E7%A5%89%E4%BD%8F%E7%92%B0%E5%A2%83%E3%82%B3%E3%83%BC%E3%83%87%E3%82%A3%E3%83%8D%E3%83%BC%E3%82%BF%E3%83%BC-%E5%95%8F%E9%A1%8C%E9%9B%86-2%E7%B4%9A-%E5%8C%BB%E7%99%82-%E7%A6%8F%E7%A5%89-%E4%BB%8B%E8%AD%B7/id6450543581",
    "jp.ktg.welfarehouse3": "https://apps.apple.com/jp/app/%E7%A6%8F%E7%A5%89%E4%BD%8F%E7%92%B0%E5%A2%83%E3%82%B3%E3%83%BC%E3%83%87%E3%82%A3%E3%83%8D%E3%83%BC%E3%82%BF%E3%83%BC-%E5%95%8F%E9%A1%8C%E9%9B%86-3%E7%B4%9A-%E5%8C%BB%E7%99%82-%E7%A6%8F%E7%A5%89-%E4%BB%8B%E8%AD%B7/id6477995484",
    "jp.ktg.generalist": "https://apps.apple.com/jp/app/g%E6%A4%9C%E5%AE%9A-%E5%95%8F%E9%A1%8C%E9%9B%86%E3%82%A2%E3%83%97%E3%83%AA/id6478066297",
    "jp.ktg.engineerbasic": "https://apps.apple.com/jp/app/%E6%8A%80%E8%A1%93%E5%A3%AB-%E5%9F%BA%E7%A4%8E%E7%A7%91%E7%9B%AE-%E9%81%8E%E5%8E%BB%E5%95%8F%E9%9B%86/id6739554285",
    "jp.ktg.machinery3": "https://apps.apple.com/jp/app/%E6%A9%9F%E6%A2%B0%E4%BF%9D%E5%85%A8%E6%8A%80%E8%83%BD%E6%A4%9C%E5%AE%9A-3%E7%B4%9A-%E9%81%8E%E5%8E%BB%E5%95%8F%E9%9B%86/id6476808807",
    "jp.ktg.gxbasic": "https://apps.apple.com/jp/app/gx%E5%95%8F%E9%A1%8C%E9%9B%86-%E3%83%99%E3%83%BC%E3%82%B7%E3%83%83%E3%82%AF-gx%E3%81%AE%E8%A9%A6%E9%A8%93%E5%AF%BE%E7%AD%96%E7%94%A8%E5%8B%89%E5%BC%B7%E3%82%A2%E3%83%97%E3%83%AA/id6590616951",
    "jp.ktg.maintainer2": "https://apps.apple.com/jp/app/%E8%87%AA%E4%B8%BB%E4%BF%9D%E5%85%A8%E5%A3%AB-2%E7%B4%9A-%E5%AD%A6%E7%A7%91%E5%95%8F%E9%A1%8C%E9%9B%86/id6467083000",
    "jp.ktg.pmp": "https://apps.apple.com/jp/app/pmp-%E3%82%AA%E3%83%AA%E3%82%B8%E3%83%8A%E3%83%AB%E5%95%8F%E9%A1%8C%E9%9B%86-%E3%83%97%E3%83%AD%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E3%83%9E%E3%83%8D%E3%82%B8%E3%83%A1%E3%83%B3%E3%83%88%E5%95%8F%E9%A1%8C%E9%9B%86/id6447619663",
    "jp.ktg.maintainer1": "https://apps.apple.com/jp/app/%E8%87%AA%E4%B8%BB%E4%BF%9D%E5%85%A8%E5%A3%AB-1%E7%B4%9A-%E5%AD%A6%E7%A7%91%E5%95%8F%E9%A1%8C%E9%9B%86/id6468426443",
    "jp.ktg.machinery1": "https://apps.apple.com/jp/app/%E6%A9%9F%E6%A2%B0%E4%BF%9D%E5%85%A8%E6%8A%80%E8%83%BD%E6%A4%9C%E5%AE%9A-1%E7%B4%9A-%E9%81%8E%E5%8E%BB%E5%95%8F%E9%9B%86/id6476808976",
    "jp.ktg.machinery2": "https://apps.apple.com/jp/app/%E6%A9%9F%E6%A2%B0%E4%BF%9D%E5%85%A8%E6%8A%80%E8%83%BD%E6%A4%9C%E5%AE%9A-2%E7%B4%9A-%E9%81%8E%E5%8E%BB%E5%95%8F%E9%9B%86/id6476808815",
    "jp.ktg.engineertalent": "https://apps.apple.com/jp/app/%E6%8A%80%E8%A1%93%E5%A3%AB-%E9%81%A9%E6%80%A7%E7%A7%91%E7%9B%AE-%E9%81%8E%E5%8E%BB%E5%95%8F%E9%9B%86-%E6%8A%80%E8%A1%93%E5%A3%AB%E8%A9%A6%E9%A8%93%E3%81%AE%E5%AF%BE%E7%AD%96%E3%82%A2%E3%83%97%E3%83%AA/id6740120131",
    "jp.ktg.pme": "https://apps.apple.com/jp/app/%E3%83%97%E3%83%AD%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E3%83%9E%E3%83%8D%E3%83%BC%E3%82%B8%E3%83%A3%E8%A9%A6%E9%A8%93-%E9%81%8E%E5%8E%BB%E5%95%8F%E9%9B%86-%E3%83%97%E3%83%AD%E3%83%9E%E3%83%8D%E3%81%AE%E9%81%8E%E5%8E%BB%E5%95%8F/id6450507923",
    "jp.ktg.gabread": "https://apps.apple.com/jp/app/gab-%E8%A8%80%E8%AA%9E-%E5%95%8F%E9%A1%8C%E9%9B%86-%E8%AB%96%E7%90%86%E7%9A%84%E8%AA%AD%E8%A7%A3%E5%AF%BE%E7%AD%96-c-gab-%E7%8E%89%E6%89%8B%E7%AE%B1/id6743147944",
    "jp.ktg.dx": "https://apps.apple.com/jp/app/dx%E6%A4%9C%E5%AE%9A-%E3%82%AA%E3%83%AA%E3%82%B8%E3%83%8A%E3%83%AB%E5%95%8F%E9%A1%8C%E9%9B%86/id1662200214",
    "jp.ktg.generalisttxt": "https://apps.apple.com/jp/app/g%E6%A4%9C%E5%AE%9A-%E5%8D%98%E8%AA%9E%E5%B8%B3/id6478640189",
    "jp.ktg.itdict": "https://apps.apple.com/jp/app/it-translation-dictionary/id6450146790",
    "jp.ktg.psychiatry": "https://apps.apple.com/jp/app/%E7%B2%BE%E7%A5%9E%E4%BF%9D%E5%81%A5%E7%A6%8F%E7%A5%89%E5%A3%AB%E5%9B%BD%E5%AE%B6%E8%A9%A6%E9%A8%93-%E9%81%8E%E5%8E%BB%E5%95%8F%E3%82%A2%E3%83%97%E3%83%AA-%E7%B2%BE%E7%A5%9E%E4%BF%9D%E5%81%A5%E7%A6%8F%E7%A5%89%E5%A3%AB/id1661621420",
    "jp.ktg.gxbasictext": "https://apps.apple.com/jp/app/gx%E5%8D%98%E8%AA%9E%E5%B8%B3-%E3%83%99%E3%83%BC%E3%82%B7%E3%83%83%E3%82%AF-gx%E3%81%AE%E8%A9%A6%E9%A8%93%E5%AF%BE%E7%AD%96%E7%94%A8%E5%8B%89%E5%BC%B7%E3%82%A2%E3%83%97%E3%83%AA/id6670433664",
    "jp.ktg.welfarehouse_textbook": "https://apps.apple.com/jp/app/%E7%A6%8F%E7%A5%89%E4%BD%8F%E7%92%B0%E5%A2%83%E3%82%B3%E3%83%BC%E3%83%87%E3%82%A3%E3%83%8D%E3%83%BC%E3%82%BF%E3%83%BC-%E9%87%8D%E8%A6%81%E8%AA%9E%E5%8F%A5-2%E7%B4%9A-%E5%8C%BB%E7%99%82-%E7%A6%8F%E7%A5%89-%E4%BB%8B%E8%AD%B7/id6462012298",
    "jp.ktg.itsecurity": "https://apps.apple.com/jp/app/%E6%83%85%E5%A0%B1%E3%82%BB%E3%82%AD%E3%83%A5%E3%83%AA%E3%83%86%E3%82%A3%E3%83%9E%E3%83%8D%E3%82%B8%E3%83%A1%E3%83%B3%E3%83%88-%E9%81%8E%E5%8E%BB%E5%95%8F%E9%A1%8C%E9%9B%86-ip%E3%81%AE%E5%8B%89%E5%BC%B7%E6%94%AF%E6%8F%B4/id1670082106",
    "jp.ktg.maintainer_textbook": "https://apps.apple.com/jp/app/%E8%87%AA%E4%B8%BB%E4%BF%9D%E5%85%A8%E5%A3%AB-%E5%8D%98%E8%AA%9E%E5%B8%B3-1%E7%B4%9A-2%E7%B4%9A/id6468481523",
    "jp.ktg.awsccpen": "https://apps.apple.com/jp/app/prep-aws-cloud-practitioner/id6747565605",
    "jp.ktg.sce": "https://apps.apple.com/jp/app/%E6%83%85%E5%A0%B1%E5%87%A6%E7%90%86%E5%AE%89%E5%85%A8%E7%A2%BA%E4%BF%9D%E6%94%AF%E6%8F%B4%E5%A3%AB%E8%A9%A6%E9%A8%93-%E9%81%8E%E5%8E%BB%E5%95%8F%E9%9B%86-%E3%82%BB%E3%82%AD%E3%82%B9%E3%83%9A%E3%81%AE%E9%81%8E%E5%8E%BB%E5%95%8F/id6450543472",
    "jp.ktg.machinerys": "https://apps.apple.com/jp/app/%E6%A9%9F%E6%A2%B0%E4%BF%9D%E5%85%A8%E6%8A%80%E8%83%BD%E6%A4%9C%E5%AE%9A-%E7%89%B9%E7%B4%9A-%E9%81%8E%E5%8E%BB%E5%95%8F%E9%9B%86/id6477385004",
    "jp.ktg.engineerwater": "https://apps.apple.com/jp/app/%E6%8A%80%E8%A1%93%E5%A3%AB-%E4%B8%8A%E4%B8%8B%E6%B0%B4%E9%81%93%E9%83%A8%E9%96%80-%E9%81%8E%E5%8E%BB%E5%95%8F%E9%9B%86-%E5%B0%82%E9%96%80%E7%A7%91%E7%9B%AE%E3%81%AE%E5%AF%BE%E7%AD%96%E3%82%A2%E3%83%97%E3%83%AA/id6746373176",
    "jp.ktg.awsccp": "https://apps.apple.com/jp/app/aws-%E3%82%AF%E3%83%A9%E3%82%A6%E3%83%89%E3%83%97%E3%83%A9%E3%82%AF%E3%83%86%E3%82%A3%E3%82%B7%E3%83%A7%E3%83%8A%E3%83%BC-%E3%82%AA%E3%83%AA%E3%82%B8%E3%83%8A%E3%83%AB%E5%95%8F%E9%A1%8C%E9%9B%86/id6744286280",
    "jp.ktg.jlptn5": "https://apps.apple.com/jp/app/jlpt-n5-wordbook/id6670312383",
    "jp.ktg.fp2": "https://apps.apple.com/jp/app/fp2%E7%B4%9A-%E9%81%8E%E5%8E%BB%E5%95%8F%E3%82%A2%E3%83%97%E3%83%AA/id6473820953",
    "jp.ktg.engineerelectric": "https://apps.apple.com/jp/app/%E6%8A%80%E8%A1%93%E5%A3%AB-%E9%9B%BB%E6%B0%97%E9%9B%BB%E5%AD%90%E9%83%A8%E9%96%80-%E9%81%8E%E5%8E%BB%E5%95%8F%E9%9B%86-%E5%B0%82%E9%96%80%E7%A7%91%E7%9B%AE%E3%81%AE%E5%AF%BE%E7%AD%96%E3%82%A2%E3%83%97%E3%83%AA/id6743985436",
    "jp.ktg.veterinary_nurse": "https://apps.apple.com/jp/app/%E6%84%9B%E7%8E%A9%E5%8B%95%E7%89%A9%E7%9C%8B%E8%AD%B7%E5%B8%AB-%E5%95%8F%E9%A1%8C%E9%9B%86%E3%82%A2%E3%83%97%E3%83%AA-%E6%84%9B%E7%8E%A9%E5%8B%95%E7%89%A9%E7%9C%8B%E8%AD%B7%E5%B8%AB%E5%9B%BD%E5%AE%B6%E8%A9%A6%E9%A8%93%E5%AF%BE%E7%AD%96/id1668797681",
    "jp.ktg.nwse": "https://apps.apple.com/jp/app/%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF%E3%82%B9%E3%83%9A%E3%82%B7%E3%83%A3%E3%83%AA%E3%82%B9%E3%83%88-%E9%81%8E%E5%8E%BB%E5%95%8F%E9%A1%8C%E9%9B%86-nw%E5%8B%89%E5%BC%B7%E6%94%AF%E6%8F%B4/id1672829104",
    "jp.ktg.ainu": "https://apps.apple.com/jp/app/%E3%82%A2%E3%82%A4%E3%83%8C%E8%AA%9E%E8%BE%9E%E5%85%B8/id6446929632",
    "jp.ktg.engineermachine": "https://apps.apple.com/jp/app/%E6%8A%80%E8%A1%93%E5%A3%AB-%E6%A9%9F%E6%A2%B0%E9%83%A8%E9%96%80-%E9%81%8E%E5%8E%BB%E5%95%8F%E9%9B%86-%E6%8A%80%E8%A1%93%E5%A3%AB-%E5%B0%82%E9%96%80%E7%A7%91%E7%9B%AE%E3%81%AE%E5%AF%BE%E7%AD%96%E3%82%A2%E3%83%97%E3%83%AA/id6743040858",
    "jp.ktg.itpassport": "https://apps.apple.com/jp/app/it%E3%83%91%E3%82%B9%E3%83%9D%E3%83%BC%E3%83%88-%E9%81%8E%E5%8E%BB%E5%95%8F%E9%A1%8C%E9%9B%86-it%E3%81%AE%E5%9F%BA%E7%A4%8E%E3%82%B9%E3%82%AD%E3%83%AB%E7%BF%92%E5%BE%97%E3%82%92%E6%94%AF%E6%8F%B4/id1665625417",
    "jp.ktg.engineerconstruction": "https://apps.apple.com/jp/app/%E6%8A%80%E8%A1%93%E5%A3%AB-%E5%BB%BA%E8%A8%AD%E9%83%A8%E9%96%80-%E9%81%8E%E5%8E%BB%E5%95%8F%E9%9B%86-%E6%8A%80%E8%A1%93%E5%A3%AB-%E5%B0%82%E9%96%80%E7%A7%91%E7%9B%AE%E3%81%AE%E5%AF%BE%E7%AD%96%E3%82%A2%E3%83%97%E3%83%AA/id6740739069",
    "jp.ktg.pmptext": "https://apps.apple.com/jp/app/pmp-japanese-dictionary/id6474183779",
    "jp.ktg.business": "https://apps.apple.com/jp/app/%E5%95%86%E6%A5%AD%E7%B5%8C%E6%B8%88%E6%A4%9C%E5%AE%9A-%E3%83%93%E3%82%B8%E3%83%8D%E3%82%B9%E5%9F%BA%E7%A4%8E-%E5%95%8F%E9%A1%8C%E9%9B%86%E3%82%A2%E3%83%97%E3%83%AA/id1663773775",
    "jp.ktg.sfdctext": "https://apps.apple.com/jp/app/sfdc-%E8%AA%8D%E5%AE%9A%E3%82%A2%E3%82%BD%E3%82%B7%E3%82%A8%E3%82%A4%E3%83%88-%E5%8D%98%E8%AA%9E%E5%B8%B3%E3%82%A2%E3%83%97%E3%83%AA/id6535655396",
    "jp.ktg.topik": "https://apps.apple.com/jp/app/topik-%E9%9F%93%E5%9B%BD%E8%AA%9E%E8%83%BD%E5%8A%9B%E6%A4%9C%E5%AE%9A-%E5%8D%98%E8%AA%9E%E3%82%A2%E3%83%97%E3%83%AA/id1672828809",
    "jp.ktg.welfare": "https://apps.apple.com/jp/app/%E7%A4%BE%E4%BC%9A%E7%A6%8F%E7%A5%89%E5%A3%AB%E5%9B%BD%E5%AE%B6%E8%A9%A6%E9%A8%93-%E9%81%8E%E5%8E%BB%E5%95%8F%E3%82%A2%E3%83%97%E3%83%AA-%E7%A4%BE%E4%BC%9A%E7%A6%8F%E7%A5%89%E5%A3%AB%E3%81%AE%E5%8B%89%E5%BC%B7%E3%82%B5%E3%83%9D%E3%83%BC%E3%83%88/id1661528203",
    "jp.ktg.emergency": "https://apps.apple.com/jp/app/%E6%95%91%E6%80%A5%E6%B3%95-%E5%95%8F%E9%A1%8C%E9%9B%86%E3%82%A2%E3%83%97%E3%83%AA/id6444561136",
    "jp.ktg.fee": "https://apps.apple.com/jp/app/%E5%9F%BA%E6%9C%AC%E6%83%85%E5%A0%B1%E6%8A%80%E8%A1%93%E8%80%85%E8%A9%A6%E9%A8%93-%E9%81%8E%E5%8E%BB%E5%95%8F%E9%9B%86-%E5%9F%BA%E6%9C%AC%E6%83%85%E5%A0%B1%E3%81%AE%E9%81%8E%E5%8E%BB%E5%95%8F%E3%82%92%E5%AD%A6%E7%BF%92/id6449242419",
    "jp.ktg.ape": "https://apps.apple.com/jp/app/%E5%BF%9C%E7%94%A8%E6%83%85%E5%A0%B1%E6%8A%80%E8%A1%93%E8%80%85%E8%A9%A6%E9%A8%93-%E9%81%8E%E5%8E%BB%E5%95%8F%E9%9B%86-%E5%BF%9C%E7%94%A8%E6%83%85%E5%A0%B1%E3%81%AE%E9%81%8E%E5%8E%BB%E5%95%8F%E3%82%92%E5%AD%A6%E7%BF%92/id6449149030",
    "jp.ktg.dbe": "https://apps.apple.com/jp/app/%E3%83%87%E3%83%BC%E3%82%BF%E3%83%99%E3%83%BC%E3%82%B9%E3%82%B9%E3%83%9A%E3%82%B7%E3%83%A3%E3%83%AA%E3%82%B9%E3%83%88%E8%A9%A6%E9%A8%93-%E9%81%8E%E5%8E%BB%E5%95%8F%E9%9B%86-db%E3%81%AE%E9%81%8E%E5%8E%BB%E5%95%8F/id6450543673",
    "jp.ktg.onomatopoeia": "https://apps.apple.com/jp/app/%E9%9F%93%E5%9B%BD%E8%AA%9E%E3%82%AA%E3%83%8E%E3%83%9E%E3%83%88%E3%83%9A%E8%BE%9E%E5%85%B8-%E3%83%8F%E3%83%B3%E3%82%B0%E3%83%AB%E3%81%AE%E6%93%AC%E6%85%8B%E8%AA%9E-%E6%93%AC%E9%9F%B3%E8%AA%9E%E3%82%92%E7%A2%BA%E8%AA%8D/id6449489898",
    "jp.ktg.ecotextbook": "https://apps.apple.com/jp/app/eco%E6%A4%9C%E5%AE%9A-%E9%87%8D%E8%A6%81%E8%AA%9E%E5%8F%A5%E3%82%A2%E3%83%97%E3%83%AA-%E3%82%A8%E3%82%B3%E6%A4%9C%E5%AE%9A-%E7%92%B0%E5%A2%83%E7%A4%BE%E4%BC%9A%E6%A4%9C%E5%AE%9A%E8%A9%A6%E9%A8%93/id6449150376",
    "jp.ktg.howtogpt": "https://apps.apple.com/jp/app/%E3%83%81%E3%83%A3%E3%83%83%E3%83%88gpt-%E6%B4%BB%E7%94%A8%E3%83%86%E3%82%AF%E3%83%8B%E3%83%83%E3%82%AF-how-to-%E3%83%81%E3%83%A3%E3%83%83%E3%83%88gpt/id6453687547",
    "jp.ktg.hsk.paid": "https://apps.apple.com/jp/app/hsk-%E9%A0%BB%E5%87%BA%E5%8D%98%E8%AA%9E%E5%AD%A6%E7%BF%92%E3%82%A2%E3%83%97%E3%83%AA-%E4%B8%AD%E5%9B%BD%E8%AA%9E%E6%A4%9C%E5%AE%9A-%E6%BC%A2%E8%AA%9E%E6%B0%B4%E5%B9%B3%E8%80%83%E8%A9%A6/id1632517752",
    "jp.ktg.nursing": "https://apps.apple.com/jp/app/%E4%BB%8B%E8%AD%B7%E7%A6%8F%E7%A5%89%E6%A4%9C%E5%AE%9A-%E9%81%8E%E5%8E%BB%E5%95%8F%E3%82%A2%E3%83%97%E3%83%AA-%E4%BB%8B%E8%AD%B7%E7%A6%8F%E7%A5%89%E5%A3%AB%E3%81%AE%E5%8B%89%E5%BC%B7%E3%82%B5%E3%83%9D%E3%83%BC%E3%83%88/id1659255992",
    "jp.ktg.fp3": "https://apps.apple.com/jp/app/fp3%E7%B4%9A-%E9%81%8E%E5%8E%BB%E5%95%8F%E3%82%A2%E3%83%97%E3%83%AA/id6473820711",
    "jp.ktg.housecompare": "https://apps.apple.com/jp/app/%E4%BD%8F%E5%AE%85%E7%89%A9%E4%BB%B6%E6%AF%94%E8%BC%83-%E9%83%A8%E5%B1%8B%E6%8E%A2%E3%81%97-%E3%81%8A%E5%AE%B6%E6%8E%A2%E3%81%97%E3%82%92%E3%82%B5%E3%83%9D%E3%83%BC%E3%83%88-%E4%B8%AD%E5%8F%A4%E6%96%B0%E7%AF%89%E5%AF%BE%E5%BF%9C/id6742167699",
    "jp.ktg.carpare": "https://apps.apple.com/jp/app/%E8%BB%8A%E6%AF%94%E8%BC%83-%E8%BB%8A%E3%81%95%E3%81%8C%E3%81%97%E3%82%92%E3%82%B5%E3%83%9D%E3%83%BC%E3%83%88-%E6%96%B0%E8%BB%8A-%E4%B8%AD%E5%8F%A4%E8%BB%8A%E5%AF%BE%E5%BF%9C/id6743841144",
}

def get_app_details(app_url):
    response = requests.get(app_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    app_name = soup.find("h1").text

    about_section = soup.find("div", {"class": "bARER"})
    for br in about_section.select("br"):
        br.replace_with('\n  ')
    description = about_section.get_text() if about_section else ""
    icon_url = soup.find("img", {"class": "T75of"})["src"]
    # print(icon_url)

    capture_urls = []
    for capture in soup.select(".qwPPwf img"):
        capture_urls.append(capture.attrs['src'].replace("w526-h296-rw", "w1052-h592-rw"))

    return {
        "name": app_name,
        "description": description,
        "icon_url": icon_url,
        "capture_urls": capture_urls,
    }

def main():
    with open("scripts/source.txt", "r", encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")

    app_urls = []
    feature_image_urls = []
    # for a in soup.find_all("a", href=True):
    #     if a["href"].startswith("/store/apps/details?id="):
    #         app_urls.append(f"https://play.google.com{a['href']}")

    for app_div in soup.select(".ULeU3b"):
        print(app_div.select_one('a').attrs['href'])
        app_urls.append(f"https://play.google.com{app_div.select_one('a').attrs['href']}")
        # print(app_div.select_one('.T75of').attrs['src'])
        feature_image_urls.append(app_div.select_one('.T75of').attrs['src'].replace("w416-h235", "w832-h470"))

    print(f"len(app_urls): {len(app_urls)}, len(feature_image_urls): {len(feature_image_urls)}")

    if len(app_urls) != len(feature_image_urls):
        print("Something Wrong.")
        print(f"len(app_urls): {len(app_urls)}, len(feature_image_urls): {len(feature_image_urls)}")
        exit(1)

    # Remove duplicates
    # app_urls = sorted(list(set(app_urls)))

    for app_url_index, url in enumerate(app_urls):
        print(f"Scraping {url}")
        app_id = url.split("id=")[1]
        # if app_id != "":
        #     continue
        ios_url = ios_urls.get(app_id)
        if not ios_url:
            print(f"iOS URL Not set [{app_id}]")
        
        app_id_hyphenated = app_id.replace(".", "-")
        details = get_app_details(url)

        # Create markdown file
        content_dir = f"src/content/apps"
        os.makedirs(content_dir, exist_ok=True)
        with open(f"{content_dir}/{app_id_hyphenated}.md", "w") as f:
            f.write(f"---\n")
            f.write(f"title: {details['name']}\n")
            f.write(f"description: |-\n  ")
            f.write(f"{details['description']}\n")
            f.write(f'icon: "@assets/apps/{app_id_hyphenated}/icon.webp"\n')
            f.write(f'image: "@assets/apps/{app_id_hyphenated}/vis.webp"\n')
            if ios_url:
                f.write(f"appStoreUrl: {ios_url}\n")
            f.write(f"playStoreUrl: {url}\n")
            f.write("screenShots:\n")
            for capture_url_index, _ in enumerate(details["capture_urls"]):
                f.write(f'  - "@assets/apps/{app_id_hyphenated}/ss{str(capture_url_index).zfill(2)}.webp"\n')
            f.write(f"---\n\n")

        # Download images
        assets_dir = f"src/assets/apps/{app_id_hyphenated}"
        os.makedirs(assets_dir, exist_ok=True)

        # Icon
        icon_response = requests.get(details["icon_url"], headers=headers)
        with open(f"{assets_dir}/icon.webp", "wb") as f:
            f.write(icon_response.content)
        
        vis_response = requests.get(feature_image_urls[app_url_index], headers=headers)
        with open(f"{assets_dir}/vis.webp", "wb") as f:
            f.write(vis_response.content)

        # Capture
        for capture_url_index, capture_url in enumerate(details["capture_urls"]):
            capture_response = requests.get(capture_url, headers=headers)
            with open(f"{assets_dir}/ss{str(capture_url_index).zfill(2)}.webp", "wb") as f:
                f.write(capture_response.content)
        # break


if __name__ == "__main__":
    main()

