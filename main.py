import io
import json
import time
from glob import glob
import openpyxl as opx
import pandas as pd
import os
from tqdm import tqdm

import spark_parse


if __name__ == '__main__':
    a = spark_parse.Spark()
    N = len(glob('data/*'))
    print(N)
    names = ['cash_flow_statement',
             'financial_report',
             'balance_sheet',
             'rosstat_report',
             'fns_report']

    inn_list = pd.read_csv('Org2_filtr_by_income.csv', usecols=['inn'])['inn']
    inn_list = pd.unique(inn_list)[::-1]

    for inn in tqdm(inn_list[N:]):
        try:
            if os.path.isdir(f'data/{inn}'):
                pass
            else:
                os.mkdir(f'data/{inn}')

            # time.sleep(0.5)
            a.company_inn = inn

            try:
                resp = a.get_xlsx()
                if resp is not None:
                    xlsx = opx.load_workbook(io.BytesIO(resp))
                    xlsx.save(f'data/{inn}/{inn}_report.xlsx')
                else:
                    cfs = a.get_cash_flow()
                    fin = a.get_fin_report()
                    bs = a.get_balance_report()
                    rst, fns = a.accountant_report()
                    data = [cfs, fin, bs, rst, fns]

                    for i in range(len(names)):
                        with open(f'data/{inn}/{names[i]}.json', 'w', encoding='utf-8') as f:
                            json.dump(data[i], f, ensure_ascii=False, indent=4)

            except IndexError:
                with open('index_error.txt', 'a') as file:
                    file.write(f'{inn}\n')

        except Exception as e:
            print(f'Exception: {str(e)}')
            time.sleep(240)

