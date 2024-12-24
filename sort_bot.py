import telebot
from telebot import types

API_TOKEN = 'sosi'
bot = telebot.TeleBot(API_TOKEN)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Отсортировать Числа")
btn2 = types.KeyboardButton("Отсортировать Слова")
btn3 = types.KeyboardButton("Назад")
markup.add(btn1, btn2, btn3)

@bot.message_handler(commands=["start", "back"])
def start(message):
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я бот сортировщик, который поможет тебе отсортировать txt файл".format(message.from_user), reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Отсортировать Числа")
def numbers_sort_menu(message):
    bot.send_message(message.chat.id, 'Отправь файл с названием numbers.txt, и я его отсортирую.')

@bot.message_handler(content_types=['document'])
def handle_document(message):
    if message.document.mime_type == 'text/plain' and message.document.file_name == 'numbers.txt':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        numbers = downloaded_file.decode('utf-8').splitlines()
        try:
            numbers = sorted(map(int, numbers))
            sorted_numbers = '\n'.join(map(str, numbers))
            with open('sorted_numbers.txt', 'w') as f:
                f.write(sorted_numbers)
            with open('sorted_numbers.txt', 'rb') as f:
                bot.send_document(message.chat.id, f)
        except ValueError:
            bot.send_message(message.chat.id, 'Ошибка: убедитесь, что файл содержит только числа, по одному на строку.')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, отправьте файл с названием numbers.txt.')

@bot.message_handler(func=lambda message: message.text == "Назад")
def back(message):
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я бот сортировщик, который поможет тебе отсортировать txt файл".format(message.from_user), reply_markup=markup)
    btn1 = types.KeyboardButton("Отсортировать Числа")
    btn2 = types.KeyboardButton("Отсортировать Слова")
    btn3 = types.KeyboardButton("Назад")
    markup.add(btn1, btn2, btn3)

if __name__ == "__main__":
    bot.polling(none_stop=True)