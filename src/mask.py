def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты, скрывая первые 6 и последние 4 цифры.
    Формат: XXXX XX** **** XXXX

    Args:
        card_number (str): Номер банковской карты.

    Returns:
        str: Маскированный номер карты.
    """
    if not card_number.isdigit() or len(card_number) != 16:
        raise ValueError("Invalid card number")
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета, показывая только 2 звезды и последние 4 цифры.

    Args:
        account_number (str): Номер банковского счета.

    Returns:
        str: Маскированный номер счета.
    """
    if not account_number.isdigit() or len(account_number) < 5:
        raise ValueError("Invalid account number")
    return "*" * (len(account_number) - 4) + account_number[-4:]
