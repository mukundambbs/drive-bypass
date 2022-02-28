import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from telegram.ext import CommandHandler
from bot.helper.drive_utils.gdriveTools import GoogleDriveHelper
from bot import LOGGER, dispatcher
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage ,deleteMessage
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands


def list_drive(update, context):
    try:
        search = update.message.text.split(' ',maxsplit=1)[1]
        LOGGER.info(f"Searching: {search}")
        emoji = sendMessage('🧐', context.bot, update)
        reply = sendMessage('𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠..... 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭!', context.bot, update)
        gdrive = GoogleDriveHelper(None)
        msg, button = gdrive.drive_list(search)

        if button:
            editMessage(msg, reply, button)
            deleteMessage(context.bot, emoji)
        else:
            editMessage(f'𝐍𝐨 𝐫𝐞𝐬𝐮𝐥𝐭 𝐟𝐨𝐮𝐧𝐝 𝐟𝐨𝐫 <code>{search}</code>', reply, button)
            deleteMessage(context.bot, emoji)

    except IndexError:
        emo = sendMessage('😡', context.bot, update)
        sendMessage("𝐃𝐨𝐧'𝐭 𝐮𝐬𝐞 𝐮𝐧𝐧𝐞𝐜𝐞𝐬𝐬𝐚𝐫𝐢𝐥𝐲, 𝐒𝐞𝐧𝐝 𝐚 𝐬𝐞𝐚𝐫𝐜𝐡 𝐤𝐞𝐲 𝐚𝐥𝐨𝐧𝐠 𝐰𝐢𝐭𝐡 𝐜𝐨𝐦𝐦𝐚𝐧𝐝", context.bot, update)
        deleteMessage(context.bot, emo)
                
@Client.on_message(filters.command(["droplink"]) & filters.regex(r'https?://[^\s]+'))
async def reply_shortens(bot, update):
    message = await update.reply_text(
        text="`Analysing your link...`",
        disable_web_page_preview=True,
        quote=True
    )
    url = update.matches[0].group(0)
    shorten_urls = await gplinks_bypass(url)
    await message.edit_text(
        text=shorten_urls,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )
    
def droplink_bypass(url):
    client = requests.Session()
    res = client.get(url)

    ref = re.findall("action[ ]{0,}=[ ]{0,}['|\"](.*?)['|\"]", res.text)[0]

    h = {'referer': ref}
    res = client.get(url, headers=h)

    bs4 = BeautifulSoup(res.content, 'lxml')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }

    h = {
        'content-type': 'application/x-www-form-urlencoded',
        'x-requested-with': 'XMLHttpRequest'
    }
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'

    time.sleep(3.1)
    res = client.post(final_url, data=data, headers=h).json()

    return res


list_handler = CommandHandler(BotCommands.ListCommand, list_drive,filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(list_handler)
