import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from telegram.ext import CommandHandler
from bot.helper.drive_utils.gdriveTools import GoogleDriveHelper
from bot import LOGGER, dispatcher
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands


def list_drive(update, context):
    try:
        search = update.message.text.split(' ',maxsplit=1)[1]
        LOGGER.info(f"Searching: {search}")
        emoji = sendMessage('🧐', context.bot, update)
        reply = sendMessage("𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠..... 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭!\n\n 𝗜𝗳 𝗕𝗼𝗧 𝗱𝗼𝗲𝘀𝗻'𝘁 𝘀𝗲𝗻𝗱 𝗮𝗻𝘆, 𝗧𝗿𝘆 𝗮𝗴𝗮𝗶𝗻 𝘄𝗶𝘁𝗵 𝗠𝗼𝘃𝗶𝗲 𝗡𝗮𝗺𝗲 & 𝗬𝗲𝗮𝗿🙂.", context.bot, update)
        gdrive = GoogleDriveHelper(None)
        msg, button = gdrive.drive_list(search)

        if button:
            msgg = "𝗟𝗶𝗻𝗸 𝗦𝗲𝗻𝗱𝗲𝗱 𝗧𝗼 𝗬𝗼𝘂𝗿 𝗣𝗠 😎"
            editMessage(msgg, reply, button)
            deleteMessage(context.bot, emoji)
            sendPrivate(msg, context.bot, update, button)
        else:
            editMessage(f'𝐍𝐨 𝐫𝐞𝐬𝐮𝐥𝐭 𝐟𝐨𝐮𝐧𝐝 𝐟𝐨𝐫 <code>{search}</code>', reply, button)
            deleteMessage(context.bot, emoji)

    except IndexError:
        emo = sendMessage('😡', context.bot, update)
        sendMessage("𝐃𝐨𝐧'𝐭 𝐮𝐬𝐞 𝐮𝐧𝐧𝐞𝐜𝐞𝐬𝐬𝐚𝐫𝐢𝐥𝐲, 𝐒𝐞𝐧𝐝 𝐚 𝐬𝐞𝐚𝐫𝐜𝐡 𝐤𝐞𝐲 𝐚𝐥𝐨𝐧𝐠 𝐰𝐢𝐭𝐡 𝐜𝐨𝐦𝐦𝐚𝐧𝐝", context.bot, update)
        deleteMessage(context.bot, emo)


list_handler = CommandHandler(BotCommands.ListCommand, list_drive,filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(list_handler)
