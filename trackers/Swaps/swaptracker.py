from calendars import DayCounts
import pandas as pd
from pandas.tseries.offsets import DateOffset

dc1 = DayCounts('ACT/360', calendar='us_trading')
date1 = pd.to_datetime('2019-04-04')
range = pd.date_range(start=date1, end=date1 + DateOffset(years=5), freq=DateOffset(months=6))
range = dc1.modified_following(range)

df = pd.DataFrame(data=range[:-1], columns=['Accrual Start'])
df['Accrual End'] = range[1:]
df['days'] = (df['Accrual End'] - df['Accrual Start']).dt.days
df['Notional'] = 10000000
df['Coupon']= 2.336


# df['Principal,[-1]]= 10000000
#adicionar no payment o principal, em que ele sera somado apenas no ultimo ano.

df['Payment']= (df['days']/360)* df['Coupon'] * df['Notional']

for i in df['Coupon']
df['Discount']= df['Coupon'] ** (0,5* i)
df['Present Value']= df['Payment']* df['Discount']


print(df)