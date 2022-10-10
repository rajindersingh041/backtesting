import concurrent.futures
import pandas as pd
import os
from dataclasses import dataclass, field
import utils
from strategy_builder import StrategyBuilder

@dataclass
class SetupToExecute:
  df: pd.DataFrame
  exc_strategy_name: str

  def __post_init__(self):
    self.spot_atm = 2
    self.mystrategy = StrategyBuilder().get_me_strategy(self.exc_strategy_name)

  def get_atm(self, price, ch = 100):
      return round(price / ch) * ch

  def get_ohlc(self, df, time):
    spot = df[df['time'] == time].iloc[0]
    return [spot['open'], spot['high'], spot['low'], spot['close']]


  def find_instruments(self):
    if self.mystrategy.select_strike_criteria.upper() == 'STRIKE TYPE':
      self.find_strike_by_strike()
    elif self.mystrategy.select_strike_criteria.upper() == 'CLOSEST PREMIUM':
      self.find_strike_by_premium()

  def find_strike_by_premium(self):
    pass

  def find_strike_by_strike(self):
    pass

mydf = pd.read_csv(fr'C:\Users\zp2117\Work non ondrive\shoonya-v2\back_tester\BNF_201904_202204\BANKNIFTY-2022-06-15.csv')
a = SetupToExecute(mydf, 'Straddle_Strangle')
print(a.mystrategy)