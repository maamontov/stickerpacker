import asyncio
import logging
from typing import Optional

from aiogram import Bot, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    InputSticker,
    Message,
    ReplyKeyboardRemove,
    Sticker,
    StickerSet,
)
from config import Config
from utils import get_banner, get_logging_config

dispatcher = Dispatcher()
config = Config()
bot = Bot(config.bot_token)


class States(StatesGroup):
    remove = State()
    remove_all = State()


# ------------------------------------------------------------------------------


# --- /start ---
@dispatcher.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state()
    await message.answer(
        (
            "👋 Для начала работы просто отправьте (или перешлите) "
            "любой статичный стикер!\nВы получите ссылку на свой набор и "
            "сможете в любое время расширить его."
        ),
        reply_markup=ReplyKeyboardRemove(),
    )


# --- /get_link ---
@dispatcher.message(Command("get_link"))
async def command_getlink_handler(message: Message) -> None:
    sticker_set_name = await get_sticker_set_name(message.from_user.id)
    sticker_set = await get_sticker_set(sticker_set_name)

    if sticker_set is None:
        await message.answer(
            "☹️ У Вас еще не создан набор.\n"
            "Для начала работы просто отправьте (или перешлите) любой "
            "статичный стикер!",
        )
        return

    await message.answer(
        f"🙌 Ваш набор!\n{await get_sticker_set_link(message.from_user.id)}",
    )


# --- /remove ---
@dispatcher.message(Command("remove"))
async def command_remove_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(States.remove)
    await message.answer(
        "🧐 Отправьте стикер из своего набора, который хотите удалить.",
    )


# --- /remove_set ---
@dispatcher.message(Command("remove_set"))
async def command_remove_set_handler(
    message: Message,
    state: FSMContext,
) -> None:
    await state.set_state(States.remove_all)
    await message.answer(
        "🧐 Вы точно хотите удалить набор?\n" 'Для подтверждения отправьте "+"',
    )


# --- receive /remove_set confirmation ---
@dispatcher.message(States.remove_all)
async def receive_remove_set_confirmation_handler(
    message: Message,
    state: FSMContext,
) -> None:
    await state.set_state()

    if message.text != "+":
        await message.answer("☺️ Вы не подтвердили удаление.")
        return

    await bot.delete_sticker_set(
        await get_sticker_set_name(message.from_user.id),
    )
    await message.answer(
        "☹️ Набор успешно удален.\n"
        "В ближайшее время информация о наборе обновится.\n"
        "Для создания нового набора просто отправьте (или перешлите) любой "
        "статичный стикер!",
    )


# --- receive sticker ---
@dispatcher.message(F.sticker)
async def receive_sticker_handler(message: Message, state: FSMContext) -> None:
    if message.sticker.is_animated or message.sticker.is_video:
        await message.answer("☹️Анимированные стикеры пока не поддерживаются.")

    sticker_set_name = await get_sticker_set_name(message.from_user.id)
    sticker_set = await get_sticker_set(sticker_set_name)

    if await state.get_state() is None:
        if sticker_set is not None:
            if message.sticker in sticker_set.stickers:
                await message.answer(
                    "😑 Данный стикер уже есть в Вашем наборе.",
                )
                return

            await bot.add_sticker_to_set(
                message.from_user.id,
                sticker_set_name,
                await get_sticker_to_add(message.sticker),
            )
            await message.answer(
                "👌 Стикер добавлен в набор!\n"
                "В ближайшее время набор обновится.\n"
                f"{await get_sticker_set_link(message.from_user.id)}",
            )
            return

        await bot.create_new_sticker_set(
            message.from_user.id,
            sticker_set_name,
            await get_sticker_set_title(),
            [await get_sticker_to_add(message.sticker)],
            "static",
        )
        await message.answer(
            "🙌 Ваш набор стикеров создан!\n"
            "В ближайшее время информация о наборе обновится.\n"
            f"{await get_sticker_set_link(message.from_user.id)}",
        )
        return

    # remove state
    if sticker_set is None:
        await message.answer(
            "🤨 У вас еще нет набора.\n"
            "Для начала работы просто отправьте (или перешлите) любой "
            "статичный стикер!",
        )
        return

    if message.sticker not in sticker_set.stickers:
        await message.answer("🤔 Данного стикера нет в Вашем наборе.")
        return

    await bot.delete_sticker_from_set(message.sticker.file_id)
    await message.answer(
        "🤝 Стикер удален из Вашего набор.\n"
        "В ближайшее время набор обновится.\n"
        f"{await get_sticker_set_link(message.from_user.id)}",
    )
    await state.set_state()


# ------------------------------------------------------------------------------


async def get_sticker_set_name(user_id: int) -> str:
    return f"u{user_id}_by_{config.bot_name}"


async def get_sticker_set_link(user_id: int) -> str:
    return f"t.me/addstickers/{await get_sticker_set_name(user_id)}"


async def get_sticker_set_title() -> str:
    return config.sticker_set_title


async def get_sticker_set(sticker_set_name: str) -> Optional[StickerSet]:
    try:
        return await bot.get_sticker_set(sticker_set_name)
    except TelegramBadRequest:
        logging.debug("Sticker set does not exist!")
        return None


async def get_sticker_to_add(sticker: Sticker) -> InputSticker:
    return InputSticker(
        sticker=sticker.file_id,
        emoji_list=[sticker.emoji],
    )


async def main() -> None:
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        **{
            **get_logging_config(),
            "level": logging.INFO,
        },
    )
    logging.info(get_banner("stickerpacker"))
    asyncio.run(main())
