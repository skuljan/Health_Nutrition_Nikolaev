# handlers/common.py

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from handlers.brand_handler import show_brands
from handlers.sku_handler import show_skus
from handlers.date_handler import show_dates
from utils.data_loader import combined_df

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    brands = combined_df['gb.name'].unique()
    context.user_data['brands'] = brands
    context.user_data['brand_page'] = 0
    return await show_brands(update, context)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Процесс отменен.')
    return ConversationHandler.END

async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'date' in context.user_data:
        del context.user_data['date']
        return await show_dates(update, context)
    elif 'sku_id' in context.user_data:
        del context.user_data['sku_id']
        return await show_skus(update, context)
    elif 'brand' in context.user_data:
        del context.user_data['brand']
        return await show_brands(update, context)
    return await start(update, context)