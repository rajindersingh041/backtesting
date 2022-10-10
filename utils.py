import pandas as pd
def get_atm(price, ch = 100):
    return round(price / ch) * ch

def get_ohlc(df, time):
  spot = df[df['time'] == time].iloc[0]
  return [spot['open'], spot['high'], spot['low'], spot['close']]
  
def find_closest_premium_strike(df, time, premium, option_type):
  Call_Put = 'C' if option_type.upper() == 'CALL' else 'P'
  df = df.loc[df['time'] == time]
  df = df.filter(regex=Call_Put + '_open')
  df = dict(df.T.iloc[:, -1] )
  
  df2 = pd.DataFrame(df.items(), columns=['strike', 'ltp'])
  df2['strike'] = df2['strike'].apply(lambda x: x[0:6])
  df2['absolute'] = abs(df2['ltp'] - closestPremiumValue)
  df2 = df2.sort_values(by=['absolute'], ascending=True)
  return df2['strike'].tolist()[0]