from data import get_similar, possible_results, get_data


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
import os
import re

PORT = int(os.environ.get('PORT', '8443'))

def get_query(update, context):
    text = update.message.text.strip()
    res = possible_results(text)

    
    keyboard = create_markup_buttons(res)
    

    update.message.reply_text('Search Results', reply_markup=keyboard)

def create_markup_buttons(res, r=False):
    keyboard = []
    if r:
        for x,y in res.items():
            key = InlineKeyboardButton(text=str(y),
	                                   callback_data=str(f'r{x}'))
            keyboard.append([key])
    else:
        for x,y in res.items():
            key = InlineKeyboardButton(text=str(y),
	                                   callback_data=str(x))
            keyboard.append([key])
    return InlineKeyboardMarkup(keyboard)




def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    query.answer()
    d = str(query.data)
    print(d)
    if 'r' not in d:

        index = int(d)
        res = get_similar(index)
        keyboard = create_markup_buttons(res, r=True)
        query.edit_message_text(text=f"Similar movies: tap to see the details",
    							reply_markup=keyboard)

    else:
        d = int(d[1:])
        movie_detail = get_data(d)
        query.edit_message_text(text=movie_detail)







def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    TOKEN = "5330473593:AAGhxPMVuvw9MM5HFOATF64Dx9RMOlwLhEw"
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("start", start))
    # dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_query))

    # Start the Bot
    updater.start_webhook(
        listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN,
        webhook_url='https://movie-rec-2001.herokuapp.com/' + TOKEN
    )

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

main()