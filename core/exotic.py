import numpy as np 
from core.base import Option

class AsianOption(Option) :
    """
    Cette classe implémente le calcul du payoff pour une option asiatique (path-dependent).
    
    À la différence des options européennes classiques, le gain d'une option asiatique 
    dépend de la moyenne des prix de l'actif sous-jacent observés durant toute la durée 
    de vie de l'option, plutôt que du seul prix à l'échéance.
    
    Cette approche permet de lisser la volatilité et de réduire le risque de manipulation 
    du cours du sous-jacent à la date de clôture.
    """
    
    def __init__(self,strike,expiry,premium=0.0,is_call=True,average_type='arithmetic') :
        super().__init__(strike,expiry,premium)
        self.is_call=is_call
        self.average_type=average_type
        
    
    def payoff(self,spot) :
        """
        Calcule le payoff de l'option asiatique en fonction de la moyenne 
        du chemin des prix (Path-Dependent).
        """
       #Calcul de la valeur de référence (moyenne des prix observés)
        if self.average_type=='arithmetic' :
            moyenne=np.mean(spot,axis=1)
        elif self.average_type=='geometric' :
            moyenne=np.exp(np.mean(np.log(spot),axis=1))
        #Calcul du gain final selon la direction du contrat (Call ou Put)
        if self.is_call :
            return np.maximum(0,moyenne-self.K)
        else :
            return np.maximum(0,self.K-moyenne)
        
class BarrierOption(Option) :
    """
    Cette classe implémente le calcul du payoff pour une option à barrière (path-dependent).
    L'activation (Knock-in) ou la désactivation (Knock-out) du contrat dépend du franchissement 
    d'un seuil de prix (H) durant la période de détention.
    """
    
    def __init__(self,strike,expiry,barrier,premium=0.0,is_call=True,is_knock_in=True,is_up=True) :
        super().__init__(strike,expiry,premium)
        self.is_call=is_call
        self.barrier=barrier
        self.is_knock_in=is_knock_in
        self.is_up=is_up
        
    def payoff(self,spot) :
        #Détermine si la barrière a été franchie
        if self.is_up :
            has_hit_barrier=np.max(spot,axis=1)>=self.barrier
        else :
            has_hit_barrier=np.min(spot,axis=1)<=self.barrier
            
        #Détermine si l'option est vivante 
        #Si knock_in seulement si la barrière est franchie
        #Si knock_out seulement si la barrière n'est pas franchie
        if self.is_knock_in :
            is_active=has_hit_barrier
        else :
            is_active=~has_hit_barrier #~ équivalent à not pour un tableau
        
        #Calcul du payoff 
        last_prices=spot[:,-1]
        if self.is_call :
            payoff_si_vivante=np.maximum(0,last_prices-self.K)
        else :
            payoff_si_vivante=np.maximum(0,self.K-last_prices)
        return np.where(is_active,payoff_si_vivante,0.0)
            
            
class LookBackOption(Option) :
    """
    Cette classe implémente l'option Lookback (path-dependent).
    Elle permet de réduire le risque de timing en utilisant les prix extrêmes 
    (maximum ou minimum) atteints par l'actif durant la période.
    
    Types supportés :
    - 'Fixe' : On compare un extrême au Strike K.
    - 'Flottant' : Le Strike est remplacé par l'extrême atteint.
    """
    
    def __init__(self,strike,expiry,premium=0.0,is_call=True,type_option='Flottant') :
        super().__init__(strike,expiry,premium)
        self.is_call=is_call
        self.type_option=type_option

    def payoff(self,spot) :
        if self.type_option=='Fixe' :
            if self.is_call :
                return np.maximum(0,np.max(spot,axis=1)-self.K)
            else :
                return np.maximum(0,self.K-np.min(spot,axis=1))
        elif self.type_option=='Flottant' :
            s_final=spot[:,-1]
            if self.is_call :
                return s_final-np.min(spot,axis=1)
            else :
                return np.max(spot,axis=1)-s_final

class ChooserOption(Option) :
    """
    Cette classe implémente l'option Chooser.
    
    À une date prédéterminée (choice_index), le détenteur décide si l'option 
    devient un Call ou un Put européen avec le même strike et la même échéance.
    C'est un produit particulièrement utile en période de forte incertitude sur 
    la direction du marché.
    """
    
    def __init__(self,strike,expiry,choice_index,premium=0.0) :
        super().__init__(strike,expiry,premium)
        self.choice_index=choice_index
    
    def payoff(self,spot):
        price_at_choice=spot[:,self.choice_index]
        s_final=spot[:,-1]
        call_payoff=np.maximum(0,s_final-self.K)
        put_payoff=np.maximum(0,self.K-s_final)
        return np.where(price_at_choice>self.K,call_payoff,put_payoff)
            

class BinaryOption(Option) :
    """
    Cette classe implémente l'option binaire (ou digitale).
    Contrairement aux options classiques, elle ne verse pas la différence de prix,
    mais un montant fixe (payout) si l'option expire dans la monnaie (In-the-money).
    """
    
    def __init__(self,strike,expiry,payout,premium=0.0,is_call=True) :
        super().__init__(strike,expiry,premium)
        self.payout=payout
        self.is_call=is_call
        
    def payoff(self,spot) :
        s_final=spot[:,-1]
        if self.is_call :
            return np.where(s_final>self.K,self.payout,0.0)
        else:
            return np.where(s_final<self.K,self.payout,0.0)
            
    
class ForwardStartOption(Option) :
    """
    Cette classe implémente l'option Forward Start.
    Le prix d'exercice (Strike) n'est pas fixé à l'origine mais est déterminé 
    à une date intermédiaire (fixing_index) en fonction du cours du sous-jacent.
    """
    
    def __init__(self,expiry,fixing_index,premium=0.0,is_call=True) :
        super().__init__(0.0,expiry,premium)
        self.fixing_index=fixing_index
        self.is_call=is_call
        
        
    def payoff(self,spot) :
        s_final=spot[:,-1]
        K_dynamique=spot[:,self.fixing_index]
        if self.is_call :
            return np.maximum(0,s_final-K_dynamique)
        else :
            return np.maximum(0,K_dynamique-s_final)
        
        
        
        
