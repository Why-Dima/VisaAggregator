import telebot
from telebot import types
from data import df, countries
from config import TOKEN
from db import BotDB


BotDB = BotDB('db/database')


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)
    listcountries = []
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i in countries:
        country = types.InlineKeyboardButton(f'{i}', callback_data=i)
        listcountries.append(country)
    
    markup.add(*listcountries)

    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, 'Выберите страну в которой хотите получить визу:', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def text(message):
    mess = '''Бот работает по средству нажатия кнопок, 
чтобы начать работу - нажмите "/start"
или выберите в меню соответствующую кнопку'''
    bot.send_message(message.chat.id, text=mess)

@bot.callback_query_handler(func = lambda call: True)
def answer(call):
    if call.message.text == 'Выберите страну в которой хотите получить визу:':
        for j in countries:
            if call.data == j:
                BotDB.add_country(call.from_user.id, j)
                counttype = []
                consulate = []
                mark = types.InlineKeyboardMarkup()
                markup = types.InlineKeyboardMarkup()
                dfs = df[lambda x: x['Страна'] == j]
                consul = (set(dfs['Консульство']))
                if len(str(consul)) > 5:
                    for cons in dfs['Консульство']:
                        if cons not in consulate:
                            consulate.append(cons)
                            mark.add(types.InlineKeyboardButton(text=cons, callback_data=cons[::10]))

                    bot.send_chat_action(call.message.chat.id, 'typing')   
                    bot.send_message(call.message.chat.id, 'Выберите консульство', reply_markup=mark)

                else:
                    BotDB.add_consulate(call.from_user.id, '')
                    for typedfs in dfs['Тип визы']:
                        if typedfs not in counttype:
                            counttype.append(typedfs)
                            markup.add(types.InlineKeyboardButton(text=typedfs, callback_data=typedfs))

                    if len(str(typedfs)) < 4:
                        bot.send_chat_action(call.message.chat.id, 'typing')
                        bot.send_message(call.message.chat.id, f'Виза в {j} не доступна')
                    else:
                        bot.send_chat_action(call.message.chat.id, 'typing')
                        bot.send_message(call.message.chat.id, f'Выберите тип {j}', reply_markup=markup)  

    if call.message.text == 'Выберите консульство':
        try:
            dfs = df[lambda x: x['Страна'] == BotDB.get_country(call.from_user.id)]
            for cons in set(dfs['Консульство']):
                if call.data == cons[::10]:
                    BotDB.add_consulate(call.from_user.id, cons)
                    type = []
                    markup = types.InlineKeyboardMarkup()
                    addcons = dfs[lambda x: x['Консульство'] == cons]
                    for typ in addcons['Тип визы']:
                        if typ not in type:
                            type.append(typ)
                            markup.add(types.InlineKeyboardButton(text=typ, callback_data=typ))

                    bot.send_chat_action(call.message.chat.id, 'typing')
                    bot.send_message(call.message.chat.id, 'Выберите тип', reply_markup=markup)
        except TypeError:
            bot.send_message(call.message.chat.id, 'У выбранной Вами ранее страны нет консульств для выбора')
                
    if call.message.text[:12] == 'Выберите тип':
        dfs = df[lambda x: x['Страна'] == BotDB.get_country(call.from_user.id)]
        if BotDB.get_bool_consulate(call.from_user.id):
            dfs = dfs[lambda x: x['Консульство'] == BotDB.get_consulate(call.from_user.id)]
        for i in set(dfs['Тип визы']):  
            if call.data == i:
                BotDB.add_type(call.from_user.id, i)
                trips = []  
                markup = types.InlineKeyboardMarkup()
                addtype = dfs[lambda x: x['Тип визы'] == i]
                for trip in addtype['Цель поездки']:
                    if trip not in trips:
                        trips.append(trip)
                        markup.add(types.InlineKeyboardButton(text=trip, callback_data=trip[::10]))
                
                bot.send_chat_action(call.message.chat.id, 'typing')
                bot.send_message(call.message.chat.id, 'Цель поездки', reply_markup=markup)

    if call.message.text == 'Цель поездки':
        dfscountry = df[lambda x: x['Страна'] == BotDB.get_country(call.from_user.id)]
        if BotDB.get_bool_consulate(call.from_user.id):
            dfscountry = dfscountry[lambda x: x['Консульство'] == BotDB.get_consulate(call.from_user.id)]
        dfstype = dfscountry[lambda x: x['Тип визы'] == BotDB.get_type(call.from_user.id)]
        for g in set(dfstype['Цель поездки']):
            if call.data == g[::10]:
                BotDB.add_trip(call.from_user.id, g)
                cat = []
                markup = types.InlineKeyboardMarkup()
                addtrip = dfstype[lambda x: x['Цель поездки'] == g]
                for ca in addtrip['Категории путешественников']:
                    if ca not in cat:
                        cat.append(ca)
                        markup.add(types.InlineKeyboardButton(text=ca, callback_data=ca[::10]))

                bot.send_chat_action(call.message.chat.id, 'typing')
                bot.send_message(call.message.chat.id, f'Категории путешественников', reply_markup=markup)
    
    if call.message.text == 'Категории путешественников':
        dfscount = df[lambda x: x['Страна'] == BotDB.get_country(call.from_user.id)]
        if BotDB.get_bool_consulate(call.from_user.id):
            dfscount = dfscount[lambda x: x['Консульство'] == BotDB.get_consulate(call.from_user.id)]
        dfsty = dfscount[lambda x: x['Тип визы'] == BotDB.get_type(call.from_user.id)]
        dfstrip = dfsty[lambda x: x['Цель поездки'] == BotDB.get_trip(call.from_user.id)]
        for f in set(dfstrip['Категории путешественников']):
            if call.data == f[::10]:
                BotDB.add_category(call.from_user.id, f)
                document = []
                markup = types.InlineKeyboardMarkup()
                addcat = dfstrip[lambda x: x['Категории путешественников'] == f]
                for doc in addcat['Документы']:
                    if doc not in document:
                        document.append(doc)
                        markup.add(types.InlineKeyboardButton(text=doc, callback_data=doc[::10]))

                bot.send_chat_action(call.message.chat.id, 'typing')
                bot.send_message(call.message.chat.id, f'Вы выбрали {f}', reply_markup=markup)
    
    if call.message.text[:10] == 'Вы выбрали':
        dfsc = df[lambda x: x['Страна'] == BotDB.get_country(call.from_user.id)]
        if BotDB.get_bool_consulate(call.from_user.id):
            dfsc = dfsc[lambda x: x['Консульство'] == BotDB.get_consulate(call.from_user.id)]
        dfst = dfsc[lambda x: x['Тип визы'] == BotDB.get_type(call.from_user.id)]
        dfstr = dfst[lambda x: x['Цель поездки'] == BotDB.get_trip(call.from_user.id)]
        dfsdoc = dfstr[lambda x: x['Категории путешественников'] == BotDB.get_category(call.from_user.id)]
        for doc in set(dfsdoc['Документы']):
            if call.data == doc[::10]:
                dfsdocument = dfsdoc[lambda x: x['Документы'] == doc]
                for docreq in dfsdocument['Требования к документам']:
                    bot.send_chat_action(call.message.chat.id, 'typing')
                    bot.send_message(call.message.chat.id, text=f'Требования: \n{docreq}', parse_mode='HTML')


bot.polling(non_stop=True)

