from typing import NoReturn


def TokenInvalid() -> NoReturn:
    """Ошибка получения токена Telegram"""
    print("Your Telegram token is invalid!")
    exit(1)
