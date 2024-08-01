import pytest

from src.mask import get_mask_account, get_mask_card_number


def test_get_mask_account() -> None:
    assert get_mask_account("1234567890") == "******7890"
    assert get_mask_account("12345") == "*2345"
    with pytest.raises(ValueError):
        get_mask_account("1234")  # Слишком короткий номер
    with pytest.raises(ValueError):
        get_mask_account("abcd")  # Не числовой ввод


def test_get_mask_card_number() -> None:
    assert get_mask_card_number("1234567812345678") == "1234 56** **** 5678"
    assert get_mask_card_number("0000111122223333") == "0000 11** **** 3333"
    with pytest.raises(ValueError):
        get_mask_card_number("12345678")  # Слишком короткий номер
    with pytest.raises(ValueError):
        get_mask_card_number("abcdabcdabcdabcd")  # Не числовой ввод
