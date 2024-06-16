# handlers/sku_handler.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.callback_data import encode_callback_data, decode_callback_data
from utils.data_loader import combined_df

ITEMS_PER_PAGE = 5
SKU = 1

async def show_skus(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    page = context.user_data['sku_page']
    skus = context.user_data['skus']
    keyboard = [[InlineKeyboardButton(sku['dp.name'], callback_data=encode_callback_data(str(sku['cr.external_id'])))] for _, sku in skus.iloc[page*ITEMS_PER_PAGE:(page+1)*ITEMS_PER_PAGE].iterrows()]

    if page > 0:
        keyboard.append([InlineKeyboardButton("Previous", callback_data="previous_sku_page")])
    if (page+1)*ITEMS_PER_PAGE < len(skus):
        keyboard.append([InlineKeyboardButton("Next", callback_data="next_sku_page")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text=f"Вы выбрали {context.user_data['brand']}. Теперь выберите SKU:", reply_markup=reply_markup)
    return SKU

async def select_sku(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    from handlers.date_handler import show_dates  # Lazy import to avoid circular import

    query = update.callback_query
    await query.answer()

    if query.data == "previous_sku_page":
        context.user_data['sku_page'] -= 1
        return await show_skus(update, context)
    elif query.data == "next_sku_page":
        context.user_data['sku_page'] += 1
        return await show_skus(update, context)
    else:
        sku_id = decode_callback_data(query.data)
        context.user_data['sku_id'] = sku_id
        dates = combined_df['cr.observed_at'].unique()
        context.user_data['dates'] = dates
        context.user_data['date_page'] = 0
        return await show_dates(update, context)