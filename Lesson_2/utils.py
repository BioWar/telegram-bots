import shelve
from telebot import types
from random import shuffle
from SQLighter import SQLighter
from config import database_name, shelve_name


def count_rows():
    """Count amount of rows in database and save in storage.
    Then chose music among them"""
    db = SQLighter(database_name)
    rowsnum = db.count_rows()
    with shelve.open(shelve_name) as storage:
        storage["rows_count"] = rowsnum


def get_rows_count():
    """Get amount of rows in database from storage"""
    with shelve.open(shelve_name) as storage:
        rowsnum = storage["rows_count"]
    return rowsnum


def set_user_game(chat_id, estimated_answer):
    """Set user as player and save his answer"""
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = estimated_answer


def finish_user_game(chat_id):
    """End game of current user and delete answer from storage"""
    with shelve.open(shelve_name) as storage:
        del storage[str(chat_id)]


def get_aswer_for_user(chat_id):
    """Get correct answer for user. If game was not started, return None"""
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        except KeyError:
            return None


def generate_markup(right_answer, wrong_answers):
    """Create keyboard for answer choice"""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    all_answers = f"{right_answer},{wrong_answers}"
    list_items = []
    for item in all_answers.split(","):
        list_items.append(item)
    shuffle(list_items)
    for item in list_items:
        markup.add(item)
    return markup
