import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import random
import pymongo
url = "mongodb+srv://demo_maker:demo_maker@cluster0.cnu98.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(url)
db = client["Karan"]
data = db["Deposit"]
token = "5005060165:AAGNFaOTFCrnBWHGMj47m5b0gIaurZiuabY"
bot = telebot.TeleBot(token)
pay_token = "yAwM2EBjWoGrFV4z"

def get_orderid(id,amo):
    num = random.randint(10000, 10000000)
    find = data.find_one({"Order":num})
    if find != None:
        return "Already"
    data.insert_one({"Order":num,"User":id,"Amount":amo})
    return num



def pay(message):
    user = message.chat.id
    msg = message.text
    order_id = get_orderid(user,msg)
    if order_id == "Already":
        bot.send_message(user, "PLease Try Again")
        return
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Pay',url=f"https://full2sms.in/accept_payment_api.php?token={pay_token}&amount={msg}&order_id={order_id}"),InlineKeyboardButton("Paid",callback_data=f"paid_{order_id}"))
    bot.send_message(user,"Hello World",reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: True)
def call_query(call):
    user = call.message.chat.id
    if call.data.startswith('paid_'):
        order_id = call.data.split("_")[1]
        print(order_id)
        url = f"https://full2sms.in/status_order.php?order_id={order_id}"
        r = requests.get(url)
        status = r.json()['status']
        if status == "success":
            bot.send_message(user,"Paid Success")
        else:
            bot.send_message(user,"Paid Failed")
@bot.message_handler(commands=['start'])
def start(message):
    user = message.chat.id
    bot.send_message(user,"Send Amount You Want To Deposit")
    bot.register_next_step_handler(message,pay)

if __name__ == "__main__":
    print("Done")
    bot.polling()

