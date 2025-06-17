import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler

TOKEN = "8064065506:AAEhEhDYD7DJqumMztFVava42YMB1ju-OWI"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Этапы сценариев
(G_CITY, G_TOTAL_BS, G_DOWN_BS, G_TIME, G_CAUSE, G_RESPONSIBLE) = range(6)
current_template = ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ассаламу алейкум! Выберите тип рассылки:\n/outage\n/degradation\n/datacenter")
/outage
/degradation
/datacenter")

# OUTAGE
async def outage_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['type'] = "outage"
    await update.message.reply_text("Введите город:")
    return G_CITY

async def collect_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['city'] = update.message.text
    await update.message.reply_text("Введите общее количество БС:")
    return G_TOTAL_BS

async def collect_total_bs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['total_bs'] = update.message.text
    await update.message.reply_text("Сколько из них вне сервиса?")
    return G_DOWN_BS

async def collect_down_bs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['down_bs'] = update.message.text
    await update.message.reply_text("Введите время начала (например, 10:19 10.01.2025):")
    return G_TIME

async def collect_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['time'] = update.message.text
    await update.message.reply_text("Введите причину:")
    return G_CAUSE

async def collect_cause(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['cause'] = update.message.text
    await update.message.reply_text("Введите ответственных:")
    return G_RESPONSIBLE

async def collect_responsible(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['responsible'] = update.message.text
    data = context.user_data
    msg = f"Наблюдается отсутствие всех видов сервисов для абонентов компании в г. {data['city']} с {data['time']}. " +           f"Вне сервиса {data['down_bs']} БС из {data['total_bs']}. Причина: {data['cause']}. Ответственный: {data['responsible']}."
    await update.message.reply_text("📢 Готовое сообщение:

" + msg)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Операция отменена.")
    return ConversationHandler.END

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    outage_conv = ConversationHandler(
        entry_points=[CommandHandler("outage", outage_start)],
        states={
            G_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_city)],
            G_TOTAL_BS: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_total_bs)],
            G_DOWN_BS: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_down_bs)],
            G_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_time)],
            G_CAUSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_cause)],
            G_RESPONSIBLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_responsible)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(outage_conv)
    app.run_polling()