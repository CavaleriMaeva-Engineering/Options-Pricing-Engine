import numpy as np

class GBMSimulator :
    """
    Cette classe implémente le simulateur de Mouvement Brownien Géométrique (GBM).
    
    Elle permet de générer des trajectoires de prix pour un actif sous-jacent de manière 
    vectorisée avec NumPy. Ces simulations servent de base au pricing par la méthode 
    de Monte-Carlo pour les options dépendantes du sentier (Path-Dependent).

    Attributs:
        S0 (float): Prix initial de l'actif (Spot).
        r (float): Taux d'intérêt sans risque annuel (Drift).
        sigma (float): Volatilité annuelle du sous-jacent (Diffusion).
        T (float): Horizon temporel en années.
        num_steps (int): Nombre de pas de discrétisation temporelle.
        num_simulations (int): Nombre de scénarios (mondes parallèles) à générer.
    """
    
    def __init__(self,S0,r,sigma,T,num_steps,num_simulations) :
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