import telebot
import os
import json
import pytesseract

try:
    from PIL import Image
except ImportError:
    import Image


def get_settings():
    connect = json.load(open('settings.json'))
    return connect["pytesseract"], connect["telegram_token"], connect["image_repository"]


pytesseract_path, telebot_token, image_repository = get_settings()
pytesseract.pytesseract.tesseract_cmd = pytesseract_path
bot = telebot.TeleBot(telebot_token)


@bot.message_handler(content_types=['photo'])
def photo(message):
    raw = message.photo[2].file_id
    name = "{}.jpg".format(raw)
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(os.path.join(image_repository, name), 'wb') as new_file:
        new_file.write(downloaded_file)

    pytesseract.image_to_string(Image.open(os.path.join(image_repository, name)))

    # TODO поиск по базе и возвращение ответа


@bot.message_handler(content_types=['text'])
def send_text(message):
    message_text = message.text.lower()
    from galery import find_picture

    result = find_picture(message_text)
    if result.count() == 1:
        result = result.first()
        bot.send_message(message.chat.id, result.description or "Описание отсутствует")
    elif 0 < result.count() < 3:
        keyboard = telebot.types.ReplyKeyboardMarkup()
        for res in result:
            keyboard.row(res.name)
        bot.send_message(message.chat.id, "Найдено более одного результата:", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, u"По введенному названию найдено {} картин.".format(result.count()))


bot.polling()