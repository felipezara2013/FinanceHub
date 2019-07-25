from calendars import DayCounts
import pandas as pd
from pandas.tseries.offsets import DateOffset

#dc1 = DayCounts('ACT/360', calendar='us_trading')
#date1 = pd.to_datetime('2019-04-04')
#range1 = pd.date_range(start=date1, end=date1 + DateOffset(years=5), freq = DateOffset(months=6))
#range1 = dc1.modified_following(range1)
#df = pd.DataFrame(data=range1[:-1], columns=['Accrual Start'])
#df['Accrual End'] = range1[1:]
#df['days'] = (df['Accrual End'] - df['Accrual Start']).dt.days
#df['Notional'] = 10000000
#df['Coupon'] = 0.02336

#lastline = df.tail(1)

#df.loc[lastline.index,'Principal']=10000000

#df['Payment'] = ((df['days']/360)* df['Coupon'] * df['Notional']).round(2)
#contador = 1
#lista = []
#for i in df.index:
   # value_disc = 1/((1+(6/12)*df['Coupon'][i])**contador)
  #  lista.append(value_disc)
 #   contador += 1

#df["Discount"]=lista
#df['Present Value'] = (df['Payment'] * df['Discount']).round(2)
#print(df)


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


    lista = []
    i=0
    for contador in df.index + 1:
        value_disc = 1 / ((1 + (df['days'][i]/ 360)* rate) ** contador)
        lista.append(value_disc)
        i+=1


    df["Discount"] = lista
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

    lista2 = []
    i=0
    for contador in df2.index + 1:
        value_disc = 1 / ((1 +(df2['days'][i] / 360)  * zero_rate) ** contador)
        lista2.append(value_disc)
        i+=1

    df2["Discount"] = lista2
    df2['Present Value'] = (df2['Cash Flow'] * df2['Discount'])

    return df2


print(swap_floating_leg_pv('2019-04-04', 0.02336, 'ACT/360', 'us_trading', 5, 3, -10000000))