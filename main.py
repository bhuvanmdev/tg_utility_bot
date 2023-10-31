# import logging

# from telegram import __version__ as TG_VER

# try:
#     from telegram import __version_info__
# except ImportError:
#     __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

# if __version_info__ < (20, 0, 0, "alpha", 1):
#     raise RuntimeError(
#         f"This example is not compatible with your current PTB version {TG_VER}. To view the "
#         f"{TG_VER} version of this example, "
#         f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
#     )
# from telegram import ForceReply, Update,ReplyKeyboardMarkup,ReplyKeyboardRemove
# from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# # Enable logging
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )
# # set higher logging level for httpx to avoid all GET and POST requests being logged
# logging.getLogger("httpx").setLevel(logging.WARNING)

# logger = logging.getLogger(__name__)


# # Define a few command handlers. These usually take the two arguments update and
# # context.
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Send a message when the command /start is issued."""
#     user = update.effective_user
#     await update.message.reply_html(
#         rf"Hi {filters.TEXT} {user.mention_html()}!",
#         reply_markup=ForceReply(selective=True),
#     )

# async def gender(update, context):



# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Send a message when the command /help is issued."""
#     await update.message.reply_text("Help!")


# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Echo the user message."""
#     await update.message.reply_text(update.message.text)

# class a:
#     def __init__(self):pass # this is how filters in message handler work
#     def check_update(self):
#         return True

# print(dir(filters))

# def main() -> None:
#     """Start the bot."""
#     # Create the Application and pass it your bot's token.
#     application = Application.builder().token("6359127570:AAG2B_8LIgVpudoihOil0AEAD37YxQAfF4Y").build()

#     # on different commands - answer in Telegram
#     application.add_handler(CommandHandler("start", start)) #/command--> function
#     application.add_handler(CommandHandler("help", help_command))

#     # on non command i.e message - echo the message on Telegram
#     application.add_handler(MessageHandler(filters.TEXT and ~filters.COMMAND,echo))

#     # Run the bot until the user presses Ctrl-C
#     application.run_polling(allowed_updates=Update.ALL_TYPES)


# if __name__ == "__main__":
#     main()

import logging,os,json
from turtle import up
os.chdir(r'C:\Users\bhuva\OneDrive\Desktop\tgbot')

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

data = json.load(open('pass.json'))
import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update , InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,#Handler--> takes input in their respective ways!! message,command,poll
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [[
        InlineKeyboardButton("1",callback_data='one'),#movie selection button type
        InlineKeyboardButton('2',callback_data='two')
    ]] #[["Boy", "Girl", "Other"]], one_time_keyboard=True , input_field_placeholder="Boy or Girl?"
    # print(dir(update.message))
    # kk = range(1,10)
    await update.message.reply_text(
        "Hi! My name is Professor Bot. I will hold a conversation with you. "
        "Send /cancel to stop talking to me.\n\n"
        "Are you a boy or a girl?"
        # ,
        # reply_markup=InlineKeyboardMarkup(
            # reply_keyboard
        # ),
    )
    # for k in kk:
    #     # await update.message.edit_text(str(k))
    #     print(update.update_id,'\n')
    #     await context.refresh_data()
    #     if update.MESSAGE is None:return ConversationHandler.END

    return GENDER


async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user# (update-->gets all meg from user and is mutable real-time!)
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "I see! Please send me a photo of yourself, "
        f"so I know what you look like, or send /skip if you don't want to.{dir(context)}",
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file =  update.message.photo[-1]
    j = await context.bot.get_file(photo_file.file_id)
    print('\n\n\n\n\n',j._get_encoded_url(),'\n\n\n\n')
    await j.download_to_drive(f"{photo_file.file_id}.jpg")
    logger.info("Photo of %s: %s", user.first_name, f"{photo_file.file_id}.jpg")
    await update.message.reply_text(
        "Gorgeous! Now, send me your location please, or send /skip if you don't want to."
    )
    return LOCATION if photo_file == () else PHOTO


async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    await update.message.reply_text(
        "I bet you look great! Now, send me your location please, or send /skip."
    )

    return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    await update.message.reply_text(
        "Maybe I can visit you sometime! At last, tell me something about yourself."
    )

    return BIO


async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    await update.message.reply_text(
        "You seem a bit paranoid! At last, tell me something about yourself."
    )

    return BIO


async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    if update.message is not None:
        user = update.message.from_user
    print(update.callback_query)
    # logger.info("Bio of %s: %s", user.first_name, update.message.text)
    # await update.message.reply_text("Thank you! I hope we can talk again some day.")
    await update.callback_query.edit_message_text(
        text="Fourth CallbackQueryHandler, Choose a route")# reply_markup=reply_markup
    # )
    return PHOTO


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user

    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )
    # await update.message.edi("yo")
    await update.effective_message.edit_text("hey")
    return ConversationHandler.END

async def stop(update,context : ContextTypes.DEFAULT_TYPE):
    print(context.user_data)

def main() -> None:
    """Run the bot."""
    app = Application.builder().token(data["token"]).build()
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(data["bot"]["token"]).arbitrary_callback_data(True).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandaHndler("start", start,fil)], #,MessageHandler(filters.TEXT,cancel)],#string to put in bot| function to run--> return value used in states
        states={ #states={0:..,1:..}[return_value](gets run)
            GENDER: [MessageHandler(filters.Regex("^(?i)(Boy|Girl|Other)$"), gender),CallbackQueryHandler(bio, pattern="^" + '(one|two)' + "$")],
            PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("skip", skip_photo)],
            LOCATION: [
                MessageHandler(filters.LOCATION, location),#takes anything not command and also applies the filters
                CommandHandler("skip", skip_location),#takes commands written "/" 
            ],
            BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],#can run irrespective of the "states" it currently is in.
    )

    application.add_handler(conv_handler)

    application.add_handler(MessageHandler(filters.Regex("^(?i)(stop)$"),stop))
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()