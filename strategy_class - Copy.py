import concurrent.futures
import pandas as pd
import os

class EntrySetting():
  def __init__(self, entry, exit):
    self.entry = entry
    self.exit = exit

class NseIndex():
  def __init__(self, name):
    self.name = name

class MoveCostSL():
  def __init__(self, flag):
    self.active = flag

class AddSimpleMomentum:

  def __init__(self, name, val):
    if name.upper() == 'STRIKE_POINTS_UP':
      pass
    elif name.upper() == 'STRIKE_POINTS_DOWN':
      pass
    elif name.upper() == 'STRIKE_PCT_UP':
      pass
    elif name.upper() == 'STRIKE_PCT_DOWN':
      pass
    elif name.upper() == 'UINDEX_POINTS_UP':
      pass
    elif name.upper() == 'UINDEX_POINTS_DOWN':
      pass
    elif name.upper() == 'UINDEX_PCT_UP':
      pass
    elif name.upper() == 'UINDEX_PCT_DOWN':
      pass

class AddTarget:

  def __init__(self, name, val):
    if name.upper() == 'STRIKE_POINTS':
      pass
    elif name.upper() == 'STRIKE_PCT':
      pass
    elif name.upper() == 'UINDEX_POINTS':
      pass
    elif name.upper() == 'UINDEX_PCT':
      pass

class AddStoploss:

  def __init__(self, name, val):
    if name.upper() == 'STRIKE_POINTS':
      pass
    elif name.upper() == 'STRIKE_PCT':
      pass
    elif name.upper() == 'UINDEX_POINTS':
      pass
    elif name.upper() == 'UINDEX_PCT':
      pass

class AddTrailingStoploss:

  def __init__(self, val1, val2):
    pass

class AddLeg:
  
  def __init__(self, lots = 1, position = 'sell', option_type = 'call', expiry = 'weekly',strike_criteria = 'strike_type', strike_type = 'ATM',
    premium = 100, simple_momentum = [False, 0 , 0], target = [False, 0 , 0], stoploss = [False, 0, 0], trailing_stoploss = [False, 0, 0],
    reentry_on_sl = False, reentry_on_target = False, entry_active = False, entry_time = None, entry_at = None,
    exit_active = False, exit_time = None, exit_at = None):

    self.lots = lots
    self.position = position
    self.option_type = option_type
    self.expiry = expiry
    self.strike_criteria = strike_criteria
    self.strike_type = strike_type
    self.premium = premium
    self.simple_momentum_active = simple_momentum[0]
    self.simple_momentum_name = simple_momentum[1]
    self.simple_momentum_val = simple_momentum[2]
    self.target_active = target[0]
    self.target_name = target[1]
    self.target_val = target[2]
    self.stoploss_active = stoploss[0]
    self.stoploss_name = stoploss[1]
    self.stoploss_val = stoploss[2]
    self.trailing_stoploss_active = trailing_stoploss[0]
    self.trailing_stoploss_val1 = trailing_stoploss[1]
    self.trailing_stoploss_val2 =trailing_stoploss[2]
    self.reentry_on_sl = reentry_on_sl
    self.reentry_on_target = reentry_on_target
    self.entry_active = entry_active
    self.entry_time = entry_time
    self.entry_at = entry_at
    self.exit_active = exit_active
    self.exit_time = exit_time
    self.exit_at = exit_at
    self.factor = 1 if position == 'buy' else -1


class Strategy:
  all_leg = {}
  myid = 0
  def __init__(self):

    self.add_leg(option_type = 'call', position = 'buy', strike_criteria = 'closest_premium', premium = 100,
      simple_momentum = [True, 'STRIKE_PCT_UP', 0.15], target = [False, 'POINTS', 50], stoploss = [True, 'PERCENTAGE', 0.25])

    self.add_leg(option_type = 'put', position = 'buy', strike_criteria = 'closest_premium', premium = 100,
      simple_momentum = [True, 'STRIKE_PCT_UP', 0.15], target = [False, 'POINTS', 50], stoploss = [True, 'PERCENTAGE', 0.25])
  
  def add_leg(self,lots = 1, position = 'sell', option_type = 'call', expiry = 'weekly',strike_criteria = 'strike_type', strike_type = 'ATM',
    premium = 100, simple_momentum = [False, 0 , 0], target = [False, 0 , 0], stoploss = [False, 0, 0], trailing_stoploss = [False, 0, 0],
    reentry_on_sl = False, reentry_on_target = False):
    Strategy.myid += 1
    self.all_leg[Strategy.myid] = {}
    self.all_leg[Strategy.myid] = AddLeg(option_type = option_type, position = position, strike_criteria = strike_criteria, premium = premium,
      simple_momentum = simple_momentum, target = target, stoploss = stoploss)


class Execute:

  def __init__(self, df):
    # self.df_date = #'abc'
    self.entry_setting = EntrySetting(entry = '09:35:00', exit = '15:15:00')
    self.nse_index = NseIndex('Nifty Bank')
    self.move_to_sl = MoveCostSL(1)
    self.df = df['data']#pd.read_csv(r'C:\Users\zp2117\Work non ondrive\shoonya-v2\back_tester\BNF_201904_202204\BANKNIFTY-2022-06-16.csv')
    self.df_date = df['filename']
    self.spot, self.spot_atm = self.get_spot_and_atm(self.df)
    self.legs = Strategy().all_leg
    self.get_ce_pe()
    self.loop_over_time()
    self.get_pnl()
    # self.return_pnl()
    # print(self.df_date)

  def return_pnl(self):
    return self.df_date, self.total_pnl

  def get_pnl(self):
    pnl = 0
    l = self.legs.copy()
    for k in l: #self.legs:
      myleg  = l[k]#self.legs[k]
      if myleg.entry_active and myleg.exit_active:
        pnl += (myleg.exit_price - myleg.entry_price) * myleg.factor
    self.total_pnl = pnl * 25
    # return self.df_date, total_pnl
    # print(f"{self.df_date} : {total_pnl:.0f}")


  def loop_over_time(self):
    df2 = self.df.copy()
    df2 = df2[(df2['time'] >= self.entry_setting.entry) & (df2['time'] <= self.entry_setting.exit)].copy()
    for tmt in df2['time'].tolist():
      self.enter(tmt)
      self.stoploss(tmt)
      self.end_of_day(tmt)

  def end_of_day(self, mytmt):
    if mytmt != self.entry_setting.exit:
      return
    for k in self.legs:
      myleg  = self.legs[k]
      if not myleg.exit_active and myleg.entry_active:
        ltp = self.get_option_ltp(myleg.instrument, 'open', self.entry_setting.exit)
        myleg.exit_price = ltp
        myleg.exit_at = 'open'
        myleg.exit_time = mytmt
        myleg.exit_active = True
        print('exit time')

  def stoploss(self, mytmt):
    # print('Hi', mytmt)
    for k in self.legs:
      myleg  = self.legs[k]
      if myleg.exit_active:
        return
      # elif not myleg.entry_active:
      #   return
      # print(mytmt,myleg.instrument, myleg.entry_active)
      if myleg.entry_active:
        ltp = self.get_option_ltp(myleg.instrument, 'open', mytmt)
        # print(ltp, myleg.stoploss_price)
        if myleg.stoploss_name.upper() == 'PERCENTAGE':
          if ltp <= myleg.stoploss_price:
            myleg.exit_price = ltp
            myleg.exit_at = 'open'
            myleg.exit_time = mytmt
            myleg.exit_active = True
            print('SL hit')
          elif self.get_option_ltp(myleg.instrument, 'low', mytmt) <= myleg.stoploss_price:
            print('SL hit at low')
            myleg.exit_price = self.get_option_ltp(myleg.instrument, 'low', mytmt)
            myleg.exit_at = 'low'
            myleg.exit_time = mytmt
            myleg.exit_active = True



  def get_atm(self, price, ch = 100):
      return round(price / ch) * ch

  def get_spot_and_atm(self, df):
    spot = df[df['time'] == self.entry_setting.entry].iloc[0]['open']
    spot_atm = self.get_atm(spot)
    return spot, spot_atm

  def get_option_ltp(self, instrument, ohlc = 'open', tmt = None):
    df = self.df
    prc = df[df['time'] == tmt].iloc[0][f"{instrument}_{ohlc}"]
    return prc

  def get_ce_pe(self):
    strikes = []
    for k in self.legs:
      myleg  = self.legs[k]
      if myleg.strike_criteria == 'closest_premium':
        myleg.instrument = self.find_closest_premium_strike(myleg.premium, myleg.option_type)

      elif myleg.strike_criteria == 'strike_type':
        if 'ATM' in myleg.strike_type:
          myleg.instrument = str(self.spot_atm) + 'C' if myleg.option_type == 'call' else None
          myleg.instrument = str(self.spot_atm) + 'P' if myleg.option_type == 'put' else None
        elif 'ITM' in myleg.strike_type:
          no = myleg.strike_type[-1]
          myleg.instrument = str(self.spot_atm - no * 100) + 'C' if myleg.option_type == 'call' else None
          myleg.instrument = str(self.spot_atm + no * 100) + 'P' if myleg.option_type == 'put' else None

        elif 'OTM' in myleg.strike_type:
          no = myleg.strike_type[-1]
          myleg.instrument = str(self.spot_atm + no * 100) + 'C' if myleg.option_type == 'call' else None
          myleg.instrument = str(self.spot_atm - no * 100) + 'P' if myleg.option_type == 'put'  else None

      myleg.price = self.get_option_ltp(myleg.instrument, 'open', self.entry_setting.entry)

  def get_options_df():
    dfg = self.df
    cols = []

    for ohlc in ['open', 'high', 'low', 'close']:
        cols.append(col + '_' + ohlc)

    cols.append('time');
    cols.append('timestamp')

    df = dfg[cols]
    df.columns = ['open', 'high', 'low', 'close', 'time', 'timestamp']
    df = df[(df['time'] >= entry_time) & (df['time'] <= exit_time)]
    entry_open = df[df['time'] >= entry_time].iloc[0]['open']
    try:
        c = int(entry_open)
    except Exception as e:
        raise e
    return df, entry_open


  def find_closest_premium_strike(self, closestPremiumValue, C_P2):
    C_P = 'C' if C_P2 == 'call' else 'P'
    df2 = self.df.copy()
    df2 = df2.loc[df2['time'] == self.entry_setting.entry]
    df2 = df2.filter(regex=C_P + '_open')
    df2 = dict(df2.T.iloc[:, -1] )
    # print(df2)
    df2 = pd.DataFrame(df2.items(), columns=['strike', 'ltp'])
    df2['strike'] = df2['strike'].apply(lambda x: x[0:6])
    df2['absolute'] = abs(df2['ltp'] - closestPremiumValue)
    df2 = df2.sort_values(by=['absolute'], ascending=True)
    return df2['strike'].tolist()[0]

  def enter(self, mytmt):
    for k in self.legs:
      myleg  = self.legs[k]
      ltp_open = self.get_option_ltp(myleg.instrument, 'open', mytmt)
      ltp_high = self.get_option_ltp(myleg.instrument, 'high', mytmt)
      ltp_low = self.get_option_ltp(myleg.instrument, 'low', mytmt)

      if myleg.entry_active: return

      if myleg.simple_momentum_active and not myleg.entry_active:
        if myleg.simple_momentum_name == 'STRIKE_PCT_UP':
          if ltp_open >= myleg.price * (1 + myleg.simple_momentum_val):
            myleg.entry_price = ltp_open
            myleg.entry_active = True
            myleg.entry_time = mytmt
            myleg.entry_at = 'open'
            print(f"{self.df_date} Momentum achieved at Open")

          elif self.get_option_ltp(myleg.instrument, 'high', mytmt) >= myleg.price * (1 + myleg.simple_momentum_val):
            myleg.entry_price = ltp_high
            myleg.entry_active = True
            print(f"{self.df_date} Momentum achieved at High")
            myleg.entry_time = mytmt
            myleg.entry_at = 'high'
        elif myleg.simple_momentum_name == 'STRIKE_PCT_DOWN':
          if ltp <= myleg.price * (1 - myleg.simple_momentum_val):
            myleg.entry_price = ltp_open
            myleg.entry_active = True
            print(f"{self.df_date} Momentum achieved at Open")
            myleg.entry_time = mytmt
            myleg.entry_at = 'open'
          elif self.get_option_ltp(myleg.instrument, 'low', mytmt) >= myleg.price * (1 - myleg.simple_momentum_val):
            myleg.entry_price = ltp_low
            myleg.entry_active = True
            print(f"{self.df_date} Momentum achieved at Low")
            myleg.entry_time = mytmt
            myleg.entry_at = 'low'
      if myleg.stoploss_active and myleg.entry_active:
        # print('Placing  SL')
        myleg.stoploss_price = myleg.entry_price * (1 - myleg.stoploss_val * myleg.factor)

# a = Execute()
# print(vars(a))
# print(a.legs[1].__dict__)
# print(a.legs[2].__dict__)
# for i in a.legs.keys():
#   print(vars(a.legs[i]))

all_files_path = r'C:\Users\zp2117\Work non ondrive\shoonya-v2\back_tester\BNF_201904_202204'
file_list = os.listdir(all_files_path)

banknifty_data = []
for filename in file_list[:5]:
    filepath = all_files_path + '//' + filename
    try:
        df = pd.read_csv(filepath, parse_dates = ['date','ds','timestamp','expiry'])
        df.sort_values('timestamp', inplace=True)
        banknifty_data.append({'filename':filename,'data': df})
    except:
        print(f"issue with {filename}")



def check2(mydf):
  # a = Execute(mydf)
  b, c = Execute(mydf).return_pnl()
  print(b,c)

# check2(banknifty_data[0])

# a = Execute()
with concurrent.futures.ThreadPoolExecutor() as executor:
  results = executor.map(check2, banknifty_data)

for f in results:
  print(f)
#   results = executor.map(check2, banknifty_data)
#   # x2 = 
  # results = executor.map(check2, [x for x in banknifty_data])
#   # results2 = [res.df_dt for res in results]
#   # print([x for x in results])
#   # print("result_list: ", results)
  # for result in results:
  #   print("Result ==========================>", str(result))

# # results2 = [(res.df_dt, res.total_pnl) for res in results]
# for i in results:
#   print(i)

# print(results.__dict__)
# merged_list = [v for f in futures for v in f.result()]
# print(banknifty_data[0])