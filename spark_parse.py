from __future__ import annotations

import base64
import io
from functools import cached_property, lru_cache
import atexit
from typing import Any

import requests
import warnings
from PIL import Image

warnings.simplefilter("ignore")


class Spark:
    __slots__ = ("__username", "__password", "company_inn", "sess")

    def __init__(self):
        """
                Initialize the spark object with a session and pass and login .
        """
        self.__username = 'skoltech8'
        self.__password = 'dEB-hF9-Kzu-W37'
        self.company_inn = None
        atexit.register(self.logout)
        self.sess = requests.Session()

        login_response = self.__login()
        if login_response.status_code == 401:
            print('captcha needed')
            text_captcha, img_text = self.__captcha()
            self.__login(text_captcha, img_text)
        if (login_response.status_code != 200) and (login_response.status_code != 401):
            raise requests.exceptions.HTTPError(login_response.json()['ResponseStatus']['Message'])

    def __login(self, captcha='', user_captcha=''):
        login_response = self.sess.post('https://spark-interfax.ru/system/sapi/auth/credentials?format=json&s_up=ssl',
                                        files={'UserName': (None, 'skoltech8'), 'Password': (None, 'dEB-hF9-Kzu-W37'),
                                               'RememberMe': (None, 'false'), 'Captcha': (None, captcha),
                                               'UserCaptcha': (None, user_captcha)}, verify=False)

        return login_response

    def __captcha(self):

        try:
            captcha = self.sess.get('https://spark-interfax.ru/sapi/captcha?format=json', verify=False)
            captcha.raise_for_status()
            text_captcha = captcha.json()['Text']
            img_captcha = io.BytesIO(base64.b64decode(captcha.json()['Image']))

            im = Image.open(img_captcha)
            im.show()
            img_text = input('input captcha text here: ')
            im.close()
            return text_captcha, img_text
        except requests.exceptions.HTTPError as e:
            raise f"Error: {e}"

    @lru_cache(32)
    def get_guid(self, inn) -> str:
        """Поиск и выборка  comapny GUID
         :return: company GUID"""

        try:
            resp = self.sess.get(
                f'https://spark-interfax.ru/sapi/companylist/autocomplete/?'
                f'query={inn}&type=Unknown&Country=RUS', verify=False)
            print('get guid')

            resp.raise_for_status()
            return resp.json()[0]['DirectLink']['Guid']
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Error: {e}")


    # 7710699964 CDF0F6BA74A94D8EBD174BD9C10B8491
    def get_company_info(self) -> str:
        """Краткое инфо о компании
            :return: json object"""

        try:
            resp = self.sess.get(
                f'https://spark-interfax.ru/sapi/company?CompanyKey={{CompanyGuid:{self.get_guid(self.company_inn)}}}',
                verify=False)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Error: {e}")


    def get_fin_report(self) -> Any | None:
        """Отчет о финансовых результатах
             :return: json object"""
        resp = self.sess.get(
            f"https://spark-interfax.ru/sapi/databalance?CompanyKey={{CompanyGuid:{self.get_guid(self.company_inn)}}}&"
            "StatementType=Form2&CurrencyType=RUB&Multiplier=1")
        try:
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            return None


    def get_balance_report(self) -> Any | None:
        """ Баланс
         :return: json object"""
        try:
            resp = self.sess.get(
                f"https://spark-interfax.ru/sapi/databalance?CompanyKey=%7BCompanyGuid%3A{self.get_guid(self.company_inn)}%7D&"
                "StatementType=Form1&CurrencyType=RUB&Multiplier=1")

            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            return None


    def get_cash_flow(self) -> Any | None:
        """Отчет о движении денежных средств
         :return: json object"""
        try:
            resp = self.sess.get(
                f"https://spark-interfax.ru/sapi/databalance?CompanyKey=%7BCompanyGuid%3A{self.get_guid(self.company_inn)}%7D&"
                "StatementType=Form4&CurrencyType=RUB&Multiplier=1")

            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            return None

    def get_xlsx(self) -> str | bytes | None:
        """Отчет о финансах в формате xlsx, включает в себя Отчет о движении денежных средств,баланс,
        Отчет о финансовых результатах
        :return: bytes object"""
        try:
            report_id = self.sess.post("https://spark-interfax.ru/sapi/sourcedata/export/xlsx",
                                       json={"CompanyKey": {"CompanyGuid": f"{self.get_guid(self.company_inn)}"},
                                             "CurrencyType": "RUB", "Scale": 1})
            print(report_id)
            report_file = self.sess.get(f'https://spark-interfax.ru/sapi/reporting/report?ReportId='
                                        f'{report_id.json()["ReportId"]}', timeout=30)

            report_id.raise_for_status()
            report_file.raise_for_status()
            return report_file.content
        except requests.exceptions.HTTPError as e:
            print(Exception(f"Error (xlsx): {e}"))
            if '500' in str(e):
                with open('old_logs/error500.txt', 'a') as file:
                    file.write(f'{self.company_inn}\n')
            return None



    def accountant_report(self) -> [str, str]:
        """Бухгалтерская отчетность
         :return: tuple of отчет росстата, отчет фнс"""
        try:
            rosstat_report = self.sess.get("https://spark-interfax.ru/sapi/financialreports/periods?"
                                           f"CompanyKey=%7BCompanyGuid%3A{self.get_guid(self.company_inn)}%7D")
            fns_report = self.sess.get("https://spark-interfax.ru/sapi/financialreports?SourceId=Fns&PeriodId=555&"
                                       f"CompanyKey=%7BCompanyGuid%3A{self.get_guid(self.company_inn)}%7D&ReportType=None")
            return rosstat_report.json(), fns_report.json()
        except Exception as e:
            print(f"Error: {e}")
            return None

    def logout(self) -> None:
        """logout"""
        print('logout')
        self.sess.post('https://spark-interfax.ru/sapi/auth/logout?continue=/', verify=False)

    # fixme returns none
    def get_shareholders(self) -> Any | None:
        """Учредители (участники)
         Returns: json object"""
        try:
            shareholders = self.sess.get(
                f"https://spark-interfax.ru/sapi/card/shareholders/egrul/current?CompanyKey="
                f"%7BCompanyGuid%3A{self.get_guid(self.company_inn)}%7D")
            shareholders.raise_for_status()
            return shareholders.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            return None


    # TODO cвязи
    # https://spark-interfax.ru/system/sapi/graph/s3/OwnershipAnalysis?jsconfig=eccn%2Ceti
    # TODO неуверенный поиск
    # https://spark-interfax.ru/system/sapi/companylist/search?&pageSize=30&pageNo=1&query=
    # {"Unknown":"сбер"}&type=Unknown&filter={Country:RUS,OkvedCodes:[],CompanySize:Unknown,RegionCodes:[],
    # IsActual:Any,EntityType:Any}&bounds=&documentType=None&ObjectType=Search
