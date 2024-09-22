from src.decorators import log


@log("masks")
def get_mask_card_number(card_number: str) -> str:
    if not card_number.isdigit() or len(card_number) < 16:
        raise ValueError("Invalid card number")

    # Первые 4 цифры
    start = card_number[:4]
    # Средние цифры маскируются
    middle = "**** **" + card_number[10:12]
    # Последние 6 цифр остаются видимыми
    end = card_number[-4:]

    # Форматируем строку
    masked_part = f"{start} {middle} {end}"

    return masked_part


@log("masks")
def get_mask_account(account_number: str) -> str:
    if not account_number.isdigit() or len(account_number) < 6:
        raise ValueError("Invalid account number")

    masked_part = '**' + account_number[-4:]
    return masked_part
