import requests
import  spark_parse





"""Value": null,
        "Type": "None",
        "IsExact": false,
        "DirectLink": {
            "SparkId": null,
            "Inn": null,
            "Edrpou": null,
            "Ogrn": null,
            "Okpo": null,
            "NameInRus": "РКСС, ЗАО",
            "Rnn": null,
            "Unp": null,
            "RegNumber": null,
            "Snils": null,
            "Codes": [
                {
                    "Name": "ИНН",
                    "Value": "<b>7710699964</b>"
                }
            ],
            "Guid": "CDF0F6BA74A94D8EBD174BD9C10B8491",
            "RegionName": "Москва",
            "EntityType": "Company"
        },
        "ValueForHistory": "РКСС, ЗАО <b>7710699964</b>"
    }
]"""
"""company short info"""
# resp = sess.get('https://spark-interfax.ru/sapi/company?CompanyKey={CompanyGuid:CDF0F6BA74A94D8EBD174BD9C10B8491}')
# print(resp.text)
# """Отчет о финансовых результатах"""
# resp = sess.get("https://spark-interfax.ru/sapi/databalance?CompanyKey={CompanyGuid:CDF0F6BA74A94D8EBD174BD9C10B8491}&"
#                 "StatementType=Form2&CurrencyType=RUB&Multiplier=1")
# print(resp.text)
# """Баланс"""
# resp = sess.get(
#     "https://spark-interfax.ru/sapi/databalance?CompanyKey=%7BCompanyGuid%3ACDF0F6BA74A94D8EBD174BD9C10B8491%7D&"
#     "StatementType=Form1&CurrencyType=RUB&Multiplier=1")
# print(resp.text)
# """Отчет о движении денежных средств"""
# resp = sess.get(
#     "https://spark-interfax.ru/sapi/databalance?CompanyKey=%7BCompanyGuid%3ACDF0F6BA74A94D8EBD174BD9C10B8491%7D&"
#     "StatementType=Form4&CurrencyType=RUB&Multiplier=1")
# print(resp.text)
# """Бухгалтерская отчетность"""
#
# resp = sess.get("https://spark-interfax.ru/sapi/financialreports/periods?"
#                 "CompanyKey=%7BCompanyGuid%3ACDF0F6BA74A94D8EBD174BD9C10B8491%7D")
# print(resp.text)
# resp = sess.get("https://spark-interfax.ru/sapi/financialreports?SourceId=Fns&PeriodId=555&"
#                 "CompanyKey=%7BCompanyGuid%3ACDF0F6BA74A94D8EBD174BD9C10B8491%7D&ReportType=None")
# print(resp.text)
# """xls"""
# resp = sess.post("https://spark-interfax.ru/sapi/sourcedata/export/xlsx",
#                  json={"CompanyKey":{"CompanyGuid":"CDF0F6BA74A94D8EBD174BD9C10B8491"},"CurrencyType":"RUB","Scale":1})
# report_id=resp.json()['ReportId']
# resp =sess.get(f'https://spark-interfax.ru/sapi/reporting/report?ReportId={report_id}')
# with open("response.xlsx", "wb") as f:
#     f.write(resp.content)
# """logout"""
# requests.post('https://spark-interfax.ru/sapi/auth/logout?continue=/',verify=False)
# TODO неуверенный поиск
# https://spark-interfax.ru/system/sapi/companylist/search?&pageSize=30&pageNo=1&query=
# {"Unknown":"сбер"}&type=Unknown&filter={Country:RUS,OkvedCodes:[],CompanySize:Unknown,RegionCodes:[],
# IsActual:Any,EntityType:Any}&bounds=&documentType=None&ObjectType=Search

#
a=spark_parse.Spark()
a.company_inn=7710699964
#guid= a.get_guid(7710699964)
#print(guid)
a.get_company_info()


#a.company_inn=7707083893
#guid= a.get_guid(7707083893)
#print(guid)
#a.get_company_info()
