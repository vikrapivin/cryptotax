import numpy as np
import pandas as pd
import cryptotax as ct

taxes = ct.cryptotax()
taxes.read_cb_pro_csv('cb_pro.csv')
taxes.read_cb_csv('cb.csv')
# print(taxes.combined_ords['ETH'])
taxes.import_custom_csv_trades('custom_BCH.csv',crypto_type='BCH')
taxable_sells = taxes.firstInFirstOut()
# print(taxes.combined_ords['ETH'])
for crypto in taxable_sells:
    for sell in taxable_sells[crypto]:
        print(f'For {sell["Amount Sold"]} {crypto} sale for ' +
            f'${round(sell["Amount USD Obtained"]*100)/100} at {sell["Time Sold"]} report cost basis as {round(100*sell["Cost Basis"])/100}\n')
