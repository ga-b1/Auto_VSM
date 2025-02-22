from dataclasses import dataclass
from inventory_management import Inventaire
from product_mangement import Produit


class Process:
    """Permet de créer un process qui est la base pour factory_process et storage_process."""
    
    def __init__(self, name: str = "Process"):
        self.name = name                # nouvel attribut pour le nom
        self.inventaire_bdl = Inventaire()
        
    def setup_inventory(self, produit: Produit):
        self.inventaire_bdl.add_product(produit)
 
    def add_product(self, produit: Produit):
        self.inventaire_bdl.add_product(produit)
        
    def add(self, produit: Produit, qte: int):
        self.inventaire_bdl.add(produit, qte)
        
    def remove(self, produit: Produit, qte: int):
        self.inventaire_bdl.remove(produit, qte)
        
    def delete_product(self, produit: Produit):
        self.inventaire_bdl.delete_product(produit)
        
    def is_empty(self, produit: Produit) -> bool:
        return self.inventaire_bdl.is_empty(produit)
    
    def get_quantity(self, produit: Produit) -> int:
        return self.inventaire_bdl.get_quantity(produit)
    
    def can_delede(self, produit: Produit) -> bool:
        return self.inventaire_bdl.can_delede(produit)
    
    def get_products(self) -> dict[Produit, int]:
        return self.inventaire_bdl.get_products()

    # Méthodes pour gérer le nom du process
    def get_name(self) -> str:
        return self.name
    
    def set_name(self, name: str) -> None:
        self.name = name

    # Méthode pour construire l'arbre (tree) du process.
    def to_tree(self) -> str:
        # Retourne une représentation simple ; à enrichir dans les classes filles si besoin.
        return f"{self.name}"
    
    def __repr__(self):
        return f"Process(name={self.name}, inventory={self.inventaire_bdl})"
    
    def __str__(self):
        return f"Process: {self.name} - {self.inventaire_bdl}"
    
    def __eq__(self, other):
        return isinstance(other, Process) and self.inventaire_bdl == other.inventaire_bdl and self.name == other.name

    def __hash__(self):
        # On utilise l'identifiant de l'objet pour le hash.
        return id(self)
    

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
