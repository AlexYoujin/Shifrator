import pytest

from src.decorators import log


# Тест успешного выполнения функции с логированием в консоль
@pytest.mark.usefixtures("caplog")
def test_log_success(caplog):
    @log("test")
    def add(x, y):
        return x + y

    result = add(1, 2)
    assert result == 3

    # Проверяем наличие нужных сообщений в логе
    assert "Function add started" in caplog.text
    assert "Function add ended" in caplog.text
    assert "Result: 3" in caplog.text


@pytest.mark.usefixtures("caplog")
def test_log_exception(caplog):
    @log("test")
    def divide(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    # Проверяем наличие нужных сообщений в логе
    assert "Function divide started" in caplog.text
    assert "Function divide failed" in caplog.text
    assert "Error: division by zero" in caplog.text
