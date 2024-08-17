import os, logging
from telegram.ext import Application, ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import Update
from handlers import start
from handlers import *

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

def get_token():
    if not os.path.exists('src/token.txt'):
        os.system("python token_input.py")

    with open('src/token.txt', 'r') as file:
        return file.read().strip()

def main():

    token = get_token()

    # Создаем экземпляр Application
    application = Application.builder().token(token).build()

    # Логируем успешную загрузку токена и запуск бота
    logger.info("Токен загружен. Запуск бота...")

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
            CallbackQueryHandler(main_menu, pattern="^(Давай начнем!|Назад в меню)$"),
            CallbackQueryHandler(cancel, pattern="^Пока$")
            ],
            CREATING_POST: [
                MessageHandler(
                    filters.Regex("^Создать пост$"), creating_post_func
                )
            ],
            CREATING_CHOICE: [
                MessageHandler(
                        filters.Regex("^Фото$"), photo_adding_func
                    ),
                MessageHandler(
                        filters.Regex("^Текст$"), text_adding_func
                    ),
                MessageHandler(
                        filters.Regex("^Кнопки$"), keyboard_adding_func
                    ),
                MessageHandler(
                        filters.Regex("^Удалить фото$"), delete_photo_func
                    ),
                MessageHandler(
                        filters.Regex("^Удалить текст$"), delete_text_func
                    ),
                MessageHandler(
                        filters.Regex("^Удалить кнопки$"), delete_keyboard_func
                    ),
                MessageHandler(
                        filters.Regex("^Далее$"), continue_func
                    ),
                MessageHandler(
                        filters.Regex("^Предпросмотр поста$"), preview_post
                    )
            ], 
            PHOTO_ADD: [
                MessageHandler(filters.PHOTO, save_photo)
            ],
            TEXT_ADD: [
                MessageHandler(filters.TEXT, save_text)
            ],
            KEYBOARD_ADD : [
                MessageHandler(filters.TEXT, save_keyboards)
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Пока"), cancel)]
    )

    application.add_handler(conv_handler)

    # Бот работает до нажатия пользователем Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
