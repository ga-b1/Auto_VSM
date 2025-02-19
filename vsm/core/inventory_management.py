from product_mangement import Produit

class Inventaire:
    def __init__(self):
        # Initialisation d'un dictionnaire pour stocker les produits et leurs quantités
        self.products: dict[Produit, int] = {}
    
    def add_product(self, produit: Produit):
        # Initialise le produit avec une quantité de 0 si inexistant.
        if produit not in self.products:
            self.products[produit] = 0

    def add(self, produit: Produit, qte: int):
        if produit not in self.products:
            raise KeyError(f"Le produit {produit} n'existe pas dans l'inventaire.")
        self.products[produit] += qte

    def remove(self, produit: Produit, qte: int):
        # Retire la quantité qte du produit, en vérifiant que la quantité disponible est suffisante.
        if produit not in self.products or self.products[produit] < qte:
            raise ValueError(f"Quantité insuffisante pour le produit {produit}.")
        self.products[produit] -= qte

    def delete_product(self, produit: Produit):
        # Vérifie que la quantité du produit est 0 avant suppression.
        if self.products.get(produit, 0) != 0:
            raise ValueError(f"Impossible de supprimer {produit}: la quantité n'est pas nulle ({self.products.get(produit)}).")
        if produit in self.products:
            del self.products[produit]

    def is_empty(self, produit: Produit) -> bool:
        # Retourne True si le produit n'existe pas ou si sa quantité est 0.
        return self.products.get(produit, 0) == 0

    def get_quantity(self, produit: Produit) -> int:
        # Retourne la quantité du produit, 0 si le produit n'existe pas.
        return self.products.get(produit, 0)
    
    def can_delede(self, produit: Produit) -> bool:
        # Retourne True si la quantité du produit est 0.
        return self.products.get(produit, 0) == 0
    
    def set_product(self, produit: Produit):
        # Ajoute le produit à l'inventaire avec une quantité de 0.
        self.products[produit] = 0
        
    def get_products(self) -> dict[Produit, int]:
        # Retourne une copie du dictionnaire de produits.
        return self.products.copy()
    
    def __repr__(self):
        return f"Inventaire({self.products})"

    def __str__(self):
        return f"Inventaire: {self.products}"
    
    def __eq__(self, other):
        return isinstance(other, Inventaire) and self.products == other.products
    
    def __hash__(self):
        return hash(tuple(sorted(self.products.items())))
    
    def __bool__(self):
        return bool(self.products)
    
    def __len__(self):
        return len(self.products)
    
    def __contains__(self, produit: Produit):
        return produit in self.products
    
    def __iter__(self):
        return iter(self.products)
    
    def __getitem__(self, produit: Produit):
        return self.products[produit]
    
    def __setitem__(self, produit: Produit, qte: int):
        self.products[produit] = qte
        
    def __delitem__(self, produit: Produit):
        del self.products[produit]
            
        
if __name__ == "__main__":
    inv = Inventaire()
    prod = Produit()
    inv.add_product(prod)
    print(inv)
    inv.add(prod, 10)
    print(inv)
    inv.remove(prod, 4)
    print(inv)
    inv.remove(prod, 6)
    
    inv.delete_product(prod)
    print(inv)
    
    print(inv.is_empty(prod))
    print(inv.get_quantity(prod))
    print(inv.can_delede(prod))
    print(inv.get_products())
    print(len(inv))
    print(prod in inv)
    print([p for p in inv])
    print(inv[prod])
    inv[prod] = 5
    print(inv[prod])
    del inv[prod]
    print(inv)
    print(bool(inv))
    inv.add_product(prod)
    print(inv)

        