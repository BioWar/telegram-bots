# Telegram Bot Tutorial (Total Recall)

This repository contains basic examples of telegram bots written partially by myself, and with guidance of telebot examples from their repository:

[Telebot](https://github.com/eternnoir/pyTelegramBotAPI/tree/master/examples)
[Other](https://github.com/MasterGroosha/telegram-tutorial)

## Description

1. [Lesson 1](https://github.com/BioWar/telegram-bots/tree/master/Lesson_1)

	Lesson 1 contains simple "echo bot", nothing special.

2. [Lesson 2](https://github.com/BioWar/telegram-bots/tree/master/Lesson_2)

	Lesson 2 already have simple "game", where you should correctly guess song, and press corresponding button in conversation menu. Simple SQLite database used as the storage for bot songs. utils.py have basic getters for that database.

3. [Lesson 3](https://github.com/BioWar/telegram-bots/tree/master/Lesson_3)

	Lesson 3 is a simple webhook example straight from the [Telebot](https://github.com/eternnoir/pyTelegramBotAPI/tree/master/examples). I have some pain during save copy of files on my server, but this is not the topic.

4. [Lesson 4](https://github.com/BioWar/telegram-bots/tree/master/Lesson_4)

	Lesson 4 is completely my "masterpiece". Some work will be done to make bot working correct but it already has some good results. Firstly we parse the  [Medium](https://medium.com/topic/technology) and get list of articles, if there are articles out of scope of our database we save them. Then bot will post new articles in telegram channel. This bot was made as "coding warm-up" not for panacea for posting bot.
