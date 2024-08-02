import pytest

from src.processing import get_date
from src.widget import mask_account_card


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
def valid_mixed_input():
    return "Account 1234567890"


@pytest.fixture
def valid_card_input():
    return "Card 1234 5678 1234 5678"


@pytest.fixture
def invalid_input():
    return "invalid_input"


@pytest.fixture
def invalid_short_input():
    return "1234"


@pytest.fixture
def invalid_account_mixed_input():
    return "Account 1234"


@pytest.fixture
def invalid_alpha_input():
    return "Account abcdefghijklmnop"


@pytest.fixture
def valid_date():
    return "2024-03-11T02:26:18.671407"


@pytest.fixture
def another_valid_date():
    return "2021-12-25T15:00:00.000000"


@pytest.fixture
def invalid_date_format_1():
    return "2024-03-11"


@pytest.fixture
def invalid_date_format_2():
    return "11.03.2024T02:26:18.671407"


@pytest.fixture
def invalid_date_format_3():
    return "2024/03/11T02:26:18.671407"


@pytest.fixture
def completely_invalid_date():
    return "invalid_date"


@pytest.fixture
def invalid_month_date():
    return "2024-13-11T02:26:18.671407"


@pytest.fixture
def invalid_zero_month_date():
    return "2024-00-11T02:26:18.671407"


@pytest.fixture
def invalid_day_date():
    return "2024-03-32T02:26:18.671407"


@pytest.fixture
def invalid_hour_date():
    return "2024-03-11T25:26:18.671407"


@pytest.fixture
def invalid_minute_date():
    return "2024-03-11T02:61:18.671407"


@pytest.fixture
def invalid_second_date():
    return "2024-03-11T02:26:61.671407"


def test_mask_account_card(valid_card_number, valid_account_number, short_account_number, valid_mixed_input,
                           valid_card_input, invalid_input, invalid_short_input, invalid_account_mixed_input,
                           invalid_alpha_input):
    assert mask_account_card(valid_card_number) == "1234 56** **** 5678"
    assert mask_account_card(valid_account_number) == "******7890"
    assert mask_account_card(short_account_number) == "*2345"
    assert mask_account_card(valid_mixed_input) == "Account ******7890"
    assert mask_account_card(valid_card_input) == "Card 1234 56** **** 5678"
    with pytest.raises(ValueError):
        mask_account_card(invalid_input)
    with pytest.raises(ValueError):
        mask_account_card(invalid_short_input)
    with pytest.raises(ValueError):
        mask_account_card(invalid_account_mixed_input)
    with pytest.raises(ValueError):
        mask_account_card(invalid_alpha_input)


def test_get_date(valid_date, another_valid_date, invalid_date_format_1, invalid_date_format_2, invalid_date_format_3,
                  completely_invalid_date, invalid_month_date, invalid_zero_month_date, invalid_day_date,
                  invalid_hour_date, invalid_minute_date, invalid_second_date):
    assert get_date(valid_date) == "11.03.2024"
    assert get_date(another_valid_date) == "25.12.2021"
    with pytest.raises(ValueError):
        get_date(invalid_date_format_1)
    with pytest.raises(ValueError):
        get_date(invalid_date_format_2)
    with pytest.raises(ValueError):
        get_date(invalid_date_format_3)
    with pytest.raises(ValueError):
        get_date(completely_invalid_date)
    with pytest.raises(ValueError):
        get_date(invalid_month_date)
    with pytest.raises(ValueError):
        get_date(invalid_zero_month_date)
    with pytest.raises(ValueError):
        get_date(invalid_day_date)
    with pytest.raises(ValueError):
        get_date(invalid_hour_date)
    with pytest.raises(ValueError):
        get_date(invalid_minute_date)
    with pytest.raises(ValueError):
        get_date(invalid_second_date)
