import unittest
from unittest.mock import patch

import pytest

from src.processing import get_date
from src.widget import (extract_digits, extract_word_and_numbers, main,
                        mask_account_card)


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
    return ["invalid_input", "1234", "Account 1234", "Account abcdefghijklmnop"]


# Параметризация входных данных и ожидаемых результатов
@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("1234567812345678", "1234 56** **** 5678"),
        ("1234567890", "******7890"),
        ("12345", "*2345"),
        ("Account 1234567890", "Account ******7890"),
        ("Card 1234 5678 1234 5678", "Card 1234 56** **** 5678"),
    ],
)
def test_mask_account_card(input_str, expected) -> None:
    assert mask_account_card(input_str) == expected


def test_extract_words_and_numbers(valid_card_input):
    assert extract_word_and_numbers(valid_card_input) == ("Card", "1234567812345678")
    assert extract_word_and_numbers("") == ("", "")


def test_extract_digits(valid_card_input):
    assert extract_digits(valid_card_input) == "1234567812345678"


@pytest.mark.parametrize(
    "input_str", ["invalid_input", "1234", "Account 1234", "Account abcdefghijklmnop"]
)
def test_mask_account_card_raises(input_str) -> None:
    with pytest.raises(ValueError):
        mask_account_card(input_str)


"""Тест дат"""


@pytest.mark.parametrize(
    "date_str,expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2021-12-25T15:00:00.000000", "25.12.2021"),
    ],
)
def test_get_date(date_str, expected):
    assert get_date(date_str) == expected


@pytest.mark.parametrize(
    "invalid_date_str",
    [
        "2024-03-11",
        "11.03.2024T02:26:18.671407",
        "2024/03/11T02:26:18.671407",
        "invalid_date",
        "2024-13-11T02:26:18.671407",
        "2024-00-11T02:26:18.671407",
        "2024-03-32T02:26:18.671407",
        "2024-03-11T25:26:18.671407",
        "2024-03-11T02:61:18.671407",
        "2024-03-11T02:26:61.671407",
        "",
        "2024-03-11T02:26",
        "2024-03-11T02:26:18",
        "2024-03-11T",
    ],
)
def test_get_date_invalid(invalid_date_str):
    with pytest.raises(ValueError):
        get_date(invalid_date_str)


def test_valid_date():
    assert get_date("2023-08-04T14:23:45.123456") == "04.08.2023"
    assert get_date("2020-01-01T00:00:00.000000") == "01.01.2020"


def test_invalid_date_format():
    with pytest.raises(
            ValueError, match="Invalid date format, expected 'YYYY-MM-DDTHH:MM:SS.SSSSSS'"
    ):
        get_date("2023-08-04 14:23:45.123456")
    with pytest.raises(
            ValueError, match="Invalid date format, expected 'YYYY-MM-DDTHH:MM:SS.SSSSSS'"
    ):
        get_date("2023-08-04T14:23:45")
    with pytest.raises(
            ValueError, match="Invalid date format, expected 'YYYY-MM-DDTHH:MM:SS.SSSSSS'"
    ):
        get_date("04.08.2023T14:23:45.123456")
    with pytest.raises(
            ValueError, match="Invalid date format, expected 'YYYY-MM-DDTHH:MM:SS.SSSSSS'"
    ):
        get_date("2023/08/04T14:23:45.123456")


def test_invalid_date():
    with pytest.raises(ValueError, match="Invalid date"):
        get_date("2023-02-30T14:23:45.123456")
    with pytest.raises(ValueError, match="Invalid date"):
        get_date("2023-13-01T14:23:45.123456")
    with pytest.raises(ValueError, match="Invalid date"):
        get_date("2023-00-01T14:23:45.123456")
    with pytest.raises(ValueError, match="Invalid date"):
        get_date("2023-01-32T14:23:45.123456")


def test_get_date_valid():
    assert get_date("2023-07-21T12:34:56.123456") == "21.07.2023"


def test_get_date_invalid_format():
    with pytest.raises(
            ValueError, match="Invalid date format, expected 'YYYY-MM-DDTHH:MM:SS.SSSSSS'"
    ):
        get_date("2023/07/21 12:34:56.123456")


def test_get_date_invalid_date():
    with pytest.raises(ValueError, match="Invalid date"):
        get_date("2023-13-21T12:34:56.123456")


class TestMain(unittest.TestCase):

    @patch('builtins.input', side_effect=["2024-03-11T02:26:18.671407", "1234567812345678", "exit"])
    @patch('builtins.print')
    def test_main_mask_card(self, mock_print, mock_input):
        main()
        mock_print.assert_any_call("Форматированная дата: 11.03.2024")
        mock_print.assert_any_call("Замаскированные данные: 1234 56** **** 5678")


if __name__ == '__main__':
    unittest.main()
