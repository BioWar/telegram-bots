import time
import eventlet
import requests
import logging
import re
import telebot
from time import sleep
from bs4 import BeautifulSoup
import utils

URL_MEDIUM = "https://medium.com/topic/technology"
BOT_TOKEN = "YOUR_TOKEN_HERE"
CHANNEL_NAME = "@CHANNEL"

SINGLE_RUN = False

bot = telebot.TeleBot(BOT_TOKEN)


def getLinks(url):
    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page)
    links = set()
    for i in soup.find_all("a", attrs={"href": re.compile("^https://")}):
        link = i.get("href")
        if (
            "https://medium.com/m/signin?operation=register" not in link
            and "https://towardsdatascience.com/?source" not in link
            and "https://medium.com/m/signin?" not in link
            and "https://medium.com/membership?s" not in link
        ):
            links.add(link)

    return list(links)


def append_table():
    links = getLinks(URL_MEDIUM)
    content = utils.SQLighter("ArticleMedium.db")
    for link in links:
        content.create_article(link)


def send_new_post(item, connection):
    print(item)
    print(item[1])
    bot.send_message(CHANNEL_NAME, item[1])
    connection.change_status(item[0], utils.USED)
    sleep(1)
    return


if __name__ == "__main__":
    logging.getLogger("requests").setLevel(logging.CRITICAL)
    logging.basicConfig(level=logging.INFO, filename="bot_log.log")

    content = utils.SQLighter("ArticleMedium.db")
    content.set_all_to_unused()

    while True:
        article = content.select_last_unused()
        send_new_post(article, content)
        sleep(10)

        try:
            if content.select_last_unused()[0] % 3 == 0:
                bot.send_message(CHANNEL_NAME, "We will be back in a Minute ;)")
                sleep(60)
        except Exception as error:
            bot.send_message(
                CHANNEL_NAME,
                "Looks like we are out of articles for today. Come here tomorrow pal :)",
            )
            append_table()
            sleep(30)

        used_articles = content.select_all_used()
        all_articles = content.select_all()
