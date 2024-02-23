import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, ConversationHandler
from telegram import Filters


TELEGRAM_BOT_TOKEN = '6543199534:AAEUVQrkL1rSlJcRqQJlGhVK5UPpXSnXJ0o'
WEBSITE_INFO_STATE = 1
user_states = {}  # Lưu trạng thái của người dùng

def send_message(chat_id, text):
    updater.bot.send_message(chat_id=chat_id, text=text)

def start(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    user_states[chat_id] = {'website_url': None}
    send_message(chat_id, 'Xin chào! Chọn "Check Website Info" để bắt đầu kiểm tra thông tin trang web.')
    return WEBSITE_INFO_STATE

def check_website_info(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    user_states[chat_id] = {'website_url': None}
    send_message(chat_id, 'Hãy gửi đường link của trang web bạn muốn kiểm tra.')
    return WEBSITE_INFO_STATE

def get_website_info(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    website_url = update.message.text
    user_states[user_id]['website_url'] = website_url

    website_info = fetch_website_info(website_url)
    send_message(chat_id, website_info)

    return ConversationHandler.END

def fetch_website_info(website_url):
    # Lấy thông tin vị trí từ ipinfo.io
    try:
        ip_address = requests.get(f'https://api.ipinfo.io/{website_url}?token=34496f1d02dc26').json().get('ip', 'N/A')
        ip_info = requests.get(f'https://ipinfo.io/{ip_address}?token=34496f1d02dc26').json()

        status = ip_info.get('status', 'N/A')
        country = ip_info.get('country', 'N/A')
        country_code = ip_info.get('country', 'N/A')
        region = ip_info.get('region', 'N/A')
        region_name = ip_info.get('region', 'N/A')
        city = ip_info.get('city', 'N/A')
        zip_code = ip_info.get('postal', 'N/A')
        latitude = ip_info.get('loc', '').split(',')[0]
        longitude = ip_info.get('loc', '').split(',')[1]
        timezone = ip_info.get('timezone', 'N/A')
        isp = ip_info.get('org', 'N/A')
        organization = ip_info.get('org', 'N/A')
        asn = ip_info.get('asn', 'N/A')

        result = f"Status: {status}\nCountry: {country}\nCountry Code: {country_code}\nRegion: {region}\nRegion Name: {region_name}\nCity: {city}\nZIP: {zip_code}\nLatitude: {latitude}\nLongitude: {longitude}\nTimezone: {timezone}\nISP: {isp}\nOrganization: {organization}\nAS: {asn}"

    except requests.RequestException as e:
        result = f"Error: {e}"

    return result

def main():
    global updater
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WEBSITE_INFO_STATE: [MessageHandler(~Filters.COMMAND & Filters.TEXT, get_website_info)],
        },
        fallbacks=[]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('check', check_website_info))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
