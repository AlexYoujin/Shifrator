import pytest

from src.processing import create_payment_dict, sort_payment_dates


@pytest.fixture
def payments():
    return [
        {"date": "2024-03-11T02:26:18.671407", "amount": "100"},
        {"date": "2024-03-11T10:15:30.123456", "amount": "200"},
        {"date": "2024-03-12T08:00:00.000000", "amount": "300"},
    ]


@pytest.fixture
def payment_dict():
    return {
        "11.03.2024": [
            {"date": "2024-03-11T02:26:18.671407", "amount": "100"},
            {"date": "2024-03-11T10:15:30.123456", "amount": "200"},
        ],
        "12.03.2024": [
            {"date": "2024-03-12T08:00:00.000000", "amount": "300"},
        ],
    }


def test_create_payment_dict(payments):
    result = create_payment_dict(payments)
    expected = {
        "11.03.2024": [
            {"date": "2024-03-11T02:26:18.671407", "amount": "100"},
            {"date": "2024-03-11T10:15:30.123456", "amount": "200"},
        ],
        "12.03.2024": [
            {"date": "2024-03-12T08:00:00.000000", "amount": "300"},
        ],
    }
    assert result == expected


def test_sort_payment_dates(payment_dict):
    result = sort_payment_dates(payment_dict)
    expected = ["11.03.2024", "12.03.2024"]
    assert result == expected
