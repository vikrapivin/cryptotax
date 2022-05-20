import pandas as pd
import numpy as np

# take orders and for each sell exhaust the first in component to find the basis
# returns an array with the amounts exhausted that are exhausted
# assumes that orders are ordered in time
# 'FIFO Exhausted' amount of the Buy that has been sold
def firstInFirstOut(self):
    for crypto in self.combined_ords:
        (sellBasis, self.combined_ords[crypto]) = firstInFirstOutCrypto(self, self.combined_ords[crypto])
        self.taxable_sells[crypto] = sellBasis
    return self.taxable_sells
def firstInFirstOutCrypto(self, orders):
    orders = pd.DataFrame.copy(orders)
    if 'FIFO Exhausted' in orders.columns:
        pass
    else:
        orders['FIFO Exhausted'] = 0
    # move these two indices in order to determine the basis
    buyIndex = 0
    sellIndex = 0
    numOrders = orders.shape[0]
    # break out once sells are done, I guess this could be a for loop, but this seems cleaner...
    sellBasis = []
    while(sellIndex < numOrders):
        curOrder = orders.iloc[sellIndex]
        if curOrder['Transaction Type'] != 'Sell':
            sellIndex = sellIndex + 1
            continue
        else:
            amountToGet = curOrder['Quantity Transacted']
            # flag to make sure all our sells have a basis in the buys
            allSellsCovered = True
            sellBasisEntry = {}
            sellBasisEntry['Time Sold'] = curOrder['Timestamp']
            sellBasisEntry['Amount Sold'] = amountToGet
            sellBasisEntry['Amount USD Obtained'] = curOrder['USD Total (inclusive of fees)']
            sellBasisEntry['Basis'] = []
            # exhaust the buys one by one starting with the first one
            # this should be a separate function
            for ii in range(buyIndex, sellIndex):
                quantityAvailable = orders.loc[ii,('Quantity Transacted')] - orders.loc[ii,('FIFO Exhausted')]
                if quantityAvailable > amountToGet:
                    orders.loc[ii,('FIFO Exhausted')] = orders.loc[ii,('FIFO Exhausted')] + amountToGet
                    sellBasisEntry['Basis'].append([amountToGet, orders.loc[ii,('Timestamp')],orders.loc[ii,('Quantity Transacted')], orders.loc[ii,('USD Total (inclusive of fees)')]])
                    allSellsCovered = True
                    break
                else:
                    orders.loc[ii,('FIFO Exhausted')] = orders.loc[ii,('FIFO Exhausted')] + quantityAvailable
                    buyIndex = buyIndex + 1
                    sellBasisEntry['Basis'].append([quantityAvailable, orders.loc[ii,('Timestamp')], orders.loc[ii,('Quantity Transacted')], orders.loc[ii,('USD Total (inclusive of fees)')]])
                    amountToGet = amountToGet - quantityAvailable
            if allSellsCovered is False:
                raise ValueError('Sells have not been covered by buys. You must have acquired more coins somewhere else.')
            # this can be a separate function as well
            totalBasis = 0
            for entry in sellBasisEntry['Basis']:
                fractionCost = entry[0]/entry[2]*entry[3]
                totalBasis = totalBasis+fractionCost
            sellBasisEntry['Cost Basis'] = totalBasis
            sellBasis.append(sellBasisEntry)
            sellIndex = sellIndex + 1
    return (sellBasis, orders)