import requests
import json
import os
import re
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

MAIN_DIRECTORY = os.path.dirname(__file__)
CURRENCYS_URL = "https://ru.wikipedia.org/wiki/\
%D0%9E%D0%B1%D1%89%D0%B5%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D0%B9_\
%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D0%BE%D1%80_\
%D0%B2%D0%B0%D0%BB%D1%8E%D1%82"
CRYPTO_CYRRENCYS_URL = "https://ru.wikipedia.org/wiki/\
%D0%9A%D1%80%D0%B8%D0%BF%D1%82%D0%BE%D0%B2%D0%B0%D0%BB%D1%8E%D1%82%D0%B0"
CONVERT_URL = "https://min-api.cryptocompare.com/data/price?\
fsym={0}&tsyms={1}&api_key={2}"


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert_currencys(message, convert_token):
        ua = UserAgent()

        message_text = message.text.strip().split(" ")
        message_text = list(
            map(
                lambda x: x.strip(),
                message_text
            )
        )
        if len(message_text) != 3:
            raise ConvertionException(
                "Ошибка! Кол-во параметров должно быть 3."
            )
        (fsym, tsym, quantity) = message_text
        if fsym == tsym:
            raise ConvertionException(
                "Ошибка! Должны быть указаны разные валюты."
            )
        fsym_result = any(
            list(
                map(
                    lambda x: fsym in x,
                    [
                        CryptoConverter().get_currency_file().keys(),
                        CryptoConverter().get_crypto_currency_file().keys()
                    ]
                )
            )
        )
        tsym_result = any(
            list(
                map(
                    lambda x: tsym in x,
                    [
                        CryptoConverter().get_currency_file().keys(),
                        CryptoConverter().get_crypto_currency_file().keys()
                    ]
                )
            )
        )
        if not(fsym_result and tsym_result):
            raise ConvertionException(f"Ошибка! [{fsym}, {tsym}] Неверный ввод валют(ты).")
        try:
            quantity = float(quantity)
        except Exception as e:
            raise ConvertionException(f"Ошибка! Кол-во должно быть числом.")

        response = requests.get(
            CONVERT_URL.format(
                fsym,
                tsym,
                convert_token
            ),
            headers={'User-Agent': ua.chrome}
        )
        response = json.loads(response.content)
        response =  f"{quantity} [{fsym}] = {float(response[tsym]) * quantity} [{tsym}]"

        return response

    @staticmethod
    def create_currency_file():
        ua = UserAgent()
        response = requests.get(
            CURRENCYS_URL, 
            headers={'User-Agent': ua.chrome}
        )
        page = BeautifulSoup(response.text, 'html.parser')

        tr = page.find_all(
            name="table",
            class_="wikitable sortable"
        )[1].find_all(
            name="tr"
        )

        currencys = {}
        for n, i in enumerate(tr):
            td_list = i.find_all(name="td")

            if n >= 3 and td_list:
                code = td_list[1].text.strip().replace("\n","")
                if code.isdigit():
                    currency_key = td_list[0].text.strip().replace("\n","")
                    currency_key = re.findall(
                        r"^[A-Za-z]+", 
                        currency_key
                    )[0]

                    currency_description = td_list[3].text.strip().replace("\n","")
                    currency_description = re.findall(
                        r"^[A-Za-zА-Яа-я\ \(\)]+", 
                        currency_description
                    )[0]

                    currencys[currency_key] = currency_description
        file_path = os.path.join(MAIN_DIRECTORY, "currencys.txt")
        with open(
            file_path,
            mode="w",
            encoding="utf-8"
        ) as file:
            file.write(
                json.dumps(
                    currencys,
                    indent=4,
                    separators=(",", ": "),
                    ensure_ascii=True
                )
            )

    @staticmethod
    def get_currency_file():
        file_path = os.path.join(MAIN_DIRECTORY, "currencys.txt")
        if os.path.exists(file_path):
            with open(file_path, mode="r") as file:
                data = json.loads(file.read())

            return data

        return False

    @staticmethod
    def create_crypto_currency_file():
        ua = UserAgent()
        response = requests.get(
            CRYPTO_CYRRENCYS_URL, 
            headers={'User-Agent': ua.chrome}
        )
        page = BeautifulSoup(response.text, 'html.parser')

        tr = page.find_all(
            name="table",
            class_="wikitable sortable"
        )[0].find_all(
            name="tr"
        )

        crypto_currencys = {}
        for n, i in enumerate(tr):
            td_list = i.find_all(name="td")

            if n >= 1 and td_list:
                crypto_key = td_list[3].text.strip().replace("\n","")
                crypto_key = re.findall(
                    r"^[A-Z]+",
                    crypto_key
                )
                if crypto_key:
                    crypto_key = crypto_key[0]

                    crypto_currency_description = td_list[2].text.strip().replace("\n","")
                    crypto_currency_description = re.findall(
                        r"^[A-Za-z\ \(\)]+",
                        crypto_currency_description
                    )[0]

                    crypto_currencys[crypto_key] = crypto_currency_description

        file_path = os.path.join(MAIN_DIRECTORY, "crypto_currencys.txt")
        with open("crypto_currencys.txt", mode="w", encoding="utf-8") as file:
            file.write(
                json.dumps(
                    crypto_currencys,
                    indent=4,
                    separators=(",", ": "),
                    ensure_ascii=True
                )
            )

    @staticmethod
    def get_crypto_currency_file():
        file_path = os.path.join(MAIN_DIRECTORY, "crypto_currencys.txt")
        if os.path.exists(file_path):
            with open(file_path, mode="r") as file:
                data = json.loads(file.read())

            return data

        return False
