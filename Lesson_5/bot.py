import telebot
import config
import dbworker

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["start"])
def cmd_start(message):
    state = dbworker.get_current_state(message.chat.id)
    if state == config.States.S_ENTER_NAME.value:
        bot.send_message(message.chat.id, "Send your name")
    elif state == config.States.S_ENTER_AGE.value:
        bot.send_message(message.chat.id, "Send your age")
    elif state == config.States.S_SEND_PIC.value:
        bot.send_message(message.chat.id, "Send your picture")
    else:
        bot.send_message(message.chat.id, "Hello send your name")
        dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME.value)


@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Reset pressed")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.chat.id)
    == config.States.S_ENTER_NAME.value
)
def user_entering_name(message):
    bot.send_message(message.chat.id, "Good name. Enter your age")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_AGE.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.chat.id)
    == config.States.S_ENTER_AGE.value
)
def user_entering_age(message):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Try again")
        return
    if int(message.text) < 5 or int(message.text) > 100:
        bot.send_message(message.chat.id, "No again")
        return
    else:
        bot.send_message(message.chat.id, "Ok. Send picture.")
        dbworker.set_state(message.chat.id, config.States.S_SEND_PIC.value)


@bot.message_handler(
    content_types=["photo"],
    func=lambda message: dbworker.get_current_state(message.chat.id)
    == config.States.S_SEND_PIC.value,
)
def user_sending_photo(message):
    bot.send_message(message.chat.id, "Ok. This is the end.")
    dbworker.set_state(message.chat.id, config.States.S_START.value)


if __name__ == "__main__":
    bot.remove_webhook()
    bot.polling(none_stop=True)
