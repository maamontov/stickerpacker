from os import getenv


class Config:
    def __init__(self) -> None:
        self.bot_token = getenv("BOT_TOKEN")
        self.bot_name = getenv("BOT_NAME")
        self.sticker_set_title = (
            f"⭐ {getenv('STICKER_SET_TITLE', 'Избранные стикеры')}"
        )
