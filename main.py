import numpy as np
from core.vanilla import CallOption, PutOption
from core.exotic import AsianOption, BarrierOption, LookBackOption, ChooserOption, BinaryOption, ForwardStartOption
from core.simulator import GBMSimulator
from matplotlib import pyplot as plt

def main() :
    ##PARTIE 1 : TEST UNITAIRE
    
    #Création d'une trajectoire de prix fictive
    price_path = np.array([100, 102, 104, 108, 107, 112, 115, 113, 110, 112])
    
    #Paramètres de tests communs
    K=105        
    T=1         
    H=114       
    
    #Création d'un portfolio d'options de test
    portfolio=[
        CallOption(strike=K,expiry=T,premium=5.0),
        PutOption(strike=K,expiry=T,premium=5.0),
        
        AsianOption(strike=K,expiry=T,is_call=True,average_type='arithmetic'),
        AsianOption(strike=K,expiry=T,is_call=True,average_type='geometric'),
        
        #Up-and-Out Call : Meurt si on touche 114 (ce qui arrive au jour 7 avec 115)
        BarrierOption(strike=K,expiry=T,barrier=H,is_knock_in=False,is_up=True),
        
        LookBackOption(strike=K,expiry=T,type_option='Fixe',is_call=True),
        LookBackOption(strike=None,expiry=T,type_option='Flottant',is_call=True),
        
        #Le choix se fait à l'index 4 (prix=107)
        ChooserOption(strike=K, expiry=T, choice_index=4),
        
        BinaryOption(strike=K, expiry=T, payout=50.0, is_call=True),
        
        #Le strike se fixe à l'index 2 (prix=104)
        ForwardStartOption(expiry=T,fixing_index=2,is_call=True)
    ]
    
    #Boucle de test
    print("=" * 65)
    print(f"TRAJECTOIRE DE TEST : {price_path}")
    print(f"STRIKE DE RÉFÉRENCE : {K}")
    print("=" * 65)
    print(f"{'TYPE OPTION':<25} | {'PAYOFF':<10} | {'P&L NET':<10}")
    print("-" * 65)
    
    for option in portfolio:
        category = "Vanilla" if "vanilla" in option.__module__ else "Exotic"
        name = option.__class__.__name__
        full_display_name = f"{category} {name}"
        try:
            payoff_brut=option.payoff(price_path)
            pnl_net=option.calculate_pnl(price_path)
            print(f"{full_display_name:<25} | {payoff_brut:>10.2f} | {pnl_net:>10.2f}")
        except Exception as e:
            print(f"{name:<25} | ERREUR : {e}")
    print("=" * 65)
    
    ##PARTIE 2 : PRICING MONTE-CARLO
    print("\nPRICING PAR MONTE-CARLO (Simulation Stochastique)")
    
    #Configuration du simulateur
    S0=100
    r=0.05
    sigma=0.20
    T=1.0
    num_steps=252
    num_sim=100000 

    sim=GBMSimulator(S0,r,sigma,T,num_steps,num_sim)
    
    # On génère la matrice de prix (100 000 lignes)
    simulated_paths = sim.simulate_paths()
    
    # Si je veux le prix d'un Asian Call aujourd'hui :
    mon_asiatique=AsianOption(strike=105,expiry=T,is_call=True)
    
    #On calcule le payoff pour TOUTES les trajectoires simulées
    #Pour le moment, testons sur la première trajectoire simulée :
    premier_scenario=simulated_paths[0] 
    payoff_simule = mon_asiatique.payoff(premier_scenario)
    
    print(f"Gain sur le scénario n°1 : {payoff_simule:.2f}")
    
if __name__=="__main__":
  main()
