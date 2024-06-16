# handlers/brand_handler.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.data_loader import combined_df
from utils.callback_data import encode_callback_data, decode_callback_data

ITEMS_PER_PAGE = 5
BRAND = 0


async def show_brands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    page = context.user_data.get('brand_page', 0)
    brands = context.user_data.get('brands', combined_df['gb.name'].unique())
    context.user_data['brands'] = brands
    keyboard = [[InlineKeyboardButton(brand, callback_data=encode_callback_data(brand))] for brand in
                brands[page * ITEMS_PER_PAGE:(page + 1) * ITEMS_PER_PAGE]]

    if page > 0:
        keyboard.append([InlineKeyboardButton("Previous", callback_data="previous_brand_page")])
    if (page + 1) * ITEMS_PER_PAGE < len(brands):
        keyboard.append([InlineKeyboardButton("Next", callback_data="next_brand_page")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query:
        await update.callback_query.edit_message_text('Пожалуйста, выберите бренд:', reply_markup=reply_markup)
    else:
        await update.message.reply_text('Пожалуйста, выберите бренд:', reply_markup=reply_markup)

    return BRAND


async def select_brand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    from handlers.sku_handler import show_skus  # Lazy import to avoid circular import

    query = update.callback_query
    await query.answer()

    if query.data == "previous_brand_page":
        context.user_data['brand_page'] -= 1
        return await show_brands(update, context)
    elif query.data == "next_brand_page":
        context.user_data['brand_page'] += 1
        return await show_brands(update, context)
    else:
        brand = decode_callback_data(query.data).strip()
        context.user_data['brand'] = brand
        skus = combined_df[combined_df['gb.name'] == brand][['dp.name', 'cr.external_id']].drop_duplicates()
        context.user_data['skus'] = skus
        context.user_data['sku_page'] = 0
        return await show_skus(update, context)