import pytest

from src.mask import get_mask_account, get_mask_card_number


@pytest.fixture
def valid_account_number():
    return "123456789123"


@pytest.fixture
def short_account_number():
    return "12345"


@pytest.fixture
def invalid_account_number():
    return "abcd"


@pytest.fixture
def valid_card_number():
    return "1234567891234567"


@pytest.fixture
def another_valid_card_number():
    return "0000111122223333"


@pytest.fixture
def short_card_number():
    return "12345678"


@pytest.fixture
def invalid_card_number():
    return "abcdabcdabcdabcd"


@pytest.mark.parametrize(
    "account_number,expected", [("123456789123", "**9123"), ("12345", None)]
)
def test_get_mask_account(account_number, expected):
    if expected is None:
        with pytest.raises(ValueError):
            get_mask_account(account_number)
    else:
        assert get_mask_account(account_number) == expected


@pytest.mark.parametrize("account_number", ["1234", "abcd"])
def test_get_mask_account_raises(account_number):
    with pytest.raises(ValueError):
        get_mask_account(account_number)


@pytest.mark.parametrize(
    "card_number,expected",
    [
        ("1234567891234567", "1234 **** **23 4567"),
        ("0000111122223333", "0000 **** **22 3333"),
    ],
)
def test_get_mask_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize("card_number", ["12345678", "abcdabcdabcdabcd"])
def test_get_mask_card_number_raises(card_number):
    with pytest.raises(ValueError):
        get_mask_card_number(card_number)
