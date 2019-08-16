from calendars import DayCounts
import pandas as pd
from pandas.tseries.offsets import DateOffset
from bloomberg import BBG
import numpy as np

bbg = BBG()

#Puxando os tickers para a curva zero

tickers_zero_curve = ['S0023Z 1Y BLC2 Curncy',
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
                      'S0023Z 6Y BLC2 Curncy',
                      'S0023Z 2W BLC2 Curncy',
                      'S0023Z 11M BLC2 Curncy',
                      'S0023Z 15M BLC2 Curncy',
                      'S0023Z 21M BLC2 Curncy',
                      'S0023Z 15Y BLC2 Curncy',
                      'S0023Z 25Y BLC2 Curncy',
                      'S0023Z 8Y BLC2 Curncy',
                      'S0023Z 10M BLC2 Curncy',
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
                      'S0023Z 17M BLC2 Curncy',
                      'S0023Z 1I BLC2 Curncy',
                      'S0023Z 22Y BLC2 Curncy',
                      'S0023Z 28Y BLC2 Curncy',
                      'S0023Z 2I BLC2 Curncy',
                      'S0023Z 30Y BLC2 Curncy',
                      'S0023Z 31Y BLC2 Curncy',
                      'S0023Z 32Y BLC2 Curncy',
                      'S0023Z 38Y BLC2 Curncy',
                      'S0023Z 39Y BLC2 Curncy',
                      'S0023Z 40Y BLC2 Curncy',
                      'S0023Z 42D BLC2 Curncy',
                      'S0023Z 48Y BLC2 Curncy']


df_bbg = bbg.fetch_series(tickers_zero_curve, "PX_LAST",
                          startdate = pd.to_datetime('today'),
                          enddate = pd.to_datetime('today'))
df_bbg = df_bbg.transpose()
df_bbg_m = bbg.fetch_contract_parameter(tickers_zero_curve, "MATURITY")
# fazendo a curva zero
zero_curve = pd.concat([df_bbg, df_bbg_m], axis=1, sort= True).set_index('MATURITY').sort_index()
zero_curve = zero_curve.astype(float)
zero_curve = zero_curve.interpolate(method='linear', axis=0, limit=None, inplace=False, limit_direction='backward', limit_area=None, downcast=None)
zero_curve.index = pd.to_datetime(zero_curve.index)

#def que calcula a parte fixa do contrato de swap
def swap_fixed_leg_pv(today, rate, busdays, calendartype, maturity=10, periodcupons=6, notional=1000000):
    global zero_curve
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

    days = pd.DataFrame(index = df['Accrual End'])

    zero_curve_discount = pd.concat([zero_curve, days], sort=True).sort_index()

    zero_curve_discount = zero_curve_discount.interpolate(method='linear', axis=0, limit=None, inplace=False, limit_direction='forward',
                                          limit_area=None, downcast=None)

    zero_curve_discount = zero_curve_discount.drop(index = zero_curve.index)
    zero_curve_discount = pd.DataFrame (data = zero_curve_discount.values)
    df['zero_curve_discount'] = zero_curve_discount/100

    df['Discount'] = 1/(1+(df['zero_curve_discount']*df['Cumulative Days']/360))
    df['Present Value'] = (df['Cash Flow'] * df['Discount'])
    fixed = np.sum(df['Present Value'])

    return fixed

#criando uma variavel para a parte float
swap_fixed = swap_fixed_leg_pv('2019-04-04', 0.02336, 'ACT/360', 'us_trading', 5, 6, 10000000)


# puxando tickers para floating leg
tickers_floating_leg = ["USSWAP2 BGN Curncy",
                        "USSWAP3 BGN Curncy",
                        "USSWAP4 BGN Curncy",
                        "USSWAP5 BGN Curncy",
                        "USSW6 BGN Curncy",
                        "USSWAP7 BGN Curncy",
                        "USSW8 BGN Curncy",
                        "USSW9 BGN Curncy",
                        "USSWAP10 BGN Curncy",
                        "USSWAP11 BGN Curncy",
                        "USSWAP12 BGN Curncy",
                        "USSWAP15 BGN Curncy",
                        "USSWAP20 BGN Curncy",
                        "USSWAP25 BGN Curncy",
                        "USSWAP30 BGN Curncy",
                        "USSWAP40 BGN Curncy",
                        "USSWAP50 BGN Curncy"]

bbg_floating_leg = bbg.fetch_series(tickers_floating_leg, "PX_LAST",
                          startdate = pd.to_datetime('today'),
                          enddate = pd.to_datetime('today'))
bbg_floating_leg = bbg_floating_leg.transpose()
bbg_floating_leg_m = bbg.fetch_contract_parameter(tickers_floating_leg, "MATURITY")

 # fazendo a curva para achar taxas flutuantes

floating_rate_curve = pd.concat([bbg_floating_leg, bbg_floating_leg_m], axis=1, sort= True).set_index('MATURITY').sort_index()
floating_rate_curve = floating_rate_curve.astype(float)
floating_rate_curve = floating_rate_curve.interpolate(method='linear', axis=0, limit=None, inplace=False, limit_direction='forward', limit_area=None, downcast=None)
floating_rate_curve.index = pd.to_datetime(floating_rate_curve.index)

#def que calcula a parte floating do contrato de swap

def swap_floating_leg_pv(today, busdays, calendartype, maturity=10, periodcupons2=6, notional2=-1000000):
    global zero_curve
    global floating_rate_curve

    dc1 = DayCounts(busdays, calendar=calendartype)
    today = pd.to_datetime(today)
    date_range = pd.date_range(start=today, end=today + DateOffset(years=maturity), freq=DateOffset(months=periodcupons2))
    date_range = dc1.modified_following(date_range)

    df2 = pd.DataFrame(data=date_range[:-1], columns=['Accrual Start'])
    df2['Accrual End'] = date_range[1:]
    df2['days'] = (df2['Accrual End'] - df2['Accrual Start']).dt.days
    df2['Notional'] = notional2
    df2['Cumulative Days'] = df2['days'].cumsum()

    df2['Principal'] = 0
    lastline = df2.tail(1)
    df2.loc[lastline.index, 'Principal'] = notional2

    days = pd.DataFrame(index=df2['Accrual End'])
    floating_rate = pd.concat([floating_rate_curve, days], sort=True).sort_index()
    floating_rate = floating_rate.interpolate(method='linear', axis=0, limit=None, inplace=False,
                                                          limit_direction='both',
                                                          limit_area=None, downcast=None)
    floating_rate = floating_rate.drop(index=floating_rate_curve.index)
    floating_rate = pd.DataFrame(data=floating_rate.values)
    df2['floating_leg_rate'] = floating_rate / 100
    df2['floating_leg_rate'] = 1 / (1 + (df2['floating_leg_rate'] * df2['Cumulative Days'] / 360))
    df2['floating_leg_rate'] = 1/(df2['floating_leg_rate'] * df2['Cumulative Days'] / 360)-(1/(df2['Cumulative Days'] / 360))


    df2['Payment'] = df2['floating_leg_rate'] * df2['Notional']
    df2['Cash Flow'] = df2['Payment'] + df2['Principal']

    zero_curve_discount = pd.concat([zero_curve, days], sort = True)
    zero_curve_discount = zero_curve_discount.interpolate(method='linear', axis=0, limit=None, inplace=False, limit_direction='forward',
                                          limit_area=None, downcast=None)

    zero_curve_discount = zero_curve_discount.drop(index=zero_curve.index)
    zero_curve_discount = pd.DataFrame(data=zero_curve_discount.values)
    df2['zero_curve_discount'] = zero_curve_discount / 100

    df2['Discount'] = 1 / (1 + (df2['zero_curve_discount'] * df2['Cumulative Days'] / 360))


    df2['Present Value'] = (df2['Cash Flow'] * df2['Discount'])
    floating = np.sum(df2['Present Value'])

    return floating

#criando uma variavel para a parte float
swap_floating = swap_floating_leg_pv('2019-04-04', 'ACT/360', 'us_trading', 5, 3, -10000000)

#criando uma variavel calcular o preco do contrato
swap_contract = swap_fixed + swap_floating
print(swap_contract)


