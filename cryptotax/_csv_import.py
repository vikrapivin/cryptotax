import pandas as pd
import numpy as np
# import csv defined by the standard from other software.
def import_custom_csv_trades(self, filename, crypto_type='BTC'):
    try:
        readin = pd.read_csv(filename,index_col=0)
        readin['Timestamp']=pd.to_datetime(readin['Timestamp'])
        self.add_orders(readin,crypto_type=crypto_type)
    except FileNotFoundError:
        print('File: ' + filename + ' does not exist.')
        