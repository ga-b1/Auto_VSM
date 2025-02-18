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
        # Ajoute la quantité qte au produit (initialise si nécessaire).
        if produit not in self.products:
            self.add_product(produit)
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
        # Supprime complètement le produit du dictionnaire.
        if produit in self.products:
            del self.products[produit]

    def is_empty(self, produit: Produit) -> bool:
        # Retourne True si le produit n'existe pas ou si sa quantité est 0.
        return self.products.get(produit, 0) == 0