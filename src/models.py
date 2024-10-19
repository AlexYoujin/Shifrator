from typing import List


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price}, quantity={self.quantity})"


class Category:
    # Атрибуты класса для подсчета категорий и товаров
    total_categories = 0
    total_products = 0

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.products: List[Product] = []

        # Увеличиваем количество категорий при создании нового объекта
        Category.total_categories += 1

    def add_product(self, product: Product):
        self.products.append(product)
        # Увеличиваем количество товаров при добавлении продукта
        Category.total_products += 1

    def __repr__(self):
        return f"Category(name='{self.name}', products={self.products})"
