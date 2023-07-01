import io
import json
import openpyxl as opx
import pandas as pd

import spark_parse

def get_guid(inn):
    return  inn

if __name__ == '__main__':
    # example
    a = spark_parse.Spark()
    # inn_list = [7707083893,5032339290,9731092941,7706107510]
    # for inn in inn_list:
    #     a.company_inn = inn
    #     print(a.get_cash_flow())
    #     print(a.get_fin_report())
    #     print(a.get_balance_report())
    #     print(a.accountant_report())
    #     #df = pd.read_excel( a.get_xlsx())
    #     #print(df.head(10))

    a.company_inn =9731092941
    guid = a.get_guid(a.company_inn)
    print(guid)
    print(a.get_owners(guid))


