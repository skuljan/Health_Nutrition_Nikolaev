# handlers/date_handler.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from utils.data_loader import combined_df
from utils.callback_data import encode_callback_data, decode_callback_data

ITEMS_PER_PAGE = 5
DATE = 2

async def show_dates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    page = context.user_data['date_page']
    dates = context.user_data['dates']
    keyboard = [[InlineKeyboardButton(str(date), callback_data=encode_callback_data(str(date)))] for date in dates[page*ITEMS_PER_PAGE:(page+1)*ITEMS_PER_PAGE]]

    if page > 0:
        keyboard.append([InlineKeyboardButton("Previous", callback_data="previous_date_page")])
    if (page+1)*ITEMS_PER_PAGE < len(dates):
        keyboard.append([InlineKeyboardButton("Next", callback_data="next_date_page")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text=f"Вы выбрали {context.user_data['sku_id']}. Теперь выберите дату:", reply_markup=reply_markup)
    return DATE

async def select_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "previous_date_page":
        context.user_data['date_page'] -= 1
        return await show_dates(update, context)
    elif query.data == "next_date_page":
        context.user_data['date_page'] += 1
        return await show_dates(update, context)
    else:
        date = decode_callback_data(query.data)
        context.user_data['date'] = date

        selected_data = combined_df[
            (combined_df['gb.name'] == context.user_data['brand']) &
            (combined_df['cr.external_id'] == int(context.user_data['sku_id'])) &
            (combined_df['cr.observed_at'] == date)
        ]

        if selected_data.empty:
            await query.edit_message_text(text=f"Для выбранных параметров нет данных. Пожалуйста, попробуйте снова.")
            return DATE  # Позволить пользователю выбрать другую дату

        platforms = selected_data['platform'].unique()
        response_text = f"Самая низкая цена на {context.user_data['brand']} ({context.user_data['sku_id']}) за {date}:\n\n"

        for platform in platforms:
            platform_data = selected_data[selected_data['platform'] == platform]
            cheapest_option = platform_data.loc[platform_data['cr.price_with_discount'].idxmin()]

            response_text += (
                f"Платформа: {platform}\n"
                f"Цена: {cheapest_option['cr.price_with_discount']} рублей\n"
                f"[Ссылка]({cheapest_option['dp.url']})\n\n"
            )

        response_text += "Вы можете выбрать новый бренд с помощью /start или вернуться на предыдущий шаг с помощью /back."

        await query.edit_message_text(
            text=response_text,
            parse_mode='Markdown'
        )
        return ConversationHandler.END