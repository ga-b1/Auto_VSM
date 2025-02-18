import unittest
from vsm.core.inventory_management import Inventaire

# Classe Dummy pour simuler un Produit.
class DummyProduit:
    def __init__(self, name: str):
        self.name = name
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        return isinstance(other, DummyProduit) and self.name == other.name
    def __repr__(self):
        return f"DummyProduit({self.name})"

class TestInventaire(unittest.TestCase):
    def setUp(self):
        self.inv = Inventaire()
        self.prod = DummyProduit("TestProduit")

    def test_add_product(self):
        self.inv.add_product(self.prod)
        self.assertIn(self.prod, self.inv.products)
        self.assertEqual(self.inv.products[self.prod], 0)

    def test_add_and_remove(self):
        self.inv.add_product(self.prod)
        self.inv.add(self.prod, 10)
        self.assertEqual(self.inv.products[self.prod], 10)
        self.inv.remove(self.prod, 4)
        self.assertEqual(self.inv.products[self.prod], 6)

    def test_remove_exception(self):
        self.inv.add_product(self.prod)
        with self.assertRaises(ValueError):
            self.inv.remove(self.prod, 1)

    def test_delete_product(self):
        self.inv.add_product(self.prod)
        # La quantité par défaut est 0, donc suppression possible.
        self.inv.delete_product(self.prod)
        self.assertNotIn(self.prod, self.inv.products)

    def test_is_empty(self):
        self.inv.add_product(self.prod)
        self.assertTrue(self.inv.is_empty(self.prod))
        self.inv.add(self.prod, 5)
        self.assertFalse(self.inv.is_empty(self.prod))

if __name__ == '__main__':
    unittest.main()
