import pandas as pd
import numpy as np

class cryptotax(object):
    def __init__(self):
        self.combined_ords = {} # placeholder
        self.taxable_sells = {}
        pass

    # Imported methods
    from ._cb_pro import read_cb_pro_csv
    from ._cb import read_cb_csv
    from ._csv_import import import_custom_csv_trades
    from ._fifo import firstInFirstOut

    # save CSV of orders
    # other parameters to be eventually implemented
    def saveCSV(self,filename,crypto_type='BTC'):
        print(f'Saving {crypto_type} orders to {filename}.')
        try:
            self.parsed_orders[crypto_type].to_csv(filename)
        except NameError:
            print(f'No records for {crypto_type} exist from imported trades.')
    def listCryptos(self):
        try:
            return self.combined_ords.keys()
        except AttributeError:
            print(f'You have not imported any cryptos.')
    def add_orders(self, orders,crypto_type='BTC'):
        try:
            add_orders = pd.concat([orders,self.combined_ords[crypto_type]], ignore_index=True)
        except (TypeError, KeyError) as e:
            add_orders=pd.DataFrame.copy(orders)
        add_orders['Timestamp']=pd.to_datetime(add_orders['Timestamp'], utc=True)
        add_orders.sort_values(by=['Timestamp'], inplace=True,ignore_index=True)
        self.combined_ords[crypto_type] = add_orders
    def getSells(orders,crypto_type='BTC'):
        cur_orders = self.combined_ords[crypto_type]
        return cur_orders[cur_orders['Transaction Type'] =='Sell']
