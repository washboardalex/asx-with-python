import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web

style.use('dark_background')

#COMMENT AND UNCOMMENT AS YOU PLEASE 

# ORGANISE DATA
start = dt.datetime(2015, 1, 1)
end = dt.datetime.now()
df = web.DataReader("TSLA", 'iex', start, end)
df.reset_index(inplace=True)
df.set_index("date", inplace=True)
print(df.head())
df.to_csv('TSLA.csv')
df=pd.read_csv('tsla.csv', parse_dates=True, index_col=0)

# HIGH-LOW
df[['high', 'low']].plot()
plt.show()

# MOVING AVERAGE
df['100ma'] = df['close'].rolling(window=100, min_periods=0).mean()
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1,sharex=ax1)
ax1.plot(df.index, df['close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['volume'])
plt.show()

# OHLC 
df_ohlc = df['close'].resample('10D').ohlc()
df_volume = df['volume'].resample('10D').sum()

print(df_ohlc.head())

df_ohlc = df_ohlc.reset_index()
df_ohlc['date'] = df_ohlc['date'].map(mdates.date2num)

fig = plt.figure()
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1,sharex=ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num),df_volume.values,0)
plt.show()

