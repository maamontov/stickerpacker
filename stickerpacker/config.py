from os import getenv


class Config:
    def __init__(self) -> None:
        self.bot_token = getenv("BOT_TOKEN")
        self.bot_name = getenv("BOT_NAME")
        self.emoji = getenv("EMOJI", "⭐️")
        self.sticker_set_title = (
            f"{self.emoji} "
            f"{getenv('STICKER_SET_TITLE', 'Избранные стикеры')}",
        )
