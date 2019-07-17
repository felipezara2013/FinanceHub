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

def swap(date, busdays, calendartype, numberyear, periodcupons, rate, notional, principal):
    dc1 = DayCounts(busdays, calendar=calendartype)
    date1 = pd.to_datetime(date)
    range = pd.date_range(start=date1, end=date1 + DateOffset(years=numberyear), freq=DateOffset(months=periodcupons))
    range = dc1.modified_following(range)

    df = pd.DataFrame(data=range[:-1], columns=['Accrual Start'])
    df['Accrual End'] = range[1:]
    df['days'] = (df['Accrual End'] - df['Accrual Start']).dt.days
    df['Notional'] = notional
    df['Coupon']= rate

    lastline = df.tail(1)
    df.loc[lastline.index,'Principal']=principal
    #adicionar no payment o principal, em que ele sera somado apenas no ultimo ano.

    df['Payment']= ((df['days']/360)* df['Coupon'] * df['Notional']).round(2)
    for i in df['Coupon']:
        df['Discount'] = (df['Coupon'] ** (0.5 * i)).round(2)
        df['Present Value'] = (df['Payment'] * df['Discount']).round(2)
    return df

print(swap('2019-04-04','ACT/360','us_trading',5,6,2.336,10000000,10000000))


