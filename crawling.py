# 사용할 라이브러리 import
from flask import Flask, request
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
    meal = pd.read_html(html)[0]

    return meal


def parse_to_json(pd):
    pd.index = ["점심", "저녁"]
    pd.columns = [column[3:-1] for column in pd.columns]
    res = pd.to_json(orient='columns').encode('utf8')
    parsed = json.loads(res, encoding="utf-8")
    return parsed


def get_meal_json(dorm_name):
    meal = get_meal(dorm_name)
    if meal.empty:
        return {"text": "식단 데이터가 존재하지 않습니다."}
    json = parse_to_json(meal)
    return json


app = Flask(__name__)


@app.route("/meals")
def meal():
    name = request.args.get('name')

    if name == "pu":
        return get_meal_json("푸름관")
    elif name == "oh1":
        return get_meal_json("오름관1동")
    elif name == "oh3":
        return get_meal_json("오름관3동")


if __name__ == "__main__":
    app.run()
