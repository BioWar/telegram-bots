import telebot
import config
import os
import time
import random
import utils
from SQLighter import SQLighter
from telebot import types

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["game"])
def game(message):
    db_worker = SQLighter(config.database_name)
    row = db_worker.select_single(random.randint(1, utils.get_rows_count()))
    markup = utils.generate_markup(row[2], row[3])
    bot.send_audio(message.chat.id, row[1], reply_markup=markup)
    utils.set_user_game(message.chat.id, row[2])
    db_worker.close()


@bot.message_handler(func=lambda message: True, content_types=["text", "audio"])
def check_answer(message):
    answer = utils.get_aswer_for_user(message.chat.id)

    if not answer:
        """
        try:
            file_info = bot.get_file(message.audio.file_id)
            print(file_info)
        except:
            pass
            """
        bot.send_message(message.chat.id, "To start the game, choose /game")
    else:
        keyboard_hider = types.ReplyKeyboardRemove()
        if message.text == answer:
            bot.send_message(message.chat.id, "Correct", reply_markup=keyboard_hider)
        else:
            bot.send_message(
                message.chat.id, "Not correct", reply_markup=keyboard_hider
            )
        utils.finish_user_game(message.chat.id)


@bot.message_handler(commands=["test"])
def find_file_ids(message):
    for file in os.listdir(
        config.music_path
    ):
        print(file)
        if file.split(".")[-1] == "ogg":
            f = open(
                config.music_path
                + file,
                "rb",
            )
            res = bot.send_voice(message.chat.id, f, None)
            print(res)
        time.sleep(3)


if __name__ == "__main__":
    utils.count_rows()
    random.seed()
    bot.polling(none_stop=True)
