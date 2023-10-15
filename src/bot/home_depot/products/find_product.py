"""imports"""
from .login import HomeDepotLogin


class HomeDepotFindProduct(HomeDepotLogin):
    """A class for finin out"""

    def find_product(self, product_name:str):
        """function for finding products and adding to cart"""
