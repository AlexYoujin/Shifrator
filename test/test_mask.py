import pytest

from src.mask import get_mask_account, get_mask_card_number


@pytest.fixture
def valid_account_number():
    return "1234567890"


@pytest.fixture
def short_account_number():
    return "12345"


@pytest.fixture
def invalid_account_number():
    return "abcd"


@pytest.fixture
def valid_card_number():
    return "1234567812345678"


@pytest.fixture
def another_valid_card_number():
    return "0000111122223333"


@pytest.fixture
def short_card_number():
    return "12345678"


@pytest.fixture
def invalid_card_number():
    return "abcdabcdabcdabcd"


def test_get_mask_account(valid_account_number, short_account_number, invalid_account_number):
    assert get_mask_account(valid_account_number) == "******7890"
    assert get_mask_account(short_account_number) == "*2345"
    with pytest.raises(ValueError):
        get_mask_account("1234")  # Слишком короткий номер
    with pytest.raises(ValueError):
        get_mask_account(invalid_account_number)  # Не числовой ввод


def test_get_mask_card_number(valid_card_number, another_valid_card_number, short_card_number, invalid_card_number):
    assert get_mask_card_number(valid_card_number) == "1234 56** **** 5678"
    assert get_mask_card_number(another_valid_card_number) == "0000 11** **** 3333"
    with pytest.raises(ValueError):
        get_mask_card_number(short_card_number)  # Слишком короткий номер
    with pytest.raises(ValueError):
        get_mask_card_number(invalid_card_number)  # Не числовой ввод
