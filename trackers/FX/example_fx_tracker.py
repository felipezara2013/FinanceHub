from trackers import FXForwardTrackers
import matplotlib.pyplot as plt
from bloomberg import BBG
import pandas as pd

currency = 'BRL'

# Calculate your own FX tracker
fx = FXForwardTrackers(currency)
fx_tracker_df = fx.df_tracker

# Get Bloomberg's FX tracker
bbg = BBG()
bbg_carry_raw = bbg.fetch_series(securities=currency + 'USDCR CMPN Curncy',
                                 fields='PX_LAST',
                                 startdate=fx_tracker_df.index[0].date(),
                                 enddate=fx_tracker_df.index[-1].date())
bbg_carry_raw.columns = ['bbg_tracker']


bbg_carry_index = pd.Series(index=fx_tracker_df.index)
bbg_carry_index.iloc[0] = fx_tracker_df.iloc[0, 0]
for d in bbg_carry_index.index[1:]:
    ret = fx_tracker_df.loc[d,'er_index'] / fx_tracker_df.loc[:d].iloc[-2, 0]
    bbg_carry_index.loc[d] = bbg_carry_index.loc[:d].iloc[-2] * ret

fig, ax = plt.subplots()
fx_tracker_df['er_index'].to_frame('my_index').dropna().plot(color='b', linewidth=3, ax=ax)
bbg_carry_index.to_frame('bbg_index').plot(color='r', linewidth=1, ax=ax)
plt.title(currency + ' tracker')
plt.show()