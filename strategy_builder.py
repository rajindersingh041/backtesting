from dataclasses import dataclass, field

@dataclass
class BaseStrategy:
  # name: str = 's1'
  total_lots: int = 1
  position: str = 'Sell'
  expiry: str = 'Weekly'
  select_strike_criteria: str = 'Strike Type'
  strike_type: str = 'ATM'
  premium: int = 100
  option_type: str = 'Call'
  simple_momentum: list = field(default_factory=list)
  target: list  = field(default_factory=list)
  stoploss: list  = field(default_factory=list)
  trailing_stoploss: list = field(default_factory=list)
  entry_time: str = '09:25:00'
  exit_time: str = '15:15:00'
  nse_index: str = 'Nifty Bank'
  instrument: str = None
  # strategy_name: str = 'Straddle'


@dataclass
class StrategyBuilder:
  get_name:str = 'Straddle' 
  all_strategy: dict = field(default_factory = dict)
  
  def __post_init__(self):
    self.add_straddle()
    self.add_strangle()
    self.add_straddle_strangle()
    self.add_straddle_strangle2()

  def add_straddle(self):
    leg_1 = BaseStrategy(option_type = 'Call', stoploss = [True, 'PERCENTAGE', 0.25])
    leg_2 = BaseStrategy(option_type = 'Put', stoploss = [True, 'PERCENTAGE', 0.25])
    self.all_strategy['Straddle'] = [leg_1, leg_2]
  def add_straddle2(self):
    leg_1 = BaseStrategy(option_type = 'Call', stoploss = [True, 'PERCENTAGE', 0.2])
    leg_2 = BaseStrategy(option_type = 'Put', stoploss = [True, 'PERCENTAGE', 0.2])
    self.all_strategy['Straddle'] = [leg_1, leg_2]
  def add_straddle2(self):
    leg_1 = BaseStrategy(option_type = 'Call', stoploss = [True, 'PERCENTAGE', 0.25])
    leg_2 = BaseStrategy(option_type = 'Put', stoploss = [True, 'PERCENTAGE', 0.25])
    self.all_strategy['Straddle'] = [leg_1, leg_2]


  def add_strangle(self):
    leg_1 = BaseStrategy(option_type = 'Call', stoploss = [True, 'PERCENTAGE', 0.25])
    leg_2 = BaseStrategy(option_type = 'Put', stoploss = [True, 'PERCENTAGE', 0.25])
    self.all_strategy['Strangle'] = [leg_1, leg_2]

  def add_straddle_strangle(self):
    leg_1 = BaseStrategy(option_type = 'Call', stoploss = [True, 'PERCENTAGE', 0.25])
    leg_2 = BaseStrategy(option_type = 'Put', stoploss = [True, 'PERCENTAGE', 0.25])
    leg_3 = BaseStrategy(option_type = 'Call', stoploss = [True, 'PERCENTAGE', 0.25], strike_type = 'OTM1')
    leg_4 = BaseStrategy(option_type = 'Put', stoploss = [True, 'PERCENTAGE', 0.25], strike_type = 'OTM1')
    self.all_strategy['Straddle_Strangle'] = [leg_1, leg_2, leg_3, leg_4]

  def get_me_strategy(self, name):
    return self.all_strategy[name]
