import telegram
import asyncio
# get id, username: https://api.telegram.org/bot[token]/getUpdates

def send_telegram(photo_path="alert.png", caption=""):
    try:
        my_token = "6163394004:AAEmyvIHyKBaD8c-yztl74ao2pX-9eF5CZA"
        bot = telegram.Bot(token=my_token)
        bot.sendPhoto(chat_id="5175598352", photo=open(photo_path, "rb"), caption=caption)
        print("good job")
    except Exception as ex:
        print("Can not send message telegram ", ex)

    print("Send sucess")

