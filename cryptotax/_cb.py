import pandas as pd
import numpy as np

# filter out other orders than what we care about for now...
def filterOrders(orders):
    return orders[(orders['Transaction Type'] =='Sell') | (orders['Transaction Type'] =='Buy')]

# parse orders in coinbase assuming USD as currency
def read_cb_csv(self, filename):
    cb_data = pd.read_csv(filename,sep=',',skip_blank_lines=False,header=7)
    currencyTransactions = {}
    for index, row in cb_data.iterrows():
        try:
            currencyTransactions[row['Asset']].append(row)
        except KeyError:
            currencyTransactions[str(row['Asset'])] = []
            currencyTransactions[row['Asset']].append(row)
    currency_transactions = {}
    for crypto in currencyTransactions:
        currency_transactions[crypto] = pd.DataFrame(currencyTransactions[crypto])
        currency_transactions[crypto].reset_index(inplace=True,drop=True)
    parsed_orders = {}
    for crypto in currencyTransactions:
        parsed_orders[crypto] = currency_transactions[crypto][['Timestamp',
            'Transaction Type','USD Total (inclusive of fees)', 
            'Quantity Transacted']]
        parsed_orders[crypto] = filterOrders(parsed_orders[crypto])
        self.add_orders(parsed_orders[crypto],crypto_type=crypto)
    return