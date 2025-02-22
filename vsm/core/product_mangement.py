

class Produit:
    id = 0
    def __init__(self):
        self.id = Produit.id
        Produit.id += 1

    def __str__(self):
        return f"Produit_{self.id}"
    