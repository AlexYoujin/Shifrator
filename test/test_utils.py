import os
import unittest
from unittest.mock import mock_open, patch

from dotenv import load_dotenv

from src.external_api import convert_to_rubles
from src.utils import read_transactions


class TestUtils(unittest.TestCase):
    def setUp(self):
        """Настройка перед каждым тестом"""
        # Загрузка переменных окружения из .env для использования в тестах
        load_dotenv()

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='[{"id": 1, "amount": 100, "currency": "USD"}]',
    )
    def test_read_transactions(self, mock_file):
        """Тест на чтение данных из JSON файла"""
        file_path = project_root / 'data' / 'operations.json'
        transactions = read_transactions(file_path)
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["id"], 1)
        self.assertEqual(transactions[0]["amount"], 100)
        self.assertEqual(transactions[0]["currency"], "USD")

    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    def test_read_empty_transactions(self, mock_file):
        """Тест на чтение пустого JSON файла"""
        file_path = "data/empty.json"
        transactions = read_transactions(file_path)
        self.assertEqual(transactions, [])

    @patch("requests.get")
    def test_convert_to_rubles(self, mock_get):
        """Тест на конвертацию валюты в рубли с использованием внешнего API"""
        mock_response = {
            "success": True,
            "query": {"from": "USD", "to": "RUB", "amount": 100},
            "result": 7400.0,
        }

        # Настройка mock для requests.get
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        transaction = {"id": 1, "amount": 100, "currency": "USD"}
        api_key = os.getenv("API_KEY")

        amount_in_rubles = convert_to_rubles(transaction, api_key)
        self.assertIsInstance(amount_in_rubles, float)
        self.assertEqual(amount_in_rubles, 7400.0)
        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/convert",
            headers={"apikey": api_key},
            params={"from": "USD", "to": "RUB", "amount": 100},
        )


if __name__ == "__main__":
    unittest.main()
