from telegram import InlineKeyboardButton
from messages import *

start_key = [InlineKeyboardButton("Давай начнем!", callback_data="Давай начнем!")]
reply_keyboard_first_menu = [["Создать пост", "Пока"]]
reply_keyboard_post_menu = [["Фото", "Текст", "Кнопки"], ["Удалить кнопки", "Удалить текст", "Удалить фото"], ["Предпросмотр поста", "Далее"]]
