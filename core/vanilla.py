import numpy as np 
from .base import Option

class CallOption(Option) :
  """
  Cette classe représente une option d'achat (Call) européenne.
  Une option Call donne au détenteur le droit, mais pas l'obligation d'acheter 
  un actif sous-jacent à un prix d'exercice fixé (K) à une date (T).
  L'investisseur est 'haussier' (bullish) : il profite si le prix du marché 
  à l'échéance (s_T) est supérieur au strike (K).
  """

  def __init__(self,strike,expiry,premium):
    super().__init__(strike,expiry,premium)

  def payoff(self,spot) :
    """
    Calcule le gain brut à l'échéance pour un Call.
    """
    return np.maximum(0,spot-self.K)

class PutOption(Option) :
  """
  Cette classe représente une option de vente (Put) européenne.
  Une option Put donne au détenteur le droit, mais pas l'obligation de vendre 
  un actif sous-jacent à un prix d'exercice fixé (K) à une date (T).
  L'investisseur est 'baissier' (bearish) : il profite si le prix du marché 
  à l'échéanc (s_T) tombe en dessous du strike (K).
  """
  
  def __init__(self,strike,expiry,premium):
    """
    Calcule le gain brut à l'échéance pour un Put.
    """
    super().__init__(strike,expiry,premium)

  def payoff(self,spot) :
     return np.maximum(0,self.K-spot)
