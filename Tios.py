import telebot
from telebot import types

bot = telebot.TeleBot('')

user_data = {}

# Словарь с направлениями для каждого уровня
DIRECTIONS = {
    'Магистратура': [
        'Информационные системы и технологии',
        'Конструирование изделий легкой промышленности',
        'Сервис энергетического оборудования и энергоаудит',
        'Сервис транспортных средств',
        'Экономика фирмы (Менеджмент стратегическое управление)'
    ],
    'Бакалавриат': [
        'Информационные системы и технологии',
        'Радиотехника',
        'Инфокоммуникационные технологии и системы связи',
        'Технологические машины и оборудование',
        'Техносферная безопасность',
        'Технология изделий легкой промышленности',
        'Экономика',
        'Менеджмент',
        'Сервис',
        'Туризм'
    ],
    'СПО': [
        'Информационные системы и технологии',
        'Радиотехника',
        'Технологические машины и оборудование',
        'Техносферная безопасность',
        'Сервис'
    ]
}


def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('📄Информация для поступающих')
    item2 = types.KeyboardButton('📞Контактная информация')
    markup.add(item1, item2)
    return markup


def create_back_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton('⬅На главную')
    markup.add(back)
    return markup


def create_education_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('📕Магистратура')
    item2 = types.KeyboardButton('📙Бакалавриат')
    item3 = types.KeyboardButton('📗СПО')
    item4 = types.KeyboardButton('О Вузе')
    back = types.KeyboardButton('⬅На главную')
    markup.add(item1, item2, item3, item4, back)
    return markup


def create_directions_menu(education_level):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    directions = DIRECTIONS.get(education_level, [])
    buttons = [types.KeyboardButton(d) for d in directions]
    markup.add(*buttons)
    back = types.KeyboardButton('⬅Назад')
    markup.add(back)
    return markup


def create_finance_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('💰Бюджет')
    item2 = types.KeyboardButton('💵Коммерция')
    back = types.KeyboardButton('⬅Назад')
    markup.add(item1, item2, back)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f'Привет, {message.from_user.first_name}',
        reply_markup=create_main_menu()
    )


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type != 'private':
        return

    chat_id = message.chat.id

    if message.text == '📞Контактная информация':
        contact_info = """
<i>Контакты</i>
<b>Адрес:</b>
355000, г. Ставрополь, проспект Кулакова, д. 41/1, каб. 110,
тел. 8 (8652) 39-69-97
<b>График работы:</b>
Пн. - Пт.: 8.00 -17.00, перерыв 12.00-13.00
Сб.: 9.00 - 14.00, без перерыва
Вс.: выходной
<b>Электронные ресурсы:</b>
Email: <i>otcom@stis.su</i>
Сайт: https://stis.su
        """
        bot.send_message(chat_id, contact_info,
                         parse_mode='HTML', reply_markup=create_back_button())

    elif message.text == '📄Информация для поступающих':
        bot.send_message(chat_id, 'Выберите уровень образования:',
                         reply_markup=create_education_menu())

    elif message.text in ['📕Магистратура', '📙Бакалавриат', '📗СПО']:
        education_level = message.text[1:]  # Убираем эмодзи
        user_data[chat_id] = {'education_level': education_level}
        bot.send_message(
            chat_id,
            f'Вы выбрали {education_level}. Выберите направление:',
            reply_markup=create_directions_menu(education_level)
        )

    elif message.text in sum(DIRECTIONS.values(), []):
        if chat_id in user_data:
            user_data[chat_id]['direction'] = message.text
            bot.send_message(
                chat_id,
                f'Направление: {message.text}\nВыберите форму обучения:',
                reply_markup=create_finance_menu()
            )

    elif message.text in ['💰Бюджет', '💵Коммерция']:
        if chat_id in user_data:
            data = user_data[chat_id]
            response = (
                f"Вы выбрали:\n"
                f"Уровень образования: {data['education_level']}\n"
                f"Направление: {data['direction']}\n"
                f"Форма обучения: {message.text}\n\n"
            )

            if message.text == '💰Бюджет':
                response += "Информация о бюджетных местах:\n[Данные по бюджету]"
            else:
                response += "Информация о коммерческом обучении:\n[Данные по коммерции]"

            bot.send_message(chat_id, response)

    elif message.text == '⬅Назад':
        if chat_id in user_data:
            del user_data[chat_id]
        bot.send_message(chat_id, 'Выберите уровень образования:',
                         reply_markup=create_education_menu())

    elif message.text == '⬅На главную':
        if chat_id in user_data:
            del user_data[chat_id]
        bot.send_message(chat_id, 'Главное меню',
                         reply_markup=create_main_menu())

    elif message.text == 'О Вузе':
        bot.send_message(
            chat_id,
            "Информация о вузе:\n[Здесь должна быть информация о вузе]",
            reply_markup=create_education_menu()
        )

    else:
        bot.send_message(
            chat_id,
            "Неизвестная команда. Попробуйте еще раз.",
            reply_markup=create_main_menu()
        )


if __name__ == '__main__':
    bot.polling(none_stop=True)
