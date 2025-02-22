from dataclasses import dataclass
from inventory_management import Inventaire
from product_mangement import Produit
from process import Process


SECURE_DELETE = True

@dataclass
class Facory_Process(Process):
    process_time: int
    efficiency: float
    
    def __init__(self):
        """
        Permet de creer un procees qui avec des produit (defini via la nomenclaure)
        crée d'autre en un temps donnée process_time et avec une efficacité
        
        limitation connue : impossible d'avoir un produit en in et en out 
        """
        super.__init__(self)
        self.nomenclature : dict[Produit,int]
        #nomenclaure : négatif => produit utile pour fabriqué; Positif => produit fabriqué
    
    
    def set_nomenclature_produit(self,produit : Produit, qte : int) -> bool:
        """permet de creer la le process de fabrication (A+B=>C+D)

        Args:
            produit (Produit): produit utile en in ou en out
            qte (int): positif out; négatif in

        Returns:
            bool: true tout est ok, false erreur lors de l'ajout
        """
        if not True:  #TODO check si le produit est deja present dans la nomenclature 
            #(si deja present dire qu'il exite deja)
            #TODO add log
            return False
        #TODO add log
        self.setup_inventory(produit)
        self.nomenclature[produit] = int
        return True
        
    
    def remove_nomenclature_produit(self,produit : Produit, secure_delete : bool = SECURE_DELETE) -> bool:
        """_summary_

        Args:
            produit (Produit): _description_
            secure_delete (bool, optional): _description_. Defaults to SECURE_DELETE.

        Returns:
            bool: _description_
        """
        #TODO add log        
        if secure_delete and self.inventaire_bdl.can_delede(produit):
            self.inventaire_bdl.is_empty(produit)
            #verifie que l'inventaire est vide avant de supprimé (que si secure_delete)
            return False
        
        if not produit in self.nomenclature:
            return False
        
        del self.nomenclature[produit]
        self.inventaire_bdl.delete(produit)
        return True
        
    
    
    
    
    
    
    
    

    
    def can_process(self) -> bool:
        for produit, quantite in self.need.items():
            if self.inventaire_bdl.get_quantity(produit) < quantite:
                return False
        return True
    
    def gobal_process(self) -> tuple[bool,float]:
        if not self.can_process():
            return False
        try:
            self.use_need()
        except ValueError:
            return False
        self.craft_produit()
        return True
    
    def multi_process(self, qte: int) -> int:
        count = 0
        for _ in range(qte):
            if not self.gobal_process():
                break
            count += 1
        return count
    
    
    def use_need(self):
        for produit, quantite in self.need.items():
            disponible = self.inventaire_bdl.get_quantity(produit)
            if disponible < quantite:
                raise ValueError(f"Quantité insuffisante de {produit} (nécessaire: {quantite}, disponible: {disponible})")
            self.inventaire_bdl.remove(produit, quantite)
    
    def craft_produit(self):
        for produit, quantite in self.prod.items():
            quantite_produite = quantite * self.efficiency // 100
            if quantite_produite > 0:
                self.inventaire_bdl.add(produit, quantite_produite)