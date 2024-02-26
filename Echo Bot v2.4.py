import telebot

# Replace 'YOUR_BOT_TOKEN' with your actual bot token

BOT_TOKEN = 'YOUR_BOT_TOKEN'

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Delete the webhook before polling
bot.delete_webhook()

# Handle the /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hi! I'm an echo bot. Send me a message, and I'll echo it back.")

# Handle the /status command
@bot.message_handler(commands=['status'])
def status(message):
    bot.reply_to(message, "I'm running and ready to echo messages.")

# Handle all messages (except commands)
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'audio', 'document', 'video', 'voice', 'sticker'])
def echo_message(message):
    # Send media files directly back to the same chat without any additional information
    if message.content_type == 'text':
        bot.send_message(message.chat.id, message.text)
    else:
        # Send the media file as if it was sent by the bot itself
        bot.send_chat_action(message.chat.id, 'upload_' + message.content_type.split('/')[0])
        
        # Get the caption of the media file
        caption = message.caption if message.caption else ''
        
        # Send the media file with the caption
        if message.content_type == 'photo':
            bot.send_photo(message.chat.id, message.photo[-1].file_id, caption=caption, disable_notification=True)
        elif message.content_type == 'audio':
            bot.send_audio(message.chat.id, message.audio.file_id, caption=caption, disable_notification=True)
        elif message.content_type == 'document':
            bot.send_document(message.chat.id, message.document.file_id, caption=caption, disable_notification=True)
        elif message.content_type == 'video':
            bot.send_video(message.chat.id, message.video.file_id, caption=caption, disable_notification=True)
        elif message.content_type == 'voice':
            bot.send_voice(message.chat.id, message.voice.file_id, caption=caption, disable_notification=True)
        elif message.content_type == 'sticker':
            bot.send_sticker(message.chat.id, message.sticker.file_id, disable_notification=True)

# Polling to receive updates
bot.polling()