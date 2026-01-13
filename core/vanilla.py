import numpy as np 
from scipy.stats import norm
from core.base import Option

class CallOption(Option) :
  """
  Cette classe représente une option d'achat (Call) européenne.
  Une option Call donne au détenteur le droit, mais pas l'obligation d'acheter 
  un actif sous-jacent à un prix d'exercice fixé (K) à une date (T).
  L'investisseur est 'haussier' (bullish) : il profite si le prix du marché 
  à l'échéance (s_T) est supérieur au strike (K).
  """
  
  def __init__(self,strike,expiry,premium=0.0) :
        super().__init__(strike,expiry,premium)

  def payoff(self,spot) :
        """
        Calcule le gain brut à l'échéance pour un Call.
        """
        return np.maximum(0,spot[:,-1]-self.K)
    
  def price_black_scholes(self,S0,r,sigma) :
      d1=(np.log(S0/self.K)+(r+0.5*sigma**2)*self.T)/(sigma*np.sqrt(self.T))
      d2=d1-sigma*np.sqrt(self.T)
      price=S0*norm.cdf(d1)-self.K*np.exp(-r*self.T)*norm.cdf(d2)
      return price
      
class PutOption(Option) :
  """
  Cette classe représente une option de vente (Put) européenne.
  Une option Put donne au détenteur le droit, mais pas l'obligation de vendre 
  un actif sous-jacent à un prix d'exercice fixé (K) à une date (T).
  L'investisseur est 'baissier' (bearish) : il profite si le prix du marché 
  à l'échéanc (s_T) tombe en dessous du strike (K).
  """
  
  def __init__(self,strike,expiry,premium=0.0) :
      """
      Calcule le gain brut à l'échéance pour un Put.
      """
      super().__init__(strike,expiry,premium)

  def payoff(self,spot) :
     return np.maximum(0,self.K-spot[:,-1])
 

  def price_black_scholes(self,S0,r,sigma) :
     d1=(np.log(S0/self.K)+(r+0.5*sigma**2)*self.T)/(sigma*np.sqrt(self.T))
     d2=d1-sigma*np.sqrt(self.T)
     price=self.K*np.exp(-r*self.T)*norm.cdf(-d2)-S0*norm.cdf(-d1)
     return price
 
    
 
    
 
    
