import os
import aiohttp
import asyncio
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pyrogram import Client, filters

from telegram.ext import CommandHandler
from bot.helper.drive_utils.gdriveTools import GoogleDriveHelper
from bot import LOGGER, dispatcher
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands

options = webdriver.ChromeOptions()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")

driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
driver.maximize_window()
torrent = []

def listmv(c,m):
  querys = ""
  texts = ""
  length = len(m.command)
  for queryss in m.command[1:length]:
    querys += f"{queryss} "
  if querys == "":
    await m.reply(f'`/listmv [query]`', quote=True)
  elif querys != "":
    link = f"https://www.1tamilmv.com/index.php?/search/&q={querys}&search_and_or=and&search_in=titles&sortby=relevancy"
    txt = await m.reply_text(f"Searching for: {querys} 🔍")
    driver.get(link)
    await asyncio.sleep(5)
    title = driver.title
    links = driver.find_elements(By.CLASS_NAME, "ipsStreamItem_title")
    msg = []
    count = 0
    
    for link in links:
      text = link.text
      url0 = link.find_element(By.CLASS_NAME, 'ipsType_break')
      url1 = url0.find_element(By.TAG_NAME, 'a').get_attribute("href")
      print(url1)
      count += 1
      msgs = f"{count}. <a href='{url1}'>{text}</a>\n\n"
      msg.append(msgs)

    for text in msg[0:20]:
      texts += text
    reply = f"<b>{title}</b>\n\n{texts}"
    await c.send_message(m.chat.id, reply, disable_web_page_preview=True, parse_mode="html")
    await txt.delete()




