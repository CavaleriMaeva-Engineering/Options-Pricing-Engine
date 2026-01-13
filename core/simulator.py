import numpy as np

class GBMSimulator :
    """
    Simulateur de trajectoires de prix basé sur le modèle du Mouvement Brownien Géométrique (GBM).
    
    Ce simulateur génère des scénarios de prix futurs dans un univers 'risque-neutre',
    où le drift de l'actif correspond au taux sans risque (r).
    """
    
    def __init__(self,S0,r,sigma,T,num_steps,num_simulations) :
        """
        Args : 
            - S0 (float): Prix initial de l'actif (Spot à t=0).
            - r (float): Taux d'intérêt sans risque annuel (continu).
            - sigma (float): Volatilité annuelle du sous-jacent.
            - T (float): Temps total jusqu'à l'échéance (en années).
            - num_steps (int): Nombre de pas de temps (discrétisation).
            - num_simulations (int): Nombre de scénarios à générer.
        """
        self.S0=S0
        self.r=r
        self.sigma=sigma
        self.T=T
        self.num_steps=num_steps
        self.num_simulations=num_simulations
        self.dt=self.T/self.num_steps
        
    
    def simulate_paths(self) :
        #Génération de chocs aléatoires que l'on stocke dans la matrice Z
        Z=np.random.standard_normal((self.num_simulations,self.num_steps))
        
        #Calcul des rendements logarithmiques (formule du GBM)
        drift=(self.r-0.5*self.sigma**2)*self.dt
        diffusion=self.sigma*np.sqrt(self.dt)*Z
        
        #Grâce à ces rendements on construit le facteur de croissance journalier
        daily_growth=np.exp(drift+diffusion)
        
        #Construction de la trajectoire
        #On commence par une colonne de 1 pour représenter le prix au temps t=0 qui vaut S0/S0
        starting_column=np.ones((self.num_simulations,1))
        full_growth_matrix=np.hstack([starting_column, daily_growth])
        
        #Calcul de la matrice paths où :
            #chaque ligne est un scénario de vie de l'action
            #chaque colonne est un instantané du prix à un moment donné
        paths=self.S0*np.cumprod(full_growth_matrix,axis=1)
        return paths