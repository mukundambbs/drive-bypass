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




