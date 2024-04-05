import numpy as np
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import statsmodels.api as sm
import seaborn as sns
import math
import time


###########--------------------###########
###########--------------------###########

def payoff_func(s, k, name) -> np.ndarray:

    match name:
        case 'call':
        
            return np.maximum(s-k,0)
        
        case 'put':

            return np.maximum(k-s,0)
        
        case 'bear_spread':

            return np.maximum(k[1]-s,0)-np.maximum(k[0]-s,0)
        
        case 'bull_spread':

            return np.maximum(k[0]-s,0)-np.maximum(k[1]-s,0)
        
        case 'forward':
            
            return s-k
        
        case 'straddle':
            
            return np.maximum(s-k,0) + np.maximum(k-s,0)
        
        case 'butterfly_spread':
        
            return np.maximum(k[0]-s,0)+np.maximum(s-k[2],0)-(np.maximum(s-k[1],0) + np.maximum(k[1]-s,0))
        
        case 'chooser':
            
            return np.maximum(k-s,s-k)
        
        case _:
            return 0

###########--------------------###########
###########--------------------###########
def get_price(r,T, k, name, Type, U, D, delta, S0):

    name = name.lower()
    Type = Type.lower()

    N = int(T/delta)
    q=(np.exp(r*delta)-D)/(U-D)   #define EMM
    gamma=np.exp(-r*delta)        #define discounting factor 
    
    stock_mat = U*np.ones((N+1, N+1))+np.tril(-U*np.ones((N+1, N+1)))+\
                    np.diag(np.concatenate([np.array([1]),np.ones(N)*(D)]).cumprod())+np.tril(np.ones([N+1, N+1]), -1)
        
    stock_mat[0,0] = 1

    stock_mat = stock_mat.cumprod(axis = 1)

    stock_mat = S0*np.triu(stock_mat)

    ###########--------------------###########

    if(Type == 'european'):

        prices=np.zeros((N+1, N+1))   #define prices matrix
        prices[:, -1]= payoff_func(stock_mat[:,-1], k, name)

        for j in reversed(range(0,N)):

                prices[:(j+1),j]=gamma*(q*prices[:(j+1), j+1]+(1-q)*prices[1:(j+2), j+1])

        return prices[0,0]
    
    ###########--------------------###########
    
    elif((Type == 'american')&(name!='forward')):

        prices=np.zeros((N+1, N+1))   #define prices matrix
    
        prices[:, -1]= payoff_func(stock_mat[:,-1], k, name)

        for j in reversed(range(0,N)):

                prices[:(j+1),j] = np.maximum(gamma*(q*prices[:(j+1), j+1]+(1-q)*prices[1:(j+2), j+1]), payoff_func(stock_mat[:(j+1),j], k, name))
    
        return prices[0,0]
    
    ###########--------------------###########

    elif((Type == 'asian')&(name!='forward')):

        N = min(20, int(T/delta))
        delta = T/N
        gamma = np.exp(-r*delta) 
        prices=np.zeros((2**N, N+1))

        #calculate the means in the paths using binary numbers to track up and down and their position 
        mat2 = np.array([list(map(int,bin(i)[2:].zfill(N))) for i in range(2**N)])

        means = (S0*(U**(1-mat2)*D**(mat2)).cumprod(axis=1)).mean(axis=1)
         
        prices[:, -1]= payoff_func(means, k, name)

        for j in reversed(range(0,N)): 

                prices[0:2**j,j] = gamma*(q*prices[0:(2**(j+1)):2, j+1]+ (1-q)*prices[1:2**(j+1):2, j+1])
       
        return prices[0,0]

    else:
        return 0
    

###########--------------------###########
###########--------------------###########
def get_graph(k, name, S0, price):

    x = np.linspace(0, np.max(k)+S0, num = 500)

    y = payoff_func(x, k, name)-price
    plt.title(name.replace('_',' ').upper()+" PAYOFF",size = 18)
    plt.xlabel("Stock Price")
    plt.ylabel("Payoff")
    plt.grid(True)
    return plt.plot(x,y)