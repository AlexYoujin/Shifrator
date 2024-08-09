import pytest

from src.decorators import log


# Тест успешного выполнения функции с логированием в консоль
def test_log_success(capsys):
    @log()
    def add(x, y):
        return x + y

    result = add(1, 2)
    assert result == 3

    captured = capsys.readouterr()
    assert "Function add started" in captured.out
    assert "Function add ended" in captured.out
    assert "Result: 3" in captured.out


# Тест возникновения исключения с логированием в консоль
def test_log_exception(capsys):
    @log()
    def divide(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()
    assert "Function divide started" in captured.out
    assert "Function divide failed" in captured.out
    assert "Error: division by zero" in captured.out
