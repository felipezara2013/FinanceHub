from calendars import DayCounts
import pandas as pd
from pandas.tseries.offsets import DateOffset
from bloomberg import BBG

bbg = BBG()

tickers = ['S0023Z 1Y BLC2 Curncy',
          'S0023Z 1D BLC2 Curncy',
          'S0023Z 3M BLC2 Curncy',
          'S0023Z 1W BLC2 Curncy',
          'S0023Z 10Y BLC2 Curncy',
          'S0023Z 1M BLC2 Curncy',
          'S0023Z 2Y BLC2 Curncy',
          'S0023Z 6M BLC2 Curncy',
          'S0023Z 2M BLC2 Curncy',
          'S0023Z 5Y BLC2 Curncy',
          'S0023Z 4M BLC2 Curncy',
          'S0023Z 2D BLC2 Curncy',
          'S0023Z 9M BLC2 Curncy',
          'S0023Z 3Y BLC2 Curncy',
          'S0023Z 4Y BLC2 Curncy',
          'S0023Z 50Y BLC2 Curncy',
          'S0023Z 12Y BLC2 Curncy',
          'S0023Z 18M BLC2 Curncy',
          'S0023Z 7Y BLC2 Curncy',
          'S0023Z 5M BLC2 Curncy',
          'S0023Z 1Y BLC Curncy',
          'S0023Z 6Y BLC2 Curncy',
          'S0023Z 2W BLC2 Curncy',
          'S0023Z 11M BLC2 Curncy',
          'S0023Z 15M BLC2 Curncy',
          'S0023Z 21M BLC2 Curncy',
          'S0023Z 15Y BLC2 Curncy',
          'S0023Z 25Y BLC2 Curncy',
          'S0023Z 8Y BLC2 Curncy',
          'S0023Z 10M BLC2 Curncy',
          'S0023Z 1D BLC Curncy',
          'S0023Z 20Y BLC2 Curncy',
          'S0023Z 33M BLC2 Curncy',
          'S0023Z 7M BLC2 Curncy',
          'S0023Z 8M BLC2 Curncy',
          'S0023Z 11Y BLC2 Curncy',
          'S0023Z 14Y BLC2 Curncy',
          'S0023Z 18Y BLC2 Curncy',
          'S0023Z 19Y BLC2 Curncy',
          'S0023Z 23D BLC2 Curncy',
          'S0023Z 9Y BLC2 Curncy',
          'S0023Z 10Y BLC Curncy',
          'S0023Z 10Y ICPL Curncy',
          'S0023Z 17M BLC2 Curncy',
          'S0023Z 1I BLC2 Curncy',
          'S0023Z 1M BLC Curncy',
          'S0023Z 22Y BLC2 Curncy',
          'S0023Z 28Y BLC2 Curncy',
          'S0023Z 2I BLC2 Curncy',
          'S0023Z 2W BLC Curncy',
          'S0023Z 30Y BLC2 Curncy',
          'S0023Z 31Y BLC2 Curncy',
          'S0023Z 32Y BLC2 Curncy',
          'S0023Z 38Y BLC2 Curncy',
          'S0023Z 39Y BLC2 Curncy',
          'S0023Z 40Y BLC2 Curncy',
          'S0023Z 42D BLC2 Curncy',
          'S0023Z 48Y BLC2 Curncy',
          'S0023Z 6M BLC Curncy']

df_bbg = bbg.fetch_series(tickers, "PX_LAST",
                          startdate = pd.to_datetime('today'),
                          enddate = pd.to_datetime('today'))
df_bbg = df_bbg.transpose()
df_bbg_m = bbg.fetch_contract_parameter(tickers, "MATURITY")

print(df_bbg_m)
print(df_bbg)

# TODO achar o ero em interpolar, está aparecendo 'Timestamp' object is not subscriptable :

# interpolate_zero_curve = pd.Series(df_bbg, index = df_bbg_m)
# interpolate_zero_curve.interpolate(method='cubic', axis=0, limit=None, inplace=False, limit_direction='forward', limit_area=None, downcast=None)
#

def swap_fixed_leg_pv(today, rate, busdays, calendartype, maturity=10, periodcupons=6, notional=1000000):
    dc1 = DayCounts(busdays, calendar=calendartype)
    today = pd.to_datetime(today)
    date_range = pd.date_range(start=today, end=today + DateOffset(years=maturity), freq=DateOffset(months=periodcupons))
    date_range = dc1.modified_following(date_range)

    df = pd.DataFrame(data=date_range[:-1], columns=['Accrual Start'])
    df['Accrual End'] = date_range[1:]
    df['days'] = (df['Accrual End'] - df['Accrual Start']).dt.days
    df['Notional'] = notional

    df['Principal'] = 0
    lastline = df.tail(1)
    df.loc[lastline.index, 'Principal'] = notional

    df['Payment'] = (df['days']/ 360) * rate * df['Notional']

    df['Cash Flow'] = df['Payment'] + df['Principal']

    df['Cumulative Days'] = df['days'].cumsum()
    df['Discount'] = 1/(1+rate*(df['Cumulative Days']/360))

    df['Present Value'] = (df['Cash Flow'] * df['Discount'])

    return df

print(swap_fixed_leg_pv('2019-04-04', 0.02336, 'ACT/360', 'us_trading', 5, 6, 10000000))

def swap_floating_leg_pv(today, zero_rate, busdays, calendartype, maturity=10, periodcupons2=6, notional2=-1000000):

    dc1 = DayCounts(busdays, calendar=calendartype)
    today = pd.to_datetime(today)
    date_range = pd.date_range(start=today, end=today + DateOffset(years=maturity), freq=DateOffset(months=periodcupons2))
    date_range = dc1.modified_following(date_range)

    df2 = pd.DataFrame(data=date_range[:-1], columns=['Accrual Start'])
    df2['Accrual End'] = date_range[1:]
    df2['days'] = (df2['Accrual End'] - df2['Accrual Start']).dt.days
    df2['Notional'] = notional2

    df2['Principal'] = 0
    lastline = df2.tail(1)
    df2.loc[lastline.index, 'Principal'] = notional2

    df2['Payment'] = (df2['days'] / 360) * zero_rate * df2['Notional']

    df2['Cash Flow'] = df2['Payment'] + df2['Principal']

    df2['Cumulative Days'] = df2['days'].cumsum()
    df2['Discount'] = 1 / (1 + zero_rate * (df2['Cumulative Days'] / 360))

    df2['Present Value'] = (df2['Cash Flow'] * df2['Discount'])

    return df2


print(swap_floating_leg_pv('2019-04-04', 0.02336, 'ACT/360', 'us_trading', 5, 3, -10000000))




################  teste ######################################

# lista = [2.3,2.4,2.5,2.6,2.7]
# df_bbg = lista
# lista2 = ["07/31/2019", "08/31/2019", "09/30/2019", "10/31/2019", "11/30/2019"]
# df_bbg_m = lista2
#################################################################