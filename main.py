# main.py

import logging
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, CallbackQueryHandler
from config import TELEGRAM_BOT_TOKEN
from handlers.brand_handler import select_brand
from handlers.sku_handler import select_sku
from handlers.date_handler import select_date
from handlers.common import start, cancel, back

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BRAND, SKU, DATE = range(3)

def main() -> None:
    token = TELEGRAM_BOT_TOKEN
    if not token:
        raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables")

    application = ApplicationBuilder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            BRAND: [CallbackQueryHandler(select_brand)],
            SKU: [CallbackQueryHandler(select_sku)],
            DATE: [CallbackQueryHandler(select_date)],
        },
        fallbacks=[CommandHandler('cancel', cancel), CommandHandler('back', back)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('back', back))
    application.add_handler(CommandHandler('cancel', cancel))

    application.run_polling()

if __name__ == '__main__':
    main()