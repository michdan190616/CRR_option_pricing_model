import numpy as np
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import statsmodels.api as sm
import seaborn as sns
import math
from functions import *

###########--------------------###########

class Stock(object):
    def __init__(self,tick,df):

        if tick.upper() in df[df['date']==df.date.max()].ticker.unique():

            self.S0 = df.loc[df['ticker']==tick.upper()]['prc'].abs().iloc[-1]
            self.sigma = df.loc[df['ticker']==tick.upper()]['Rn'].std()

        else: exit()

###########--------------------###########

class Option(object):
    def __init__(self,r:float,T:float,N:int,stock:Stock):
        self.T = T
        self.n = N
        self.stock = stock
        self.r = r
        self.delta = self.T/self.n
        self.sigma = self.stock.sigma
        self.S0 = self.stock.S0
        self.U = np.exp(self.sigma*np.sqrt(self.delta))
        self.D = np.exp(-self.sigma*np.sqrt(self.delta))

###########--------------------###########

class Call(Option):
    def __init__(self,r,T,N,stock, k, Type):
            Option.__init__(self,r,T,N,stock)

            self.name = 'call'
            self.strike = k
            self.Type = Type

            self.price = get_price(r,T, k, self.name, Type, self.U, self.D, self.delta, self.S0)
        
    def graph(self):

        get_graph(self.strike, self.name, self.S0, self.price)

###########--------------------###########
        
class Put(Option):
    def __init__(self,r,T,N,stock, k, Type):
            Option.__init__(self,r,T,N,stock)

            self.name = 'put'
            self.strike = k
            self.Type = Type

            self.price = get_price(r,T, k, self.name, Type, self.U, self.D, self.delta, self.S0)
    
    def graph(self):

        get_graph(self.strike, self.name, self.S0, self.price)

###########--------------------###########

class Bear_Spread(Option):
    def __init__(self,r,T,N,stock, k, Type):
            Option.__init__(self,r,T,N,stock)

            self.name = 'bear_spread'
            self.strike = k
            self.Type = Type

            self.price = get_price(r,T, k, self.name, Type, self.U, self.D, self.delta, self.S0)
    
    def graph(self):

        get_graph(self.strike, self.name, self.S0, self.price)

###########--------------------###########

class Bull_Spread(Option):
    def __init__(self,r,T,N,stock, k, Type):
            Option.__init__(self,r,T,N,stock)

            self.name = 'bull_spread'
            self.strike = k
            self.Type = Type

            self.price = get_price(r,T, k, self.name, Type, self.U, self.D, self.delta, self.S0)
    
    def graph(self):

        get_graph(self.strike, self.name, self.S0, self.price)

###########--------------------###########

class Forward(Option):
    def __init__(self,r,T,N,stock, k):
            Option.__init__(self,r,T,N,stock)

            self.name = 'forward'
            self.strike = k

            self.price = get_price(r,T, k, self.name, 'european', self.U, self.D, self.delta, self.S0)
    
    def graph(self):

        get_graph(self.strike, self.name, self.S0, self.price)

###########--------------------###########

class Straddle(Option):
    def __init__(self,r,T,N,stock, k, Type):
            Option.__init__(self,r,T,N,stock)

            self.name = 'straddle'
            self.strike = k
            self.Type = Type

            self.price = get_price(r,T, k, self.name, Type, self.U, self.D, self.delta, self.S0)
    
    def graph(self):

        get_graph(self.strike, self.name, self.S0, self.price)

###########--------------------###########

class Butterfly_Spread(Option):
    def __init__(self,r,T,N,stock, k, Type):
            Option.__init__(self,r,T,N,stock)

            self.name = 'butterfly_spread'
            self.strike = k
            self.Type = Type

            self.price = get_price(r,T, k, self.name, Type, self.U, self.D, self.delta, self.S0)
    
    def graph(self):

        get_graph(self.strike, self.name, self.S0, self.price)

###########--------------------###########

class Chooser(Option):
    def __init__(self,r,T,N,stock, k, Type):
            Option.__init__(self,r,T,N,stock)

            self.name = 'chooser'
            self.strike = k
            self.Type = Type

            self.price = get_price(r,T, k, self.name, Type, self.U, self.D, self.delta, self.S0)
    
    def graph(self):

        get_graph(self.strike, self.name, self.S0, self.price)








###########--------------------###########
###########--------------------###########

def create_option(derivative, option_type, stock,r,T,parameter=None, parameter2=None, parameter3=None):
    N=1200
    derivative = derivative.lower()
    if derivative == 'call':
         return Call(r,T,N,stock,parameter,option_type)
    
    elif derivative == 'put':
         return Put(r,T,N,stock,parameter,option_type)
    
    elif derivative == 'forward':
         return Forward(r,T,N,stock,parameter)
    
    elif derivative == 'straddle':
         return Straddle(r,T,N,stock,parameter,option_type)
    
    elif derivative == 'chooser':
         return Chooser(r,T,N,stock,parameter,option_type)
    
    elif derivative == 'bear spread':
         return Bear_Spread(r,T,N,stock,[parameter,parameter2],option_type)
    
    elif derivative == 'bull spread':
         return Bull_Spread(r,T,N,stock,[parameter,parameter2],option_type)
    
    elif derivative == 'butterfly spread':
         return Butterfly_Spread(r,T,N,stock,[parameter,parameter2,parameter3],option_type)
