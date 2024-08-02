import pytest

from src.widget import mask_account_card


# Фикстуры для тестов
@pytest.fixture
def valid_card_number():
    return "1234567812345678"


@pytest.fixture
def valid_account_number():
    return "1234567890"


@pytest.fixture
def short_account_number():
    return "12345"


@pytest.fixture
def valid_account_mixed_input():
    return "Account 1234567890"


@pytest.fixture
def valid_card_input():
    return "Card 1234 5678 1234 5678"


@pytest.fixture
def invalid_inputs():
    return [
        "invalid_input", "1234", "Account 1234", "Account abcdefghijklmnop"
    ]


# Параметризация входных данных и ожидаемых результатов
@pytest.mark.parametrize("input_str, expected", [
    ("1234567812345678", "1234 56** **** 5678"),
    ("1234567890", "******7890"),
    ("12345", "*2345"),
    ("Account 1234567890", "Account ******7890"),
    ("Card 1234 5678 1234 5678", "Card 1234 56** **** 5678")
])
def test_mask_account_card(input_str, expected) -> None:
    assert mask_account_card(input_str) == expected


@pytest.mark.parametrize("input_str", [
    "invalid_input", "1234", "Account 1234", "Account abcdefghijklmnop"
])
def test_mask_account_card_raises(input_str) -> None:
    with pytest.raises(ValueError):
        mask_account_card(input_str)


@pytest.mark.parametrize("date_str,expected", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2021-12-25T15:00:00.000000", "25.12.2021")
])
def test_get_date(date_str, expected):
    from src.processing import get_date
    assert get_date(date_str) == expected


@pytest.mark.parametrize("date_str", [
    "2024-03-11", "11.03.2024T02:26:18.671407", "2024/03/11T02:26:18.671407",
    "invalid_date", "2024-13-11T02:26:18.671407", "2024-00-11T02:26:18.671407",
    "2024-03-32T02:26:18.671407", "2024-03-11T25:26:18.671407", "2024-03-11T02:61:18.671407",
    "2024-03-11T02:26:61.671407", "", "2024-03-11T02:26", "2024-03-11T02:26:18", "2024-03-11T"
])
def test_get_date_raises(date_str):
    from src.processing import get_date
    with pytest.raises(ValueError):
        get_date(date_str)
