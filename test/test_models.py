import pytest
from src.models import Product, Category


# Фикстуры для тестирования
@pytest.fixture
def sample_product():
    return Product(name="Молоко", description="Коровье молоко", price=1.5, quantity=100)


@pytest.fixture
def sample_category():
    return Category(name="Молочные продукты", description="Все молочные продукты")


def test_product_initialization(sample_product):
    """Тест на проверку корректной инициализации объекта Product"""
    assert sample_product.name == "Молоко"
    assert sample_product.description == "Коровье молоко"
    assert sample_product.price == 1.5
    assert sample_product.quantity == 100


def test_category_initialization(sample_category):
    """Тест на проверку корректной инициализации объекта Category"""
    assert sample_category.name == "Молочные продукты"
    assert sample_category.description == "Все молочные продукты"
    assert isinstance(sample_category.products, list)  # Проверяем, что это список
    assert len(sample_category.products) == 0  # Проверяем, что список товаров пуст в начале


def test_category_and_product_count():
    """Тест на подсчет количества категорий и продуктов"""
    # Обнуляем атрибуты перед тестом
    Category.total_categories = 0
    Category.total_products = 0

    category1 = Category(name="Молочные продукты", description="Все молочные продукты")
    category2 = Category(name="Выпечка", description="Все виды хлеба")

    assert Category.total_categories == 2  # Проверяем количество категорий

    product1 = Product(name="Молоко", description="Коровье молоко", price=1.5, quantity=100)
    product2 = Product(name="Хлеб", description="Батон белого хлеба", price=0.8, quantity=50)

    category1.add_product(product1)
    category2.add_product(product2)

    assert Category.total_products == 2  # Проверяем количество товаров


def test_add_product_to_category(sample_category, sample_product):
    """Тест на добавление продукта в категорию"""
    sample_category.add_product(sample_product)
    assert len(sample_category.products) == 1  # Проверяем, что продукт добавлен
    assert sample_category.products[0] == sample_product  # Проверяем, что это тот же продукт
