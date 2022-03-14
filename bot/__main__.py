from telegram.ext import CommandHandler
from bot import dispatcher, updater, botStartTime
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import *
from .helper.telegram_helper.filters import CustomFilters
from .modules import authorize, list


def start(update, context):
    
    await bot.get_chat_member(chat_id=-1001472280508, user_id=update.from_user.id)
    await bot.send_message(
            chat_id=update.from_user.id,
            text="**your not a primium user if you want primium service contact my father**")
    
    
    start_string = '\x1f𝐇𝐞𝐲 𝐁𝐫𝐨!! 𝐈 𝐜𝐚𝐧 𝐬𝐞𝐚𝐫𝐜𝐡 𝐟𝐢𝐥𝐞 𝐟𝐫𝐨𝐦 𝐏𝐌 𝐆𝐨𝐨𝐠𝐥𝐞 𝐃𝐫𝐢𝐯𝐞!\x1f'
    sendMessage(start_string, context.bot, update)


def log(update, context):
    sendLogFile(context.bot, update)


botcmds = [(f'{BotCommands.ListCommand}','Search files in My Drive')]


def main():
    bot.set_my_commands(botcmds)

    start_handler = CommandHandler(BotCommands.StartCommand, start, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter, run_async=True)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(log_handler)

    updater.start_polling()
    LOGGER.info("𝐁𝐨𝐭 𝐒𝐭𝐚𝐫𝐭𝐞𝐝!")
    updater.idle()

main()
