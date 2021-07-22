# 사용할 라이브러리 import
from flask import Flask
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import unicodedata
import json
import pandas as pd
import lxml
import re

# 크롤링을 함수로 제작


def get_dorm_code(dorm_name):
    dorm_code = "menu01"

    if dorm_name == "푸름관":
        dorm_code = "menu01"
    elif dorm_name == "오름관1동":
        dorm_code = "menu02"
    elif dorm_name == "오름관3동":
        dorm_code = "menu03"

    return dorm_code


# url를 얻는 함수
def get_dorm_url(dorm_name):
    return "https://dorm.kumoh.ac.kr/dorm/restaurant_" + get_dorm_code(dorm_name) + ".do"


def get_dorm_soup(url):
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, "html.parser")
    return soup.find(attrs={'class': 'board-list01 horizontal-scroll'})


def clean_soup(soup):
    for tag in soup.find_all('p'):
        tag.decompose()

    return str(soup).replace("\n", " ")


def get_meal(dorm_name):
    dorm_url = get_dorm_url(dorm_name)
    soup = get_dorm_soup(dorm_url)
    html = clean_soup(soup)
    res = pd.read_html(html)[0]

    return res


app = Flask(__name__)


@app.route("/푸름관")
def pu():
    return get_meal("푸름관").to_html()


@app.route("/오름관1동")
def oh1():
    return get_meal("오름관1동").to_html()


@app.route("/오름관3동")
def oh3():
    return get_meal("오름관3동").to_html()


if __name__ == "__main__":
    app.run()
