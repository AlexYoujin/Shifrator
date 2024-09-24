from src.decorators import log


@log("masks")
def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.

    :param card_number: Номер банковской карты.
    :return: Маскированный номер карты.
    :raises ValueError: Если номер карты не является числовым или слишком коротким.
    """
    if not card_number.isdigit() or len(card_number) < 16:
        raise ValueError("Invalid card number")

    # Первые 4 цифры
    start = card_number[:4]
    # Средние цифры маскируются
    middle = "**** **" + card_number[10:12]
    # Последние 4 цифры остаются видимыми
    end = card_number[-4:]

    # Форматируем строку
    masked_part = f"{start} {middle} {end}"

    return masked_part


@log("masks")
def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета.

    :param account_number: Номер банковского счета.
    :return: Маскированный номер счета.
    :raises ValueError: Если номер счета не является числовым или слишком коротким.
    """
    if not account_number.isdigit() or len(account_number) < 6:
        raise ValueError("Invalid account number")

    masked_part = '**' + account_number[-4:]
    return masked_part
