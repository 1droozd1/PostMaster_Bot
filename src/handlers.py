from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputMediaPhoto, InputMediaDocument
from telegram.ext import ContextTypes, ConversationHandler
from messages import *
from kb import *
import os, logging, shutil

logger = logging.getLogger(__name__)
   
# Функция для очистки папки
def clear_data_folder(folder_path: str):
   """Удаляет все файлы и папки в указанной папке."""
   if os.path.exists(folder_path):
      # Удаляем содержимое папки
      shutil.rmtree(folder_path)
      # Создаем папку заново
      os.makedirs(folder_path)

# Функция для удаление файла с информацией по кнопкам пользователя
def clear_keyboard(filepath: str):
   if os.path.exists(filepath):
      os.remove(filepath)
      return True
   else:
      return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
   
   logger.info("Запущена команда /start")

   # Очистка папки data
   data_folder = './data'
   clear_data_folder(data_folder)

   await context.bot.send_photo(
      chat_id=update.effective_chat.id,
      photo='https://i.pinimg.com/564x/a8/f1/5e/a8f15eee6a420f42ceae8e2111ab865b.jpg',
      caption=HELLO_MESSAGE,
      reply_markup=InlineKeyboardMarkup(inline_keyboard=[start_key])
      )
   return MAIN_MENU

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

   logger.info("Запущена главное меню...")
   await context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = MAIN_MENU_TEXT,
      reply_markup=ReplyKeyboardMarkup(
         reply_keyboard_first_menu,
         resize_keyboard=True,
         one_time_keyboard=True
      ),
   )
   return CREATING_POST

async def creating_post_func(update: Update, context: ContextTypes.DEFAULT_TYPE):

   logger.info("Выбор пользователем вида информации для поста..")
   await context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = CREATING_POST_TEXT,
      reply_markup=ReplyKeyboardMarkup(
         reply_keyboard_post_menu,
         resize_keyboard=True,
         one_time_keyboard=True
      ),
   )
   return CREATING_CHOICE

async def photo_adding_func(update: Update, context: ContextTypes.DEFAULT_TYPE):

   logger.info("Запуск добавления фото")
   await context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = PHOTO_ADDING_TEXT,
   )
   return PHOTO_ADD

async def save_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

   logger.info("Получение фото от пользователя")

   if not os.path.exists('./data'):
      os.makedirs('./data')

   photo_file = await update.message.photo[-1].get_file()
   photo_path = os.path.join("./data", f"1_{update.message.from_user.id}.jpg")

   await photo_file.download_to_drive(photo_path)

   with open(photo_path, 'rb') as photo:
       await context.bot.send_photo(
           chat_id=update.effective_chat.id,
           caption="Ваше фото сохранено!",
           photo=photo
       )

   await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Что вы хотите добавить дальше?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_post_menu,
            resize_keyboard=True,
            one_time_keyboard=True
        )
   )
   return CREATING_CHOICE

async def text_adding_func(update: Update, context: ContextTypes.DEFAULT_TYPE):

   logger.info("Запуск добавления текста")
   await context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = TEXT_ADDING_TEXT,
   )
   return TEXT_ADD

async def save_text (update: Update, context: ContextTypes.DEFAULT_TYPE):

   logger.info("Сохранение текста")

   text = update.message.text

   # Создаём директорию 'data', если она не существует
   if not os.path.exists('./data'):
      os.makedirs('./data')

   # Сохраняем текст в файл
   text_path = os.path.join("./data", f"text_{update.message.from_user.id}.txt")

   with open(text_path, 'w') as file:
      file.write(text)

   # Подтверждаем сохранение текста пользователю
   await context.bot.send_message(
      chat_id=update.effective_chat.id,
      text="Ваш текст сохранён!",
   )

   await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Что вы хотите добавить дальше?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_post_menu,
            resize_keyboard=True,
            one_time_keyboard=True
        )
   )

   return CREATING_CHOICE

async def preview_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
   logger.info("Предпросмотр поста")

   # Проверяем наличие папки
   if not os.path.exists('./data'):
      await context.bot.send_message(
         chat_id=update.effective_chat.id,
         text="Нет данных для предпросмотра."
      )
      return CREATING_CHOICE
   
   # Получаем все файлы из папки data
   files = os.listdir('./data')

   # Получаем текст из текстового файла, если он есть
   text_content = ""
   button_texts = []
   text_file_path, keys_file_path = None, None

   texts = sorted([file for file in files if file.endswith('.txt') and str(update.message.from_user.id) in file])
   if texts:
      for text in texts:
         if text.startswith('text'):
            text_file_path = os.path.join('./data', text)
         if text.startswith('keys'):
            keys_file_path = os.path.join('./data', text)

      if text_file_path:
         with open(text_file_path, 'r') as text_file:
            text_content = text_file.read()

      if keys_file_path:
         with open(keys_file_path, 'r') as text_file:
            for line in text_file:
               button_texts.append(line.strip())
   
   buttons = []
   if button_texts:
      for btn_text in button_texts:
            new_buttons = []
            if '|' in btn_text:
               for new_button in btn_text.strip().split('|'):
                  try:
                     btn_label, btn_url = new_button.strip('[]').split(' + ')
                     btn_label = btn_label.strip('[] ')
                     btn_url = btn_url.strip('[] ')
                     new_buttons.append(InlineKeyboardButton(btn_label, callback_data=btn_url, url=btn_url))
                  except ValueError:
                     await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text='Неправильный формат кнопок!',
                     )
                     # Возвращаем пользователя к состоянию выбора
                     await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Что вы хотите добавить дальше?",
                        reply_markup=ReplyKeyboardMarkup(
                           reply_keyboard_post_menu,
                           resize_keyboard=True,
                           one_time_keyboard=True
                        )
                     )
                     return CREATING_CHOICE 

               buttons.append(tuple(new_buttons))
            else:
               try:
                  btn_label, btn_url = btn_text.strip('[]').split(' + ')
                  btn_label = btn_label.strip('[] ')
                  btn_url = btn_url.strip('[] ')
                  buttons.append((InlineKeyboardButton(btn_label, callback_data=btn_url, url=btn_url),))
               except ValueError:
                     await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text='Неправильный формат кнопок!',
                     )
                     # Возвращаем пользователя к состоянию выбора
                     await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Что вы хотите добавить дальше?",
                        reply_markup=ReplyKeyboardMarkup(
                           reply_keyboard_post_menu,
                           resize_keyboard=True,
                           one_time_keyboard=True
                        )
                     )
                     return CREATING_CHOICE 

   # Отправляем фото
   photos = sorted([file for file in files if file.endswith('.jpg') and str(update.message.from_user.id) in file])
   buttons = tuple(buttons)
   reply_markup = InlineKeyboardMarkup(buttons) if buttons else None

   if photos:
      photo_path = os.path.join('./data', photos[0])

      with open(photo_path, 'rb') as photo_file:
         if buttons:
            if text_content:
               await context.bot.send_photo(
                  chat_id=update.effective_chat.id,
                  photo=photo_file,
                  caption=text_content,
                  reply_markup=reply_markup
               )
            else:
               await context.bot.send_photo(
                  chat_id=update.effective_chat.id,
                  photo=photo_file,
                  reply_markup=reply_markup
               )
         else:
            if text_content:
               await context.bot.send_photo(
                  chat_id=update.effective_chat.id,
                  photo=photo_file,
                  caption=text_content
               )
            else:
               await context.bot.send_photo(
                  chat_id=update.effective_chat.id,
                  photo=photo_file,
               )
   else:
      if buttons:
         if text_content:
            await context.bot.send_message(
                  chat_id=update.effective_chat.id,
                  text=text_content,
                  reply_markup=reply_markup
               )
         else:
            await context.bot.send_message(
                  chat_id=update.effective_chat.id,
                  text='Нет данных для просмотра',
                  reply_markup=reply_markup
               )
      else:
         if text_content:
            await context.bot.send_message(
                  chat_id=update.effective_chat.id,
                  text=text_content,
               )
         else:
            await context.bot.send_message(
                  chat_id=update.effective_chat.id,
                  text='Нет данных для просмотра'
               )

   # Возвращаем пользователя к состоянию выбора
   await context.bot.send_message(
      chat_id=update.effective_chat.id,
      text="Что вы хотите добавить дальше?",
      reply_markup=ReplyKeyboardMarkup(
         reply_keyboard_post_menu,
         resize_keyboard=True,
         one_time_keyboard=True
      )
   )
   return CREATING_CHOICE


async def delete_keyboard_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
   file_path = f'./data/keys_{update.message.from_user.id}.txt'
   if clear_keyboard(file_path):
      await context.bot.send_message (
         chat_id = update.effective_chat.id,
         text = 'Кнопки успешно удалены!',
      )
   else:
      await context.bot.send_message (
         chat_id = update.effective_chat.id,
         text = 'Вы не добавляли еще кнопок!',
      )
   
   await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Что вы хотите добавить дальше?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_post_menu,
            resize_keyboard=True,
            one_time_keyboard=True
        )
   )
   return CREATING_CHOICE

async def delete_text_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
   file_path = f'./data/text_{update.message.from_user.id}.txt'
   if clear_keyboard(file_path):
      await context.bot.send_message (
         chat_id = update.effective_chat.id,
         text = 'Текст успешно удален!',
      )
   else:
      await context.bot.send_message (
         chat_id = update.effective_chat.id,
         text = 'Вы еще не добавляли текст!',
      )
   
   await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Что вы хотите добавить дальше?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_post_menu,
            resize_keyboard=True,
            one_time_keyboard=True
        )
   )
   return CREATING_CHOICE

async def delete_photo_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
   file_path = f'./data/1_{update.message.from_user.id}.jpg'
   if clear_keyboard(file_path):
      await context.bot.send_message (
         chat_id = update.effective_chat.id,
         text = 'Фото успешно удалено!',
      )
   else:
      await context.bot.send_message (
         chat_id = update.effective_chat.id,
         text = 'Вы еще не добавляли фото!',
      )
   
   await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Что вы хотите добавить дальше?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_post_menu,
            resize_keyboard=True,
            one_time_keyboard=True
        )
   )
   return CREATING_CHOICE

async def keyboard_adding_func(update: Update, context: ContextTypes.DEFAULT_TYPE):

   logger.info("Запуск добавления кнопок")
   await context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = KEYBOARD_ADD_TEXT,
   )
   return KEYBOARD_ADD

async def save_keyboards (update: Update, context: ContextTypes.DEFAULT_TYPE):

   logger.info("Сохранение кнопок")

   text = update.message.text

   # Создаём директорию 'data', если она не существует
   if not os.path.exists('./data'):
      os.makedirs('./data')

   # Сохраняем текст в файл
   text_path = os.path.join("./data", f"keys_{update.message.from_user.id}.txt")

   with open(text_path, 'w') as file:
      file.write(text)

   # Подтверждаем сохранение текста пользователю
   await context.bot.send_message(
      chat_id=update.effective_chat.id,
      text="Ваши кнопки добавлены!",
   )

   await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Что вы хотите добавить дальше?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_post_menu,
            resize_keyboard=True,
            one_time_keyboard=True
        )
   )
   return CREATING_CHOICE

async def continue_func(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

   logger.info("Сохранение поста")

   # Проверяем наличие папки
   if not os.path.exists('./data'):
      await context.bot.send_message(
         chat_id=update.effective_chat.id,
         text="Нет данных для просмотра."
      )
      return CREATING_CHOICE
   
   # Получаем все файлы из папки data
   files = os.listdir('./data')

   # Получаем текст из текстового файла, если он есть
   text_content = ""
   button_texts = []
   text_file_path, keys_file_path = None, None

   texts = sorted([file for file in files if file.endswith('.txt') and str(update.message.from_user.id) in file])
   if texts:
      for text in texts:
         if text.startswith('text'):
            text_file_path = os.path.join('./data', texts[-1])
         if text.startswith('keys'):
            keys_file_path = os.path.join('./data', texts[0])

      if text_file_path:
         with open(text_file_path, 'r') as text_file:
            text_content = text_file.read()

      if keys_file_path:
         with open(keys_file_path, 'r') as text_file:
            for line in text_file:
               button_texts.append(line.strip())
   
   buttons = []
   if button_texts:
      for btn_text in button_texts:
            new_buttons = []
            if '|' in btn_text:
               for new_button in btn_text.strip().split('|'):
                  btn_label, btn_url = new_button.strip('[]').split(' + ')
                  btn_label = btn_label.strip('[] ')
                  btn_url = btn_url.strip('[] ')
                  new_buttons.append(InlineKeyboardButton(btn_label, callback_data=btn_url, url=btn_url))

               buttons.append(tuple(new_buttons))
            else:
               btn_label, btn_url = btn_text.strip('[]').split(' + ')
               btn_label = btn_label.strip('[] ')
               btn_url = btn_url.strip('[] ')
               buttons.append((InlineKeyboardButton(btn_label, callback_data=btn_url, url=btn_url),))

   # Отправляем фото
   photos = sorted([file for file in files if file.endswith('.jpg') and str(update.message.from_user.id) in file])
   buttons = tuple(buttons)
   reply_markup = InlineKeyboardMarkup(buttons) if buttons else None

   await context.bot.send_message(
         chat_id=update.effective_chat.id,
         text="Ваш пост:"
      )

   if photos:
      photo_path = os.path.join('./data', photos[0])

      with open(photo_path, 'rb') as photo_file:
         if buttons:
            if text_content:
               await context.bot.send_photo(
                  chat_id=update.effective_chat.id,
                  photo=photo_file,
                  caption=text_content,
                  reply_markup=reply_markup
               )
            else:
               await context.bot.send_photo(
                  chat_id=update.effective_chat.id,
                  photo=photo_file,
                  reply_markup=reply_markup
               )
         else:
            if text_content:
               await context.bot.send_photo(
                  chat_id=update.effective_chat.id,
                  photo=photo_file,
                  caption=text_content
               )
            else:
               await context.bot.send_photo(
                  chat_id=update.effective_chat.id,
                  photo=photo_file,
               )
   else:
      if buttons:
         if text_content:
            await context.bot.send_message(
                  chat_id=update.effective_chat.id,
                  text=text_content,
                  reply_markup=reply_markup
               )
         else:
            await context.bot.send_message(
                  chat_id=update.effective_chat.id,
                  text='Нет данных для просмотра',
                  reply_markup=reply_markup
               )
      else:
         if text_content:
            await context.bot.send_message(
                  chat_id=update.effective_chat.id,
                  text=text_content,
               )
         else:
            await context.bot.send_message(
                  chat_id=update.effective_chat.id,
                  text='Нет данных для просмотра'
               )
   
   # Очистка папки data
   data_folder = './data'
   clear_data_folder(data_folder)

   logger.info("Запущена главное меню...")
   await context.bot.send_message(
      chat_id = update.effective_chat.id,
      text = MAIN_MENU_TEXT,
      reply_markup=ReplyKeyboardMarkup(
         reply_keyboard_first_menu,
         resize_keyboard=True,
         one_time_keyboard=True
      ),
   )
   return CREATING_POST

# Завершение диалога с ботом
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

   await context.bot.send_message(
         chat_id= update.effective_chat.id,
         text= BYE_TEXT, 
         reply_markup=ReplyKeyboardRemove()
   )

   return ConversationHandler.END