def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты, скрывая первые 6 и последние 4 цифры.
    Формат: XXXX XX** **** XXXX

    Args:
        card_number (str): Номер банковской карты.

    Returns:
        str: Маскированный номер карты.
    """
    card_number = str(card_number)
    length = len(card_number)

    if length != 16:
        raise ValueError("Номер банковской карты должен содержать 16 цифр")

    return card_number[:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета, показывая только 2 звезды и последние 4 цифры.

    Args:
        account_number (str): Номер банковского счета.

    Returns:
        str: Маскированный номер счета.
    """
    account_number = str(account_number)
    length = len(account_number)

    if length <= 4:
        # Если номер счета <= 4, вернуть без изменений
        return account_number
    else:
        # Вернуть 2 звезды и последние 4 цифры
        return "**" + account_number[-4:]
