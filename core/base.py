from abc import ABC, abstractmethod
import numpy as np

class Option (ABC):
  """
  Classe abstraite pour tous les types d'options.
  Ce module définit les attributs fondamentaux partagés par tous les dérivés :
  - le strike (K)
  - l'échéance (T)
  - la prime (P)
  """

  def __init__(self,strike,expiry,premium=0.0):
    #initialisation d'un contrat d'option
    self.K=strike
    self.T=expiry
    self.P=premium

  @abstractmethod
  def payoff(self,s_T) :
    """
    Calcule le gain brut à l'échéance.
    Méthode implémentée par les classes filles.

    Args : 
      s_T : prix spot de l'actif à l'échéance

    Returns : 
      Le gain positif ou nul généré par l'exercice de l'option.
    """
    pass
    
