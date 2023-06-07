from functools import cached_property, lru_cache
import atexit

import requests


class Spark:
    def __init__(self):
        """login"""
        self.sess = requests.Session()
        login_response = self.sess.post('https://spark-interfax.ru/system/sapi/auth/credentials?format=json&s_up=ssl',
                                        files={'UserName': (None, 'skoltech8'), 'Password': (None, 'dEB-hF9-Kzu-W37'),
                                               'RememberMe': (None, 'true')}, verify=False)

        if login_response.status_code == 401:
            captcha = self.sess.get('https://spark-interfax.ru/sapi/captcha?format=json', verify=False)
            text_captcha = captcha.json()['Text']
            img_captcha = captcha.json()['Image']
        print(login_response.text)
        self.company_inn = None
        atexit.register(self.logout)

    # def capcha(self):
    #
    # Captcha =nkr0+2qaZhnAAz1v9lJPDMlAfMp+RUNw
    # UserCaptcha = 33n49b3i

    @lru_cache(32)
    def get_guid(self, inn) -> str:
        """Поиск и выборка  comapny GUID
         Returns: company GUID"""
        resp = self.sess.get(
            f'https://spark-interfax.ru/sapi/companylist/autocomplete/?'
            f'query={inn}&type=Unknown&Country=RUS', verify=False)
        print('get guid')
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return "Error: " + str(e)
        return resp.json()[0]['DirectLink']['Guid']

    # 7710699964 CDF0F6BA74A94D8EBD174BD9C10B8491
    def get_company_info(self) -> str:
        """Краткое инфо о компании
            Returns: json object"""
        resp = self.sess.get(
            f'https://spark-interfax.ru/sapi/company?CompanyKey={{CompanyGuid:{self.get_guid(self.company_inn)}}}',
            verify=False)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return "Error: " + str(e)
        return resp.json()

    def get_fin_res(self) -> str:
        """Отчет о финансовых результатах
             Returns: json object"""
        resp = self.sess.get(
            f"https://spark-interfax.ru/sapi/databalance?CompanyKey={{CompanyGuid:{self.get_guid(self.company_inn)}}}&"
            "StatementType=Form2&CurrencyType=RUB&Multiplier=1")
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return "Error: " + str(e)
        return resp.json()

    def get_xlsx(self) -> str | bytes:
        """Отчет о финансах в формате xlsx
        Returns: json object"""
        report_id = self.sess.post("https://spark-interfax.ru/sapi/sourcedata/export/xlsx",
                                   json={"CompanyKey": {"CompanyGuid": {self.get_guid(self.company_inn)}},
                                         "CurrencyType": "RUB", "Scale": 1}).json()['ReportId']
        report_file = self.sess.get(f'https://spark-interfax.ru/sapi/reporting/report?ReportId={report_id}', timeout=30)
        try:
            report_id.raise_for_status()
            report_file.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return "Error: " + str(e)
        return report_file.content

    def logout(self) -> None:
        """logout"""
        print('logout')
        self.sess.post('https://spark-interfax.ru/sapi/auth/logout?continue=/', verify=False)