import pandas as pd
import telebot
import random
from telebot import types

df = pd.read_csv('anime.csv', converters={'anime_genre': eval})
listgenre = []
for i in range(len(df)):
    listgenre += df['anime_genre'][i]
listgenre = set(listgenre)
listgenre = [cousine for cousine in listgenre if not cousine.isdigit()]
listgenre.sort()


bot = telebot.TeleBot('token for bot')


@bot.message_handler(commands=['start'])
def hello(message):
    key = types.ReplyKeyboardMarkup(resize_keyboard=True)
    genre = types.KeyboardButton("/Genre")
    name = types.KeyboardButton("/Name")
    game = types.KeyboardButton("/Game")
    key.add(genre, name, game)
    text1 = f"Добро пожаловать, {message.from_user.first_name}!\nЯ - <b>{bot.get_me().first_name}</b> для погружения в мир аниме."
    text1 += str('\n' + '\n')
    text1 += 'Нажмите /Genre для подбора аниме по жанру.'
    text1 += str('\n' + '\n')
    text1 += 'Нажмите /Name для поиска аниме по названию.'
    text1 += str('\n' + '\n')
    text1 += 'Нажмите /Game для игры в викторину.'
    text1 += str('\n' + '\n' + '\n')
    text1 += 'Разработчик: @Malkovw'
    bot.send_message(message.chat.id, text1, parse_mode='html', reply_markup=key)


@bot.message_handler(commands=['Game'], content_types=['text'])
def game1(message):
    global a
    a = 1
    buttonlogic = types.InlineKeyboardMarkup()
    game = df.sample(4)
    global right
    right = game['anime_name'].iloc[0]
    global answer
    answer = [a for a in game['anime_name']]
    random.shuffle(answer)
    for gen in answer:
        key_genre = types.InlineKeyboardButton(text=gen, callback_data=gen)
        buttonlogic.add(key_genre)
    bot.send_message(message.from_user.id,
                     text=game['anime_description'].iloc[0] + '\n ' + '\n' + 'Выбери правильный ответ:',
                     reply_markup=buttonlogic)
    bot.send_message(message.from_user.id, text='Для следующего вопроса нажмите /Game')


@bot.message_handler(commands=['Genre'], content_types=['text'])
def hello1(message):
    global a
    a = 0
    buttonlogic = types.InlineKeyboardMarkup()
    for gen in listgenre:
        key_genre = types.InlineKeyboardButton(text=gen, callback_data=gen)
        buttonlogic.add(key_genre)
    bot.send_message(message.from_user.id, text='Выбери жанр:', reply_markup=buttonlogic)


@bot.callback_query_handler(func=lambda let: True)
def gen(let):
    genre1 = let.data
    id1 = let.message.chat.id
    if a == 1:
        gamerule(genre1, id1)
    else:
        recomendation(genre1, id1)


def gamerule(name1, id1):
    if (name1 == right):
        bot.send_message(id1, 'Правильный ответ :)')
    else:
        bot.send_message(id1, 'Ответ неверный : (')


def recomendation(genre1, id1):
    indexes_match_queries = df.apply(lambda row: str(genre1) in row['anime_genre'], axis=1, )
    df3 = df[indexes_match_queries].tail().reset_index(drop=True)
    df3 = df3.sort_values(by=['anime_views', 'anime_comments']).reset_index(drop=True)
    bot.send_message(id1, 'Топ аниме жанра ' + genre1 + ':')
    for i in range(len(df3)):
        answer = str(df3['anime_name'].iloc[i])
        answer += str('\n' + '\n')
        answer += 'Год: '
        answer += str(df3['anime_year'].iloc[i])
        answer += str('\n' + '\n')
        answer += 'Количество эпизодов: '
        answer += str(df3['number_of_episodes'].iloc[i])
        answer += str('\n' + '\n')
        if (df3['ongoing'].iloc[i] == 1):
            answer += 'Выходят новые серии'
        else:
            answer += 'Серии больше не выходят'
        answer += str('\n' + '\n')
        answer += 'Количество просмотров: '
        answer += str(df3['anime_views'].iloc[i])
        answer += str('\n' + '\n')
        answer += str(df3['anime_description'].iloc[i])
        answer += str('\n' + '\n')
        answer += str(df3['anime_url'].iloc[i])
        bot.send_message(id1, answer)


@bot.message_handler(commands=['Name'], content_types=['text'])
def hello2(message):
    bot.send_message(message.from_user.id, text='Введите название:')


@bot.message_handler(content_types=['text'])
def name1(message):
    buttonlogic = types.InlineKeyboardMarkup()
    if len(df[df['anime_name'] == message.text]) == 1:
        indexes_match_queries = df.apply(lambda row: str(message.text) in row['anime_name'], axis=1, )
        df3 = df[indexes_match_queries]
        answer = str(df3['anime_name'].iloc[0])
        answer += str('\n' + '\n')
        answer += 'Год: '
        answer += str(df3['anime_year'].iloc[0])
        answer += str('\n' + '\n')
        answer += 'Количество эпизодов: '
        answer += str(df3['number_of_episodes'].iloc[0])
        answer += str('\n' + '\n')
        if (df3['ongoing'].iloc[0] == 1):
            answer += 'Выходят новые серии'
        else:
            answer += 'Серии больше не выходят'
        answer += str('\n' + '\n')
        answer += 'Количество просмотров: '
        answer += str(df3['anime_views'].iloc[0])
        answer += str('\n' + '\n')
        answer += str(df3['anime_description'].iloc[0])
        answer += str('\n' + '\n')
        answer += str(df3['anime_url'].iloc[0])
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, 'Аниме не найдено')


bot.polling(none_stop=True)
