import telebot
from telebot import types
from data import new_df, df, countries
from config import TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    listcountries = []
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i in countries:
        country = types.InlineKeyboardButton(f'{i}', callback_data=i)
        listcountries.append(country)
    
    markup.add(*listcountries)
    bot.send_message(message.chat.id, 'Выберите страну в которой хотите получить визу:', reply_markup=markup)

addcountry, addtype, addtrip, addcat, addcons = None, None, None, None, None

@bot.callback_query_handler(func = lambda call: True)
def answer(call):
    
    for j in countries:
        if call.data == j:
            counttype = []
            consulate = []
            markup = types.InlineKeyboardMarkup()
            mark = types.InlineKeyboardMarkup()
            dfs = df[lambda x: x['Страна'] == j]
            global addcountry, addtype, addtrip, addcat, addcons
            addcountry, addtype, addtrip, addcat, addcons = dfs, dfs, dfs, dfs, dfs
            s = (set(dfs['Консульство']))
            if list(s)[0] == '-':
                for typedfs in dfs['Тип визы']:
                    if typedfs not in counttype:
                        counttype.append(typedfs)
                        markup.add(types.InlineKeyboardButton(text=typedfs, callback_data=typedfs))

                # bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text=f'Вы выбрали {j}', reply_markup=markup)
                bot.send_message(call.message.chat.id, 'Выберите тип', reply_markup=markup)  
            else:
                for consul in dfs['Консульство']:
                    if consul not in consulate:
                        consulate.append(consul)
                        mark.add(types.InlineKeyboardButton(text=consul, callback_data=consul[::10]))

                bot.send_message(call.message.chat.id, 'Выберите консульство', reply_markup=mark)

    for cons in set(addcons['Консульство']):
        if call.data == cons[::10]:
            typs = []
            markup = types.InlineKeyboardMarkup()
            addcountry = addcons[lambda x: x['Консульство'] == cons]
            for type in addtype['Тип визы']:
                if type not in typs:
                    typs.append(type)
                    markup.add(types.InlineKeyboardButton(text=type, callback_data=type))
            
            bot.send_message(call.message.chat.id, 'Выберите тип', reply_markup=markup)

    for i in set(addcountry['Тип визы']):        
        if call.data == i:
            trips = []
            markup = types.InlineKeyboardMarkup()
            addtype = addcountry[lambda x: x['Тип визы'] == i]
            for trip in addtype['Цель поездки']:
                if trip not in trips:
                    trips.append(trip)
                    markup.add(types.InlineKeyboardButton(text=trip, callback_data=trip[::10]))
            
            bot.send_message(call.message.chat.id, 'Цель поездки', reply_markup=markup)

    for g in set(addtype['Цель поездки']):
        if call.data == g[::10]:
            cat = []
            markup = types.InlineKeyboardMarkup()
            addtrip = addtype[lambda x: x['Цель поездки'] == g]
            for ca in addtrip['Категории путешественников']:
                if ca not in cat:
                    cat.append(ca)
                    markup.add(types.InlineKeyboardButton(text=ca, callback_data=ca[::10]))
    
            bot.send_message(call.message.chat.id, f'Вы выбрали {g}', reply_markup=markup)

    for f in set(addtrip['Категории путешественников']):
        if call.data == f[::10]:
            document = []
            markup = types.InlineKeyboardMarkup()
            addcat = addtrip[lambda x: x['Категории путешественников'] == f]
            for doc in addcat['Документы']:
                if doc not in document:
                    document.append(doc)
                    markup.add(types.InlineKeyboardButton(text=doc, callback_data=doc[::10]))
    
            bot.send_message(call.message.chat.id, f'Вы выбрали {f}', reply_markup=markup)

    for doc in set(addcat['Документы']):
        if call.data == doc[::10]:
            dfsss1 = addcat[lambda x: x['Документы'] == doc]
            for docreq in dfsss1['Требования к документам']:
                bot.send_message(call.message.chat.id, f'Требования: \n{docreq}')
            

bot.polling(non_stop=True)