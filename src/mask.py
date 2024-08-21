from decorators import log


@log()
def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты, показывая первые 6 и последние 4 цифры.
    Формат: XXXX XX** **** XXXX

    Args:
        card_number (str): Номер банковской карты.

    Returns:
        str: Маскированный номер карты.
    """
    if not card_number.isdigit() or len(card_number) != 16:
        raise ValueError("Invalid card number")
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


@log()
def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета, оставляя только последние 4 цифры.
    Формат: **XXXX

    :param account_number: Полный номер счета.
    :return: Замаскированный номер счета.
    """
    if not account_number.isdigit() or len(account_number) < 4:
        raise ValueError("Invalid account number")

    masked_account = f"**{account_number[-4:]}"
    return masked_account
