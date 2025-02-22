from dataclasses import dataclass
from inventory_management import Inventaire
from product_mangement import Produit
from process import Process
import numpy as np


SECURE_DELETE = True


class Facory_Process(Process):

    def __init__(self, process_time : float, time_variability : float, quality : float):
        """
        Permet de creer un procees qui avec des produit (defini via la nomenclaure)
        crée d'autre en un temps donnée process_time et avec une efficacité
        
        limitation connue : impossible d'avoir un produit en in et en out 
        """
        super().__init__()
        self.process_time = process_time
        self.time_variability = time_variability
        self.quality = quality
        
        self.nomenclature : dict[Produit,int] = {}
        
        #nomenclaure : négatif => produit utile pour fabriqué; Positif => produit fabriqué
    
    
    def set_nomenclature_produit(self,produit : Produit, qte : int) -> bool:
        """permet de creer la le process de fabrication (A+B=>C+D)

        Args:
            produit (Produit): produit utile en in ou en out
            qte (int): positif out; négatif in

        Returns:
            bool: true tout est ok, false erreur lors de l'ajout
        """
        if produit in self.get_nomenclature():
            return False
        self.setup_inventory(produit)
        self.nomenclature[produit] = qte
        return True
  
        
    
    def remove_nomenclature_produit(self,produit : Produit, secure_delete : bool = SECURE_DELETE) -> bool:
        """_summary_

        Args:
            produit (Produit): _description_
            secure_delete (bool, optional): _description_. Defaults to SECURE_DELETE.

        Returns:
            bool: _description_
        """
        if produit not in self.nomenclature:
            return False
        if secure_delete and self.get_quantity(produit) != 0:
            return False
        del self.nomenclature[produit]
        self.delete_product(produit)
        return True
    
    def get_nomenclature(self) -> dict[Produit,int]:
        return self.nomenclature
    
    def get_process_time(self) -> int:
        return self.process_time
    
    def get_efficiency(self) -> float:
        return self.efficiency
    
    def get_batch_size(self) -> int:
        return self.batch_size
    
    def get_quality(self) -> float:
        return self.quality
    
    def _set_process_time(self, time : int) -> bool:
        self.process_time = time
        return True
    
    def _set_efficiency(self, efficiency : float) -> bool:
        self.efficiency = efficiency
        return True
    
    def _set_batch_size(self, batch_size : int) -> bool:
        self.batch_size = batch_size
        return True
    
    def can_process(self) -> bool:
        for produit, quantite in self.nomenclature.items():
            if quantite < 0 and abs(self.get_quantity(produit)) < abs(quantite):
                return False
            
        return True
    
    def craft(self) -> bool:
        if not self.can_process():
            return -1
        return self._craft_produit()
    
    def calcul_process_time(self) -> float:
        return self.process_time + np.random.normal(0,self.time_variability)
    
    def _craft_produit(self):
        #on fabrique (les valeur negative de la nomenclature sont les produit utile pour fabriquer)
        # (les valeurs positive sont les produit fabriqué)
        for produit, quantite in self.nomenclature.items():
            if quantite < 0:
                self.remove(produit, abs(quantite))
            if quantite > 0:
                self.add(produit, quantite)
        return self.calcul_process_time()
    
    def __repr__(self):
        # Affiche les attributs spécifiques de la factory process
        return (f"{self.__class__.__name__}(process_time={self.process_time}, "
                f"time_variability={self.time_variability}, quality={self.quality}, "
                f"nomenclature={self.nomenclature})")
                
    def __str__(self):
        # Crée une représentation de la nomenclature en utilisant str(product) pour chaque produit.
        nomenclature_str = ", ".join([f"{str(prod)}: {qte}" for prod, qte in self.nomenclature.items()])
        texte = f"""Factory Process:
        Process time: {self.process_time}
        Time variability: {self.time_variability}
        Quality: {self.quality}
        Nomenclature: {{{nomenclature_str}}}
        Inventaire: {self.inventaire_bdl}"""
        return texte
    
                

if __name__ == "__main__":
    factory = Facory_Process(process_time = 10, time_variability = 1, quality = 1)
    print(factory)

    prod1 = Produit()
    prod2 = Produit()
    prod3 = Produit()
    
    factory.add_product(prod1)
    factory.add_product(prod2)
    factory.add_product(prod3)
    
    factory.add(prod1, 10)
    factory.add(prod2, 10)
    factory.add(prod3, 10)
    
    print(factory)
    
    factory.set_nomenclature_produit(prod1, -1)
    factory.set_nomenclature_produit(prod2, -1)
    factory.set_nomenclature_produit(prod3, 2)
    
    print(factory)
    
    factory.craft()
    
    print(factory)
    
    factory.craft()









