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
    inn_list = [7707083893]
    for inn in inn_list:
        a.company_inn = inn

        print(a.accountant_report())
        #df = pd.read_excel( a.get_xlsx())
        #print(df.head(10))
        print(a.get_shareholders())
