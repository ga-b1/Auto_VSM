from dataclasses import dataclass
from inventory_management import Inventaire
from product_mangement import Produit

@dataclass
class Process:
    
    
    def __init__(self):
        self.inventaire_bdl = Inventaire()
        
    def setup_inventory(self,produit : Produit):
        self.inventaire_bdl.add_product(produit)
 
    