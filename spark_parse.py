from functools import cached_property, lru_cache
import atexit
import requests
import warnings

warnings.simplefilter("ignore")


class Spark:
    __slots__ = ('company_inn', 'sess')

    def __init__(self):
        """
                Initialize the Caiso object with a session and nodename and login .

                :param sess: Requests session object (optional)
                :type sess: requests.Session, optional
                :param nodename: Name of the node (optional)
                :type nodename: str, optional

        """
        self.company_inn = None
        atexit.register(self.logout)
        self.sess = requests.Session()
        login_response = self.sess.post('https://spark-interfax.ru/system/sapi/auth/credentials?format=json&s_up=ssl',
                                        files={'UserName': (None, 'skoltech8'), 'Password': (None, 'dEB-hF9-Kzu-W37'),
                                               'RememberMe': (None, 'true')}, verify=False)
        print(login_response.json())
        # todo captcha recognition
        # if login_response.status_code == 401:
        #     print('captcha needed')
        #
        #
        #     captcha = self.sess.get('https://spark-interfax.ru/sapi/captcha?format=json', verify=False)
        #     text_captcha = captcha.json()['Text']
        #     img_captcha = captcha.json()['Image']
        # raise requests.exceptions.HTTPError(login_response.json()['ResponseStatus']['Message'])
        if login_response.status_code != 200:
            raise requests.exceptions.HTTPError(login_response.json()['ResponseStatus']['Message'])

    # def capcha(self):
    #
    # Captcha =nkr0+2qaZhnAAz1v9lJPDMlAfMp+RUNw
    # UserCaptcha = 33n49b3i

    @lru_cache(32)
    def get_guid(self, inn) -> str:
        """Поиск и выборка  comapny GUID
         :return: company GUID"""
        resp = self.sess.get(
            f'https://spark-interfax.ru/sapi/companylist/autocomplete/?'
            f'query={inn}&type=Unknown&Country=RUS', verify=False)
        print('get guid')
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return f"Error: {e}"
        return resp.json()[0]['DirectLink']['Guid']

    # 7710699964 CDF0F6BA74A94D8EBD174BD9C10B8491
    def get_company_info(self) -> str:
        """Краткое инфо о компании
            :return: json object"""
        resp = self.sess.get(
            f'https://spark-interfax.ru/sapi/company?CompanyKey={{CompanyGuid:{self.get_guid(self.company_inn)}}}',
            verify=False)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return f"Error: {e}"
        return resp.json()

    def get_fin_report(self) -> str:
        """Отчет о финансовых результатах
             :return: json object"""
        resp = self.sess.get(
            f"https://spark-interfax.ru/sapi/databalance?CompanyKey={{CompanyGuid:{self.get_guid(self.company_inn)}}}&"
            "StatementType=Form2&CurrencyType=RUB&Multiplier=1")
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return f"Error: {e}"
        return resp.json()

    def get_balance_report(self)->str:
        """ Баланс
         :return: json object"""
        resp = self.sess.get(
            "https://spark-interfax.ru/sapi/databalance?CompanyKey=%7BCompanyGuid%3ACDF0F6BA74A94D8EBD174BD9C10B8491%7D&"
            "StatementType=Form1&CurrencyType=RUB&Multiplier=1")
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return f"Error: {e}"
        return resp.json()

    def get_cash_flow(self)->str:
        """Отчет о движении денежных средств
         :return: json object"""
        resp = self.sess.get(
            "https://spark-interfax.ru/sapi/databalance?CompanyKey=%7BCompanyGuid%3ACDF0F6BA74A94D8EBD174BD9C10B8491%7D&"
            "StatementType=Form4&CurrencyType=RUB&Multiplier=1")
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return f"Error: {e}"
        return resp.json()

    def get_xlsx(self) -> str | bytes:
        """Отчет о финансах в формате xlsx, включает в себя Отчет о движении денежных средств,баланс,
        Отчет о финансовых результатах
        :return: bytes object"""
        report_id = self.sess.post("https://spark-interfax.ru/sapi/sourcedata/export/xlsx",
                                   json={"CompanyKey": {"CompanyGuid": {self.get_guid(self.company_inn)}},
                                         "CurrencyType": "RUB", "Scale": 1}).json()['ReportId']
        report_file = self.sess.get(f'https://spark-interfax.ru/sapi/reporting/report?ReportId={report_id}', timeout=30)
        try:
            report_id.raise_for_status()
            report_file.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return f"Error: {e}"
        return report_file.content

    def accountant_report(self) -> [str, str]:
        """Бухгалтерская отчетность
         :return: tuple of отчет росстата, отчет фнс"""

        rosstat_report = self.sess.get("https://spark-interfax.ru/sapi/financialreports/periods?"
                                       f"CompanyKey=%7BCompanyGuid%3A{self.get_guid(self.company_inn)}%7D")
        fns_report = self.sess.get("https://spark-interfax.ru/sapi/financialreports?SourceId=Fns&PeriodId=555&"
                                   f"CompanyKey=%7BCompanyGuid%3A{self.get_guid(self.company_inn)}%7D&ReportType=None")
        return rosstat_report.json(), fns_report.json()

    def logout(self) -> None:
        """logout"""
        print('logout')
        self.sess.post('https://spark-interfax.ru/sapi/auth/logout?continue=/', verify=False)

    # TODO неуверенный поиск
    # https://spark-interfax.ru/system/sapi/companylist/search?&pageSize=30&pageNo=1&query=
    # {"Unknown":"сбер"}&type=Unknown&filter={Country:RUS,OkvedCodes:[],CompanySize:Unknown,RegionCodes:[],
    # IsActual:Any,EntityType:Any}&bounds=&documentType=None&ObjectType=Search