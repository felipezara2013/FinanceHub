from calendars import DayCounts
import pandas as pd
from pandas.tseries.offsets import DateOffset

#dc1 = DayCounts('ACT/360', calendar='us_trading')
#date1 = pd.to_datetime('2019-04-04')
#range = pd.date_range(start=date1, end=date1 + DateOffset(years=5), freq=DateOffset(months=6))
#range = dc1.modified_following(range)

#df = pd.DataFrame(data=range[:-1], columns=['Accrual Start'])
#df['Accrual End'] = range[1:]
#df['days'] = (df['Accrual End'] - df['Accrual Start']).dt.days
#df['Notional'] = 10000000
#df['Coupon']= 2.336

#lastline = df.tail(1)

#df.loc[lastline.index,'Principal']=10000000
#adicionar no payment o principal, em que ele sera somado apenas no ultimo ano.

#df['Payment']= ((df['days']/360)* df['Coupon'] * df['Notional']).round(2)

#    for i in df['Coupon']:
        #df['Discount'] = (df['Coupon'] ** (0.5 * i)).round(2)
        #df['Present Value'] = (df['Payment'] * df['Discount']).round(2)
#print(df)


def swap_fixed_leg_cf(today, rate, busdays, calendartype, maturity=10, periodcupons=6, notional=1000000):
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

    df['Payment'] = (df['days']/360) * rate * df['Notional']

    df['Cash Flow'] = df['Payment'] + df['Principal']

    return df


print(swap_fixed_leg_cf('2019-04-04', 0.02336, 'ACT/360', 'us_trading', 5, 6, 10000000))


