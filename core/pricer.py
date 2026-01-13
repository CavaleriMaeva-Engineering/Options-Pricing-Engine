import numpy as np
from core.simulator import GBMSimulator 
from core.exotic import AsianOption, BarrierOption, LookBackOption, ChooserOption, BinaryOption, ForwardStartOption

class MonteCarloPricer :
    """
    Moteur de valorisation par la méthode de Monte-Carlo.
    
    Le prix d'une option est calculé comme l'espérance de son payoff futur 
    actualisée au taux sans risque r : Price = E[Payoff]*exp(-r*T).
    """
    
    def __init__(self,option,simulator) :
        """
        Args :
            - option (Option): Un objet héritant de la classe de base Option.
            - simulator (GBMSimulator): Un simulateur de trajectoires de prix.
        """
        self.option=option
        self.simulator=simulator 
        
    def price(self) :
        """
        Exécute la simulation et calcule la prime de l'option.
        Retourne la juste valeur (fair value) de l'option aujourd'hui.
        """
        #Génération des scénarios de marché
        paths=self.simulator.simulate_paths()
        
        #calcul du gain pour chaque scénario
        payoffs=self.option.payoff(paths)
        
        #Calcul du gain moyen attendu
        expected_payoff=np.mean(payoffs)
        
        #Actualisation au présent
        option_price=expected_payoff*np.exp(-self.simulator.r*self.simulator.T)
        
        return option_price