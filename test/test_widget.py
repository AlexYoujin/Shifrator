import pytest

from src.processing import get_date
from src.widget import mask_account_card


def test_mask_account_card() -> None:
    assert mask_account_card("1234567812345678") == "1234 56** **** 5678"
    assert mask_account_card("1234567890") == "******7890"
    assert mask_account_card("12345") == "*2345"
    assert mask_account_card("Account 1234567890") == "Account ******7890"
    assert mask_account_card("Card 1234 5678 1234 5678") == "Card 1234 56** **** 5678"
    with pytest.raises(ValueError):
        mask_account_card("invalid_input")
    with pytest.raises(ValueError):
        mask_account_card("1234")
    with pytest.raises(ValueError):
        mask_account_card("Account 1234")
    with pytest.raises(ValueError):
        mask_account_card("Account abcdefghijklmnop")


def test_get_date() -> None:
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
    assert get_date("2021-12-25T15:00:00.000000") == "25.12.2021"
    with pytest.raises(ValueError):
        get_date("2024-03-11")
    with pytest.raises(ValueError):
        get_date("11.03.2024T02:26:18.671407")
    with pytest.raises(ValueError):
        get_date("2024/03/11T02:26:18.671407")
    with pytest.raises(ValueError):
        get_date("invalid_date")
    with pytest.raises(ValueError):
        get_date("2024-13-11T02:26:18.671407")
    with pytest.raises(ValueError):
        get_date("2024-00-11T02:26:18.671407")
    with pytest.raises(ValueError):
        get_date("2024-03-32T02:26:18.671407")
    with pytest.raises(ValueError):
        get_date("2024-03-11T25:26:18.671407")
    with pytest.raises(ValueError):
        get_date("2024-03-11T02:61:18.671407")
    with pytest.raises(ValueError):
        get_date("2024-03-11T02:26:61.671407")
