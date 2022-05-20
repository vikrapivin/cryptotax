import pandas as pd
import numpy as np

# parse orders in coinbase assuming USD as currency
def read_cb_pro_csv(self, filename):
    cb_pro_data = pd.read_csv(filename,sep=',',skip_blank_lines=False,header=0)
    orders = {}
    for index, row in cb_pro_data.iterrows():
        if pd.isna(row['time']):
            continue
        try:
            orders[row['time']].append(row)
        except KeyError:
            orders[row['time']] = []
            orders[row['time']].append(row) 
    orders_dict = {}
    for order in orders:
        orders_dict[order] = pd.DataFrame(orders[order])
    parsed_orders = {}
    for order in orders_dict:
        initial_parse = {}
        for index, row in orders_dict[order].iterrows():
            try:
                initial_parse[row['amount/balance unit']][row['type']] = row['amount']
            except KeyError:
                initial_parse[row['amount/balance unit']] = {}
                initial_parse[row['amount/balance unit']][row['type']] = row['amount']
        if 'USD' in initial_parse and 'match' in initial_parse['USD']:
            buyOrder = False
            if initial_parse['USD']['match'] < 0:
                buyOrder = True
            keysindict = list(initial_parse.keys())
            keysindict.remove('USD')
            transactedCurrency = keysindict[0]
            structuredOrder = [order, 'Buy' if buyOrder else 'Sell', 
                np.abs(initial_parse['USD']['match']+initial_parse['USD']['fee']), 
                np.abs(initial_parse[transactedCurrency]['match'])] # order date, buy/sell, amount usd, amount crypto
            try:
                parsed_orders[transactedCurrency].append(structuredOrder)
            except KeyError:
                parsed_orders[transactedCurrency] = []
                parsed_orders[transactedCurrency].append(structuredOrder)
        else:
            continue
    for crypto in parsed_orders:
        parsed_orders[crypto] = pd.DataFrame(parsed_orders[crypto],columns=['Timestamp','Transaction Type','USD Total (inclusive of fees)', 'Quantity Transacted'])
        self.add_orders(parsed_orders[crypto],crypto_type=crypto)
    return
