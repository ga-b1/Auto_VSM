from dataclasses import dataclass
from inventory_management import Inventaire
from product_mangement import Produit

@dataclass
class Process:
    """Permet de creer un process qui est la base pour factory_process et storage_process
    """
    
    def __init__(self):
        self.inventaire_bdl = Inventaire()
        
    def setup_inventory(self,produit : Produit):
        self.inventaire_bdl.add_product(produit)
 
    def add_product(self,produit : Produit):
        self.inventaire_bdl.add_product(produit)
        
    def add(self,produit : Produit, qte : int):
        self.inventaire_bdl.add(produit,qte)
        
    def remove(self,produit : Produit, qte : int):
        self.inventaire_bdl.remove(produit,qte)
        
    def delete_product(self,produit : Produit):
        self.inventaire_bdl.delete_product(produit)
        
    def is_empty(self,produit : Produit) -> bool:
        return self.inventaire_bdl.is_empty(produit)
    
    def get_quantity(self,produit : Produit) -> int:
        return self.inventaire_bdl.get_quantity(produit)
    
    def can_delede(self,produit : Produit) -> bool:
        return self.inventaire_bdl.can_delede(produit)
    
    def get_products(self) -> dict[Produit, int]:
        return self.inventaire_bdl.get_products()
    
    def __repr__(self):
        return f"Process({self.inventaire_bdl})"
    
    def __str__(self):
        return f"Process: {self.inventaire_bdl}"
    
    def __eq__(self, other):
        return isinstance(other, Process) and self.inventaire_bdl == other.inventaire_bdl


if __name__ == "__main__":
    proc = Process()
    prod = Produit()
    proc.add_product(prod)
    print(proc)
    proc.add(prod, 10)
    print(proc)
    proc.remove(prod, 4)
    print(proc)
    print(proc.get_quantity(prod))
    print(proc.can_delede(prod))
    proc.remove(prod, 6)
    print(proc.can_delede(prod))
    print(proc)
    
    proc.delete_product(prod)
    print(proc)
    
    print(proc.is_empty(prod))
    print(proc.get_quantity(prod))
    