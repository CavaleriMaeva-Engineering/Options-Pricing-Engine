import numpy as np
import matplotlib.pyplot as plt
from core.vanilla import CallOption
from core.exotic import AsianOption,BarrierOption,LookBackOption,ChooserOption,BinaryOption,ForwardStartOption
from core.simulator import GBMSimulator
from core.pricer import MonteCarloPricer

def main():
    #CONFIGURATION DU MARCHÉ 
    S0,r,sigma,T=100.0,0.05,0.20,1.0
    K=100.0
    num_sim=100000 #100k pour une bonne convergence
    
    sim=GBMSimulator(S0,r,sigma,T,num_steps=252,num_simulations=num_sim)

    #DÉFINITION DES PRODUITS (On veut comparer leur valeur relative)
    portfolio = [
        ("Vanilla Call", CallOption(K,T)),
        ("Asian Call (Arith)", AsianOption(K,T,average_type='arithmetic')),
        ("Asian Call (Geo)", AsianOption(K,T,average_type='geometric')),
        ("Barrier Call (Up-and-Out H=120)", BarrierOption(K,T,barrier=120,is_knock_in=False)),
        ("Lookback Call (Fixed Strike)", LookBackOption(K,T,type_option='Fixe')),
        ("Binary Call (Payout=10)", BinaryOption(K,T,payout=10.0)),
    ]

    print("="*95)
    print(f"REPORT: DERIVATIVE VALUATION ENGINE | S0={S0} | r={r} | sigma={sigma} | T={T}")
    print("="*95)
    print(f"{'PRODUCT NAME':<35} | {'MC FAIR VALUE':<15} | {'ANALYTICAL (BS)':<15} | {'DIFFERENCE'}")
    print("-"*95)

    for name, option in portfolio:
        #Calcul par Monte-Carlo
        pricer_mc=MonteCarloPricer(option,sim)
        mc_price=pricer_mc.price()
        
        #Calcul Analytique (uniquement pour la Vanille pour valider le moteur)
        bs_price_string="N/A"
        difference="N/A"
        if name=="Vanilla Call":
            bs_price=option.price_black_scholes(S0,r,sigma)
            bs_price_string=f"{bs_price:.4f}"
            difference=f"{abs(mc_price - bs_price):.4f}"

        print(f"{name:<35} | {mc_price:>15.4f} | {bs_price_string:>15} | {difference}")

    print("-"*95)
    print("NOTES D'ANALYSE :")
    print("1. Le prix du Call Vanille sert de benchmark pour valider la convergence de Monte-Carlo.")
    print("2. L'option Asiatique doit être moins chère que la Vanille (lissage de la volatilité).")
    print("3. La Lookback doit être l'option la plus chère (protection contre le regret).")
    print("4. La Barrier Out doit être moins chère que la Vanille (risque d'extinction).")
    print("="*95)
    
    #VISUALISATION (Le graphique des trajectoires)
    print("\nGénération du graphique des trajectoires...")
    
    #On récupère quelques trajectoires (les 50 premières)
    paths = sim.simulate_paths()
    plot_paths = paths[:50] 

    plt.figure(figsize=(12,7))
    
    #On trace les trajectoires simulées
    plt.plot(plot_paths.T,alpha=0.4,lw=1)
    
    #On trace la moyenne des trajectoires (la tendance centrale)
    plt.plot(np.mean(paths,axis=0),color='black',lw=3,label='Moyenne attendue (Drift)')
    
    #On ajoute les niveaux clés
    plt.axhline(S0,color='blue',linestyle='--',label='Prix initial S0')
    plt.axhline(K, color='red',linestyle='-',label='Strike K')
    plt.axhline(125,color='orange',linestyle=':',label='Barrière H (Up-and-Out)')

    plt.title(f"Simulation Monte-Carlo : 50 scénarios basés sur le GBM",fontsize=14)
    plt.xlabel("Pas de temps (Jours)",fontsize=12)
    plt.ylabel("Prix de l'actif sous-jacent (€)",fontsize=12)
    plt.legend(loc='upper left')
    plt.grid(True,alpha=0.2)
    
    plt.show()

if __name__ == "__main__":
    main()